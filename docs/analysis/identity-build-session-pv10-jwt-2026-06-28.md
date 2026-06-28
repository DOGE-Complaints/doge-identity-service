# Отчёт о работах в doge-identity-service (2026-06-28)

> **Дата:** 2026-06-28  
> **Объект:** Builder Queue волна **STORY-IDS-PV-10** (File SMS sink dev) + post-audit override + инцидент интеграции spa `/verify`  
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с путями к коду/артефактам  
> **SSOT процесса:** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) · [`ids-epic-execution-pipeline.md`](../tasks/ids-epic-execution-pipeline.md)

---

## 0. Executive summary

За одну build-сессию закрыта полная волна **EPIC-IDS-10 / PV-10**:

| Фаза | Результат |
|------|-----------|
| **P1** materialize | `pkg-000041`, 7 task README (t01–t07) |
| **P3** execute | Runtime `SMS_PROVIDER=file`, 8 offline-тестов, **394 pytest** |
| **P4** audit | [`epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md`](./epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md) — F2 inline, backlog F1 |
| **P5** scaffold | safe-override `run_mode=epic_ids_10_pv_10_audit_2026_06_28`, task **t08** |
| **P6** override | F1 pipeline story sync (docs-only), override закрыт |
| **P8 (частично)** | 3 git-коммита `feat/test/docs(ids-pv-10)` на `dev` |

**Параллельно** (интеграция spa ↔ identity, вне pkg-000041): обнаружен и исправлен блокер **`GET /me` → 401** для Supabase Cloud JWT (**ES256**), из‑за которого spa показывал «Session Expired» на `#/verify`. Исправление в [`supabase_validator.py`](../../src/core/auth/supabase_validator.py) — **на диске, ещё не в git** (см. §6).

> ⚠️ **Жёсткая валидация JWT-фикса — см. §10.** По сути решение верное, но **в текущем виде коммитить нельзя**: 1× 🔴 блокер (debug-лог с хардкод-путём на hot-path) + связка 🟠 (нарушение DI, утечка httpx.Client, magic-string `demo.local`, **нулевое тест-покрытие нового JWKS-пути**, demo-fallback секрет). Вердикт и список доработок — §10.

---

## 1. Зачем PV-10 (обоснование продукта)

**Проблема (G-SMS-1):** при `SMS_PROVIDER=mock` OTP остаётся только в памяти процесса ([`mock_sender.py`](../../src/core/phone/mock/mock_sender.py)); оператор, тестирующий через браузер, **не видит код**. Telnyx тратит бюджет.

**Решение:** провайдер `file` — append plaintext OTP в `<outbox>/<E.164>.log` с UTC-таймстемпом; чтение через `tail -f`. Dev-only: fail-fast при `APP_PROFILE=pilot` ([`schema.py:180-183`](../../src/core/config/schema.py)).

**Источник требований:** [`STORY-IDS-PV-10-file-sms-sink-dev.md`](../tasks/backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md) · [`runbook/sms-mock-testing.md`](../runbook/sms-mock-testing.md) §G-SMS-1 (перенесён из `analysis/` при P8).

---

## 2. Runtime: что реализовано (P3)

### 2.1 Новый пакет `src/core/phone/file/`

| Файл | Назначение |
|------|------------|
| [`file_sender.py`](../../src/core/phone/file/file_sender.py) | `FileSmsSender`: append `{utc_iso}\t{text}\n`, sanitize `[+0-9]`, `.replace(microsecond=0)` |
| [`config.py`](../../src/core/phone/file/config.py) | `FILE_SMS_OUTBOX_DIR`, default `var/sms-outbox` |
| [`descriptor.py`](../../src/core/phone/file/descriptor.py) | Дескриптор `file`, wiring в registry |

### 2.2 Интеграция в phone backbone

