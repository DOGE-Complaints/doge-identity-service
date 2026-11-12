# 13. Verified Person Hash и Conflict Detection

> **Актуализировано 2026-06-24 под фактический код (решение Q4: код — истина, ADR-IDS-008).** См. `docs/analysis/identity-backend-full-audit-2026-06-24.md`.
>
> **Статус (AS-BUILT):**
> - **Phone-hash** (`verified_phone_hash`) — **активный механизм** верифицированной личности. Реализован в `src/core/phone/otp_engine.py`, `src/core/api/handlers.py`, репозиториях.
> - **eID-hash** (`verified_person_hash`) — путь существует в коде (`handlers.py`, репозитории), но **подключение eID ОТЛОЖЕНО**; используется двухстадийная модель ADR-IDS-008.
> - Хэш-механизм — `src/core/security/hashing.py:hash_secret` (HMAC-SHA256, hex).
> - Conflict detection — `src/core/infrastructure/repositories.py` (in-memory) и `db_supabase.py` (Supabase).
>
> **Предусловие:** profiles table с partial unique index (`unique_verified_phone_hash`, миграция `20260611000001_profiles_phone_verification.sql`).
> **Связь:** eID-ветка вызывается в eID callback; phone-ветка — в confirm phone verification.

---

## Назначение

Псевдонимный hash верифицированной личности позволяет:
1. Детектировать дубли (один человек / один номер → один civic account).
2. Привязать верификацию к профилю.
3. Никогда не раскрывать сырые PII (personal_code, номер телефона) — ни в API, ни в logs, ни on-chain.

В коде существуют **два хэша** с одинаковым механизмом, но разными входами:

| Hash | Колонка | Вход | Статус |
|------|---------|------|--------|
| `verified_phone_hash` | `profiles.verified_phone_hash` | E.164 номер телефона | **активный** |
| `verified_person_hash` | `profiles.verified_person_hash` | provider-agnostic `subject_hash` от eID-провайдера | существует, но eID **отложен** |

Оба используют один и тот же HMAC-ключ — `config.eid_secret` (env `DOGESTONIA_EID_SECRET`).

---

## Хэш-механизм (общий)

Фактическая реализация — `src/core/security/hashing.py`:

```python
# src/core/security/hashing.py
import hashlib
import hmac


def hash_secret(plaintext: str, *, key: str) -> str:
    """HMAC-SHA256 hex digest; key передаётся явно (без global state)."""
    return hmac.new(key.encode("utf-8"), plaintext.encode("utf-8"), hashlib.sha256).hexdigest()
```

**Свойства:**
- Детерминированный: тот же вход + тот же `key` → тот же hash.
- Односторонний: hash не разворачивается обратно в plaintext.
- Key-ed (HMAC): бесполезен без server-side секрета `eid_secret`.

---

## Генерация `verified_phone_hash` (активный путь)

`hash_secret` применяется к E.164-номеру:

```python
# src/core/phone/otp_engine.py (start: ~53, confirm: ~96)
phone_hash = hash_secret(e164, key=key)          # key = config.eid_secret
# ...
subject_hash = hash_secret(e164, key=key)        # тот же вход при подтверждении
```

В handler-е (`src/core/api/handlers.py:~553`) повторно вычисляется `expected_phone_hash = hash_secret(e164, key=deps.config.eid_secret or "")` и сравнивается с `session.phone_hash` для защиты сессии.

**Вход:** E.164 (например, `"+3725xxxxxxx"`). Country-scoping обеспечивается самим префиксом страны внутри E.164 — отдельного `{country}:` префикса для phone-hash НЕТ.

---

## Генерация `verified_person_hash` (eID, двухстадийная модель — ADR-IDS-008)

Фактический код (`src/core/api/handlers.py:~378-381`):

```python
verified_person_hash = hash_secret(
    f"{verification.country}:{verification.subject_hash}",
    key=deps.config.eid_secret or "",
)
```

Где `verification` — это `EIDVerificationResult` (`src/core/providers/base.py:~21-29`), а `subject_hash` — **provider-agnostic непрозрачное значение**, которое возвращает eID-провайдер. Это **НЕ** сырой `personal_code`.

**Двухстадийная модель (ADR-IDS-008):**
1. Провайдер отдаёт `subject_hash` (provider-agnostic, `provider` — только provenance).
2. Оркестратор HMAC-ит строку `{country}:{subject_hash}` с ключом `eid_secret`.

**Форматирование входных данных:**
- `country` — как отдаёт провайдер (`EIDVerificationResult.country`); uppercase нормализация в коде хэширования не выполняется.
- Разделитель `:` — фиксирован.

> ⚠️ **OBSOLETE (ADR-IDS-008 revision).** Прежняя формула `HMAC("{country}:{personal_code}")` над сырым `personal_code`, а также модуль `src/core/auth/verified_person_hasher.py` и функция `generate_verified_person_hash(...)` — **в коде НЕ существуют**. Сырой `personal_code` оркестратором не хэшируется; вместо него хэшируется provider-agnostic `subject_hash`.

---

## Conflict Detection

Вызывается внутри `attach_*_verification` репозитория сразу после генерации hash.

### eID-ветка (`attach_eid_verification`)

`src/core/infrastructure/repositories.py:~115-119` (in-memory) и `db_supabase.py:~411-443`:

| Case | Условие | Действие |
|------|---------|---------|
| **A** — hash новый | по hash → не найден | Привязать к current account: `eid_verified=true`, `verified_person_hash`, провайдер/метод/страна, `eid_verified_at` |
| **B** — hash принадлежит current user | найден, `supabase_user_id == current` | Идемпотентно: профиль обновляется на тот же hash (исключение НЕ бросается) |
| **C** — hash принадлежит другому | найден, `supabase_user_id != current` | Бросить `ProfileConflictError` |