| Изменение | Файл | Обоснование |
|-----------|------|-------------|
| Регистрация `FILE_SMS_DESCRIPTOR` | [`registry_builder.py:4,12`](../../src/core/phone/registry_builder.py) | `SMS_PROVIDER=file` → активный sender |
| `file` без httpx | [`runtime_factory.py:14-15,26-29`](../../src/core/phone/runtime_factory.py) | Как `mock`; settings грузятся до http-блока |
| Pilot fail-fast | [`schema.py:180-183`](../../src/core/config/schema.py) | Plaintext OTP на диск запрещён в pilot |
| `.gitignore` outbox | [`.gitignore:11`](../../.gitignore) | Не коммитить OTP-логи |
| `.env.example` | [`.env.example:63,71-72`](../../.env.example) | `mock \| file \| telnyx`, `FILE_SMS_OUTBOX_DIR` |

### 2.3 Тесты

- [`tests/test_phone_file_sms_sender.py`](../../tests/test_phone_file_sms_sender.py) — **8** offline-тестов (append, sanitize, pilot reject, e2e `POST /auth/phone/request`, no-http-client).
- Полная сюита после P3: **394 passed** (`pytest -m "not live_integration"`) — см. [`run-summary-20260628-1747-…`](../../docs/tasks/run-reports/identity-build-windows/run-summary-20260628-1747-epic-ids-10-pv-10-pkg-000041.md).

### 2.4 Active package (не менялся после P5/P6)

- Pointer: [`identity-active-package.current.yaml`](../tasks/identity-active-package.current.yaml) → `pkg-000041` (**7 paths**, t01–t07).
- Audit override **не** создавал `pkg-000042` (порог safe-override: 1 gap, 1 task).

---

## 3. Builder Queue: audit → scaffold → override

### 3.1 P4 audit SSOT

Отчёт: [`epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md`](./epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md)

| Finding | Severity | Действие |
|---------|----------|----------|
| **F1** pipeline story ms timestamps | LOW | task **t08** (P6) |
| **F2** EPIC-IDS-PHONE header без PV-10 | LOW | closed **inline** в P4 ([`EPIC-IDS-PHONE.md:3`](../tasks/backlog-stories/phone-verification/EPIC-IDS-PHONE.md)) |
| INFO-1..3 | INFO | excluded |

### 3.2 P5 scaffold

- Task: [`task-ids-10-10-t08-audit-f1-pipeline-story-timestamp-example-sync/README.md`](../tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t08-audit-f1-pipeline-story-timestamp-example-sync/README.md)
- `run_mode=epic_ids_10_pv_10_audit_2026_06_28` в [`ID_builder.plan.md`](../../../.cursor/plans/ID_builder.plan.md) §safe-override
- Gap queue + task queue t08 в [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md)

### 3.3 P6 override (docs-only)

**Изменён один файл runtime-docs:**

- Pipeline story §«Целевое поведение»: `.345Z`/`.118Z` → `T10:01:02Z` / `T10:03:40Z`  
  [`STORY-IDS-PV-10-file-sms-sink-dev.md:27-28`](../tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/STORY-IDS-PV-10-file-sms-sink-dev.md)

**Gate:**

```bash
grep -n "345Z\|118Z" …/STORY-IDS-PV-10-file-sms-sink-dev.md   # no matches
grep -n "T10:01:02Z" backlog + pipeline story                    # both aligned
```

Run summary: [`run-summary-20260628-1811-epic-ids-10-pv-10-audit-override.md`](../tasks/run-reports/identity-build-windows/run-summary-20260628-1811-epic-ids-10-pv-10-audit-override.md)

**Bullrun:** P6 Done line, F1 🟢, t08 🟢, override закрыт ([`bullrun-launch-index.md:11-15`](../tasks/bullrun-launch-index.md)).

---

## 4. Документация и runbook (P8 commits)

### 4.1 Git-коммиты на `dev` (identity repo)

| Commit | Scope | Содержимое |
|--------|-------|------------|
| `37c5bfc` | **feat(ids-pv-10)** | `phone/file/*`, registry, runtime_factory, schema pilot gate |
| `9af8a7e` | **test(ids-pv-10)** | `test_phone_file_sms_sender.py` |
| `283913d` | **docs(ids-pv-10)** | `.env.example`, `.gitignore`, runbook, audit report |

**Намеренно не в git** (политика builder-session): `docs/tasks/**`, acceptance-verification, run-summary task-артефакты — остаются в рабочей зоне Builder Queue.

### 4.2 Runbook

[`docs/runbook/sms-mock-testing.md`](../runbook/sms-mock-testing.md) — операторский how-to: три режима SMS, quick start `file`, pilot/Railway нюансы, `file:line` ссылки на код.

---

## 5. Инцидент интеграции: spa «Session Expired» на `#/verify`

### 5.1 Симптом

После успешного Supabase-login spa на [`#/verify`](../../../spa-app/docs/runtime-docs/manual-smoke-phone-verification.md) показывает overlay **«Session Expired»** ([`SessionShellPanels.jsx:69-74`](../../../spa-app/src/components/SessionShellState/SessionShellPanels.jsx)).

### 5.2 Цепочка (факты из кода)

```mermaid
flowchart LR
  login[Supabase login OK] --> token[access_token в session]
  token --> shell[useSessionShellState]
  shell --> me[GET /me identity]
  me -->|401 AUTHENTICATION_REQUIRED| expired[shellState session_expired]
  expired --> ui[Session Expired overlay]
```

| Шаг | Код | Факт |
|-----|-----|------|
| Shell state | [`useSessionShellState.js:39-49`](../../../spa-app/src/auth/useSessionShellState.js) | `fetchMe(token)` после login |
| 401 → expired | [`sessionShellState.js:21-24`](../../../spa-app/src/auth/sessionShellState.js) | `AuthenticationRequiredError` + `hadAccessToken` → `SESSION_EXPIRED` |
| Login маскирует ошибку | [`LoginPage.jsx:56-61`](../../../spa-app/src/pages/LoginPage.jsx) | `fetchMe` catch пустой → «Welcome Back» даже при 401 |
| spa config | [`spa-app/.env`](../../../spa-app/.env) | `VITE_IDENTITY_MOCK_MODE=false` → реальный `/me` |

### 5.3 Root cause (runtime logs, debug session 3c4b9a)

Backend log при валидации Supabase JWT:

```text
unsupported_algorithm: Algorithm of 'ES256' is not allowed
usingDemoFallbackSecret: true
expectedIss: https://ydocxoquirltrrfmvpqz.supabase.co/auth/v1
```

| Фактор | Доказательство |
|--------|----------------|
| Supabase Cloud выдаёт **ES256** JWT | debug log `supabase_validator.py:validate` |
| Старый валидатор — только **HS256** | [`supabase_validator.py`](../../src/core/auth/supabase_validator.py) (до правки): `algorithms=["HS256"]` |
| `SUPABASE_JWT_SECRET` **отсутствует** в [`.env`](../../.env) | grep → no match; fallback `"test-secret-for-demo"` ([`providers.py:107-109`](../../src/core/infrastructure/providers.py)) |

Спека [`09-supabase-jwt-validation.md`](../requirements/09-supabase-jwt-validation.md) §RS256/JWKS предупреждала о Cloud JWKS; код до сессии реализовывал только HS256 MVP.

### 5.4 Исправление (на диске, §6)

Расширен [`SupabaseJwtValidatorImpl`](../../src/core/auth/supabase_validator.py):

- **HS256** — прежний путь (OctKey + `SUPABASE_JWT_SECRET`, тесты offline).
- **ES256 / RS256 / ES384 / ES512** — JWKS `{SUPABASE_URL}/auth/v1/.well-known/jwks.json` через существующий [`JwksCache`](../../src/core/security/oidc/jwks_cache.py) (паттерн [`id_token.py:42-55`](../../src/core/security/oidc/id_token.py)).
- Алгоритм выбирается по JWT header (`alg`), не по эвристике.

Unit-тесты JWT: **17 passed** (`test_supabase_jwt_validator.py`, `test_supabase_jwt_auth.py`) после правки.

---

## 6. Состояние на диске vs git (на момент отчёта)

### 6.1 В git (`dev`, pushed не проверялся)

- PV-10 runtime + tests + runbook (§4.1)