### Phone-ветка (`attach_phone_verification`)

`src/core/infrastructure/repositories.py:~176-181` и `db_supabase.py:~500-505`. Проверка включается флагом `config.phone_one_account_per_number` (one-number-one-account):

| Case | Условие | Действие |
|------|---------|---------|
| **A** — hash новый | по `verified_phone_hash` → не найден | `phone_verified=true`, `verified_phone_hash`, провайдер/dial_prefix, `phone_verified_at` |
| **B** — hash принадлежит current user | найден, `supabase_user_id == current` | Идемпотентно (исключение НЕ бросается) |
| **C** — hash принадлежит другому | найден, `supabase_user_id != current` | Бросить `ProfileConflictError` |

**MVP: auto-merge аккаунтов ЗАПРЕЩЁН.**

---

## Реализация конфликта (фактическая)

Репозиторий не возвращает status-enum, а **бросает `ProfileConflictError`**. Маппинг в HTTP делает handler.

**eID** (`src/core/api/handlers.py:~383-411`):

```python
try:
    profile_repo.attach_eid_verification(
        session.supabase_user_id,
        provider=verification.provider,
        country=verification.country,
        method=verification.login_method,
        verified_person_hash=verified_person_hash,
        verified_at=verification.verified_at,
    )
except ProfileConflictError as exc:
    store.mark_failed(session.id, "profile_conflict")
    # ... audit ...
    return EidCallbackOutcome(
        outcome="failed",
        return_url=session.return_url,
        error_code=None,
        json_status=409,
        envelope_code="profile_conflict",
        envelope_message=str(exc),
    )
```

**Phone** (`src/core/api/handlers.py:~580-600`):

```python
try:
    profile_repo.attach_phone_verification(
        user_id,
        provider=verification.provider,
        dial_prefix=verification.dial_prefix,
        verified_phone_hash=verification.subject_hash,
        verified_at=verification.verified_at,
        one_account_per_number=deps.config.phone_one_account_per_number,
    )
except ProfileConflictError as exc:
    # ... audit ...
    body = build_error_envelope("profile_conflict", str(exc), trace_id=trace_id)
    return body, 409
```

> ⚠️ В обоих случаях конфликт → envelope code **`profile_conflict`** при HTTP **409**. Прежний код `identity_already_linked` в `src/` **не встречается** и удалён из этого spec.

---

## Race Condition Protection

**Сценарий:** Два запроса с одним hash одновременно.

**Защита:**
1. `UNIQUE INDEX unique_verified_phone_hash` (`supabase/migrations/20260611000001_profiles_phone_verification.sql`) — финальный enforcer для phone.
2. Supabase-репозиторий (`db_supabase.py:~438-443`, `~523-527`) ловит `httpx.HTTPStatusError` со статусом 409 от PostgREST и переводит его в `ProfileConflictError` — то есть нарушение UNIQUE constraint трактуется как конфликт (Case C), а не как необработанное исключение.

---

## Ограничения использования hash (`verified_person_hash` и `verified_phone_hash`)

| Место | Разрешено | Запрещено |
|-------|---------|---------|
| Хранение в DB (profiles) | ✅ | — |
| Использование для conflict detection | ✅ | — |
| API response (`/me`) | ❌ | Никогда |
| Logs / audit events | ❌ | Никогда |
| Custom GPT token claims | ❌ | Никогда |
| On-chain | ❌ | Никогда |

---

## Тип результата eID-callback (фактический)

Dataclass `AttachEidResult` со status-enum **не существует** в коде. Реальный тип результата eID-callback — **`EidCallbackOutcome`** (`src/core/api/eid_callback.py`):

```python
EidCallbackOutcomeKind = Literal["verified", "already_verified", "failed"]


@dataclass(frozen=True)
class EidCallbackOutcome:
    outcome: EidCallbackOutcomeKind
    return_url: str | None
    error_code: EidErrorCode | None
    json_status: int
    envelope_code: str = "ok"
    envelope_message: str = ""
    envelope_data: dict[str, object] | None = None
```

Маппинг на ответы (`build_callback_json_envelope`, `append_eid_redirect_query`):
```
outcome="verified"          → success envelope {status: "verified"}      / redirect ?eid_status=verified
outcome="already_verified"  → success envelope {status: "already_consumed"} / redirect ?eid_status=verified
outcome="failed" (конфликт) → error envelope code="profile_conflict", 409  / redirect ?eid_status=error
```

Сам конфликт привязки сигнализируется через `ProfileConflictError` из репозитория (см. выше), а не через значение enum.

---

## Acceptance Criteria (AS-BUILT)

- [ ] `hash_secret(x, key=X)` детерминирован при одинаковых входах
- [ ] eID: `hash_secret("EE:" + subject_hash, key=X)` != `hash_secret("LV:" + subject_hash, key=X)` (country scope через префикс)
- [ ] `hash_secret(x, key=X)` != `hash_secret(x, key=Y)` (key/pepper scope)
- [ ] eID-вход — provider-agnostic `subject_hash`, НЕ сырой `personal_code`
- [ ] Phone-вход — E.164 номер
- [ ] Case A: новый hash → профиль помечается verified, hash установлен
- [ ] Case B: тот же пользователь → идемпотентно, `ProfileConflictError` НЕ бросается
- [ ] Case C: другой пользователь → `ProfileConflictError` → envelope `profile_conflict` / HTTP 409
- [ ] Race condition: 409 от PostgREST (UNIQUE violation) → `ProfileConflictError` (не необработанное исключение)
- [ ] `verified_person_hash` / `verified_phone_hash` не возвращаются ни в одном API response
- [ ] Сырые PII (`personal_code`, номер телефона) не логируются ни в каком log statement