### 6.2 В рабочей зоне, **не закоммичено**

| Изменение | Файлы | Рекомендация |
|-----------|-------|--------------|
| **JWT ES256/JWKS** | [`supabase_validator.py`](../../src/core/auth/supabase_validator.py), [`providers.py:107-110`](../../src/core/infrastructure/providers.py) | **commit** `fix(ids-jwt): validate Supabase ES256 via JWKS` |
| **Debug instrumentation** | `_debug_log` в `supabase_validator.py`; `#region agent log` в spa `identityService.js`, `useSessionShellState.js` | **удалить** перед commit |
| Builder task-артефакты | `docs/tasks/**` t08, bullrun, acceptance | по политике — отдельно, если оператор явно попросит |

### 6.3 Локальный `.env` identity (факты)

| Переменная | Значение на диске | Замечание |
|------------|-------------------|-----------|
| `SMS_PROVIDER` | `file` (строка 63; дубль mock на 25) | для ручного OTP через outbox |
| `SUPABASE_JWT_SECRET` | **не задан** | для HS256-пути; ES256 закрыт JWKS после §5.4 |
| `DB_BACKEND` | `supabase` | PostgREST к `ydocxoquirltrrfmvpqz.supabase.co` |

---

## 7. Рекомендации оператору (следующие шаги)

1. **Проверить** `#/verify` после reload identity с JWKS-фиксом — ожидается экран phone verification, не «Session Expired».
2. **Закоммитить** JWT-фикс; убрать debug logs из identity + spa.
3. **Опционально:** добавить `SUPABASE_JWT_SECRET` в `.env` (Dashboard → JWT Secret) — для HS256 sanity / live_integration; JWKS-путь покрывает ES256 Cloud.
4. **Ручной smoke file SMS:** runbook §1 + `tail -f var/sms-outbox/<номер>.log` после `POST /auth/phone/request`.
5. **Builder next (default):** EPIC-IDS-10 epic gate; SPIKE-PV-08 backlog-only ([`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) recommended next).

---

## 8. Индекс артефактов

| Тип | Путь |
|-----|------|
| Audit SSOT | [`epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md`](./epic-ids-10-pv-10-file-sms-sink-audit-2026-06-28.md) |
| P3 run-summary | [`run-summary-20260628-1747-epic-ids-10-pv-10-pkg-000041.md`](../tasks/run-reports/identity-build-windows/run-summary-20260628-1747-epic-ids-10-pv-10-pkg-000041.md) |
| P6 run-summary | [`run-summary-20260628-1811-epic-ids-10-pv-10-audit-override.md`](../tasks/run-reports/identity-build-windows/run-summary-20260628-1811-epic-ids-10-pv-10-audit-override.md) |
| Runbook | [`docs/runbook/sms-mock-testing.md`](../runbook/sms-mock-testing.md) |
| pkg-000041 | [`pkg-000041-20260628-epic-ids-10-pv-10-file-sms-sink-dev.yaml`](../tasks/identity-active-packages/pkg-000041-20260628-epic-ids-10-pv-10-file-sms-sink-dev.yaml) |
| t08 task | [`task-ids-10-10-t08-…/README.md`](../tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t08-audit-f1-pipeline-story-timestamp-example-sync/README.md) |
| spa smoke | [`spa-app/docs/runtime-docs/manual-smoke-phone-verification.md`](../../../spa-app/docs/runtime-docs/manual-smoke-phone-verification.md) |

---

## 9. Ограничения отчёта

- Не покрывает **spa-app** изменения вне инцидента §5 (scope identity microservice).
- Не включает **push** статус remote `dev`.
- **INFO-3** (SPIKE-08 vs epic status в bullrun) — сознательно out of scope PV-10; см. audit §2 INFO-3.

---

## 10. Жёсткая валидация JWT-фикса (архитектурная адекватность)

> Метод: [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — claims по фактическому коду `supabase_validator.py` (прочитан целиком), сверка с эталонным паттерном системы (OIDC `id_token.py` / `toolkit.py`), прогон сюиты.

### 10.1 Что сделано правильно (по сути решение адекватно)
- **Диагноз точный.** Supabase Cloud подписывает JWT асимметрично; старый валидатор знал только HS256 → `GET /me` 401. Добавление JWKS-пути — корректный механизм, а не обход симптома.
- **Переиспользован системный кэш.** `JwksCache` ([`jwks_cache.py:13-55`](../../src/core/security/oidc/jwks_cache.py)) — тот же, что у OIDC; не плодит параллельную инфраструктуру. ✅ (Knowledge Integration)
- **Паттерн refresh-on-unknown-kid** ([`supabase_validator.py:109-120`](../../src/core/auth/supabase_validator.py)) повторяет [`id_token.py:42-58`](../../src/core/security/oidc/id_token.py) — консистентно с ротацией ключей.
- **Выбор alg по header + строгая привязка ключа к пути** (HS256→`OctKey`; JWKS→asymmetric с `algorithms=[alg]`), `alg=none` отклоняется (тест [`:93-96`](../../tests/test_supabase_jwt_validator.py)) → классический alg-confusion в этом дизайне закрыт.
- **`aud="authenticated"` теперь валидируется** ([`:72-77`](../../src/core/auth/supabase_validator.py)) — закрывает прежний gap **G-5** аудита backend ([`identity-backend-full-audit-2026-06-24.md`](./identity-backend-full-audit-2026-06-24.md) §3).

### 10.2 Слабые места, костыли, нарушения паттернов

| ID | Severity | Проблема | Доказательство | Как закрыть |
|----|----------|----------|----------------|-------------|
| **W1** | 🔴 **HIGH (блокер коммита)** | **Debug-инструментация в проде на hot-path.** `_debug_log` пишет в **хардкод абсолютный путь** `/Users/eslinko/…/.cursor/debug-3c4b9a.log`, вызывается на **каждом** `validate()` (успех+ошибка) — т.е. на каждом авторизованном запросе. `run_id="post-fix"` зашит. | [`supabase_validator.py:20-44`](../../src/core/auth/supabase_validator.py) (def), [`:136-166`](../../src/core/auth/supabase_validator.py) (вызовы), [`:128`](../../src/core/auth/supabase_validator.py) | Удалить `_debug_log` и все вызовы до коммита. Нарушает гигиену, зеркальную spa [`STORY-SPA-SEC-03`](../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-03-remove-debug-instrumentation.md). Path Fragmentation anti-pattern. |
| **W2** | 🟠 MEDIUM | **Нарушение DI-паттерна + утечка `httpx.Client`.** Валидатор сам строит `JwksCache` **и** `httpx.Client` внутри `__init__`; `providers.py` http_client **не передаёт** → создаётся новый клиент, который **никогда не закрывается**. Эталон системы — инъекция: OIDC принимает `JwksCache` в конструктор, а кэш собирается из **общего** `self._http_client`. | валидатор: [`:78-82`](../../src/core/auth/supabase_validator.py); конструирование без client: [`providers.py:107-110`](../../src/core/infrastructure/providers.py); эталон DI: [`id_token.py:30-31`](../../src/core/security/oidc/id_token.py), [`toolkit.py:24`](../../src/core/security/oidc/toolkit.py) | Инъектировать `JwksCache`/общий `http_client` снаружи (как OIDC toolkit); снять двойную ответственность валидатора. |
| **W3** | 🟠 MEDIUM | **Magic-string эвристика `demo.local`.** JWKS включается по суффиксу URL-сентинела, который инжектится в **другом** файле (`"https://demo.local"`). Неявный контракт между двумя модулями через строку-маркер. | [`supabase_validator.py:79`](../../src/core/auth/supabase_validator.py); сентинел: [`providers.py:110`](../../src/core/infrastructure/providers.py) | Управлять явно — `APP_PROFILE`/факт наличия реального `supabase_url` в конфиге, не URL-сниффингом. |
| **W4** | 🟠 MEDIUM (для критичного пути — фактически HIGH) | **Новый JWKS/ES256-путь не покрыт тестами.** Все 9 тестов валидатора — **HS256**; `_validate_jwks`, refresh-on-kid, выбор alg по header — **0 тестов**. Именно то, что чинило инцидент, не защищено регрессом. «17 passed» в §5.4 — это HS256/auth-набор. | [`test_supabase_jwt_validator.py:45,126-142`](../../tests/test_supabase_jwt_validator.py) (везде `alg:HS256`); grep `ES256/RS256/jwks` по тестам → пусто | Оффлайн-тест с мок-JWKS (ES256-ключ, мок `httpx`): success; unknown-kid→refresh→success; alg вне whitelist→reject; `_jwks_cache is None`→ понятная ошибка. |
| **W5** | 🟡 LOW-MEDIUM (security-note) | **HS256 demo-fallback секрет — вектор подделки.** При незаданном `SUPABASE_JWT_SECRET` (по §6.3 — текущий `.env`) валидатор принимает HS256-токены, подписанные **публично известной** строкой `"test-secret-for-demo"` → подделка `authenticated`-токена возможна (alg=HS256). Pre-existing demo-дизайн (pilot требует секрет — fail-fast), но при demo против **реального** Cloud-проекта путь открыт. | [`providers.py:108`](../../src/core/infrastructure/providers.py); HS256-ветка [`supabase_validator.py:100-102,130-131`](../../src/core/auth/supabase_validator.py); pilot-required: [`schema.py:185+`](../../src/core/config/schema.py) | Не принимать HS256 c fallback-секретом, когда `supabase_url` реальный; либо требовать секрет при реальном URL даже в demo. |
| **W6** | 🟢 LOW | Мелочи: `run_id="post-fix"` (мёртвый scaffold); широкий `except Exception` ([`:168`](../../src/core/auth/supabase_validator.py)) маскирует прочие ошибки в `JwtValidationError`; helper `resolve_key_set_for_kid` ([`jwks_cache.py:47-55`](../../src/core/security/oidc/jwks_cache.py)) не используется (но и `id_token.py` дублирует цикл — т.е. консистентно с ним). | — | Чистка вместе с W1; широкий catch оставить осознанно или сузить. |

### 10.3 Консистентность с паттернами — сводка
| Аспект | Вердикт |
|--------|---------|
| Переиспользование `JwksCache` | ✅ как OIDC |
| refresh-on-unknown-kid | ✅ как `id_token.py` |
| `aud`-валидация (закрывает G-5) | ✅ улучшение |
| DI `JwksCache`/`http_client` | ❌ расходится с OIDC toolkit (W2) |
| Управление режимом (profile vs `demo.local`) | ❌ magic-string (W3) |
| Гигиена (no debug в проде) | ❌ нарушено (W1) |
| Тест-покрытие нового пути | ❌ отсутствует (W4) |

### 10.4 Резюме / вердикт (кратко)

> 📌 **Доводка оформлена стори:** [`STORY-IDS-SEC-06`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) (пакет security-hardening) — закрывает W1–W6: код, тесты, документация.

**По сути решение верное** — диагноз ES256 точный, JWKS-механизм правильный, переиспользует наш кэш и паттерн ротации ключей; вдобавок закрыл прежний gap по `aud`. **Но коммитить в текущем виде нельзя.**

**Нужно дорабатывать — да.** Минимально перед коммитом:
1. **W1 (🔴):** убрать `_debug_log` целиком — это блокер (хардкод-путь + I/O на каждом auth-запросе).
2. **W4 (🟠→HIGH для критичного пути):** добавить оффлайн-тесты JWKS/ES256 — иначе фикс не защищён регрессом.

Желательно сразу (дёшево, повышает консистентность):
3. **W2/W3:** привести к нашему DI-паттерну (инъекция `JwksCache`/`http_client`) и заменить `demo.local`-эвристику явным конфигом; заодно чинит утечку `httpx.Client`.

Отдельным решением:
4. **W5:** политика demo-fallback секрета при реальном `supabase_url` (security).

Регрессий нет (offline-сюита **394 passed**), но «зелёная сюита» здесь не доказывает корректность ES256-пути — он просто не тестируется (W4).
