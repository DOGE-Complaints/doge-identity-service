# Жёсткий аудит backend identity vs спеки (requirements / tech-requirements / runtime-docs / docs/Identity)

> **Дата:** 2026-06-24
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity. Жёсткие расхождения вынесены в интерактивное интервью (решения зафиксированы ниже).
> **Объём:** 19 requirements + 7 tech-requirements + 10 runtime-docs + 7 docs/Identity vs ~70 src-файлов, 13 роутов, 56 тест-файлов.
> **Метод исполнения:** 6 параллельных доменных срезов (A–F), каждый код-grounded; OAuth (E) опирается на 4 предыдущих аудита OAUTH-01..04.
> **Сюита:** **366 passed, 11 deselected** (offline) — базовая линия регрессий.

---

## 0. Решения оператора (интервью 2026-06-24)

| # | Расхождение | Решение |
|---|-------------|---------|
| Q1 | requirements 06–09 + все impl-epic — gateway-копипаст; phone-механизм без спека | **Авторизовать недостающее + актуализировать identity-релевантные** (новый phone-спек; 08/09/10/11/13/15 под факт; gateway-копии — reference-only баннер) |
| Q2 | code-гэпы G-1/2/3 (rate-limit, durable аудит+IP/UA, durable phone-сессии) | **Только отчёт + severity**, сборку решаем позже |
| Q3 | `/me` shape vs спек 10 | **Код — истина**, спек 10 → факт |
| Q4 | verified-person-hash vs спек 13 | **Код — истина**, спек 13 → as-built |

---

## 1. 🔴 Системные расхождения

### HD-1 — requirements 06–09 + ВСЕ `impl-epic-01..05` скопированы из doge-complaints-gateway
Спеки описывают **другой сервис**: мандатят `/intake/stories`, `/tallinn/issues`, `/protected/status`, `/metrics`, таблицы `stories`/`idempotency_keys`/`cluster_memberships`/`doge_issues`/`story_embeddings`, `pyproject name="doge-complaints-gateway"` ([impl-epic-01:80]), `ServiceTokenAuth` как основную авторизацию, `CLUSTER_*`-конфиг, `StoryRepository`/`IssueProjectionReadStore`-протоколы. В identity **ничего этого нет** (роуты `/me`/`/auth/*`/`/oauth/*`; `BearerTokenAuth`/Supabase-JWT; `ProfileRepository`/`VerificationSessionStore`/OAuth/eID/phone-протоколы; 3 identity-таблицы). Подтверждено срезами A и B независимо.
- **impl-epic-05 Story 4** (стр.417-531) — verbatim gateway-схема (`stories`, `doge_issues`, …); реальный [`supabase/bootstrap/000_full_init.sql`](../../supabase/bootstrap/000_full_init.sql) создаёт `profiles`/`eid_verification_sessions`/`eid_audit_events`.
- **req-06/07** AppConfig не содержит eID-Easy, phone, `NODE_ID`, `DB_BACKEND`, `SERVICE_API_TOKEN` (всё есть в [`schema.py`](../../src/core/config/schema.py)).
- **Решение Q1 → действие:** на `06`, `07`, `impl-epic-01..06` — баннер «reference-only: скопировано из gateway, не отражает identity; SSOT кода — `src/`».

### HD-2 — phone-верификация (АКТИВНЫЙ гейт) не имеет спека в `docs/requirements`
`grep -riE "phone|sms|otp|telnyx" docs/requirements/` → 1 случайное упоминание ([09:61](../requirements/09-supabase-jwt-validation.md)). Весь набор 01–18 — eID-эра. Активный механизм (`phone_verified`) специфицирован только в [`docs/analysis/phone-verification-architecture-2026-06-10.md`](./phone-verification-architecture-2026-06-10.md). Построено: [`src/core/phone/`](../../src/core/phone/) (12 файлов), роуты [`asgi_app.py:322,338,355`](../../src/core/api/asgi_app.py), 10 тест-файлов.
- **Решение Q1 → действие:** создать numbered `docs/requirements/19-phone-verification-flow.md` из кода + проиндексировать.

### HD-3 — статус-заголовки «НЕ реализовано» при построенном коде
[`08-supabase-migrations.md:3`](../requirements/08-supabase-migrations.md) и [`09-supabase-jwt-validation.md:3`](../requirements/09-supabase-jwt-validation.md) = «> Статус: НЕ реализовано», хотя 8 миграций + валидатор + security построены и протестированы.
- **Решение Q1 → действие:** заголовки → «реализовано»; в 08 добавить phone + OAuth-миграции.

---

## 2. 🔴 Контрактные расхождения (решены: код = истина)

### HD-4 — `/me` shape vs спек 10 (Q3: код-истина)
Код [`me_response.py:19-46`](../../src/core/api/me_response.py): `{supabase_user_id, eid_verified, role, display_name, avatar_url, eid_provider, eid_method, eid_country, eid_verified_at, phone_verified, phone_provider, phone_dial_prefix, phone_verified_at}`.
Спек 10 (стр.93-106): `{user_id, display_name, avatar_url, eid_verified, eid_country, eid_method, eid_verified_at, wallet_linked, permissions, created_at}`.
- В коде **нет**: `user_id`(назван `supabase_user_id`), `permissions[]`, `wallet_linked`, `created_at`.
- Авто-provision профиля при первом `/me` — **не делается** ([handlers.py:85-87](../../src/core/api/handlers.py) синтетический 200 без записи; тест `test_me_profile.py:146-166` фиксирует «no upsert on GET /me» — решение t01).
- **Действие:** спек 10 → фактический shape + «no-auto-provision» + phone-поля; `permissions`/`wallet_linked`/`created_at` снять (или вынести как future).

### HD-5 — verified-person-hash vs спек 13 (Q4: код-истина)
Спек 13 (стр.27,42): `HMAC(secret, "{country}:{personal_code}")`. Код [`handlers.py:378-381`](../../src/core/api/handlers.py): `hash_secret(f"{country}:{subject_hash}", key=eid_secret)`, где `subject_hash` — провайдер-агностичный (ревизия ADR-IDS-008). Статус конфликта: код `profile_conflict`/409 ([handlers.py:392-411](../../src/core/api/handlers.py)), спек — `identity_already_linked`.
- **Действие:** спек 13 → two-stage `subject_hash`→`verified_person_hash`, `profile_conflict`/409, + ветка phone-hash; старая `personal_code`-формула obsolete.

---

## 3. 🟠 Реальные code-гэпы (Q2: только отчёт + severity; сборку решаем позже)

| ID | Severity | Гэп | Доказательство | Как закрыть |
|----|----------|-----|----------------|-------------|
| **G-1** | HIGH | Нет rate-limiting нигде. Спек 11:126-128 (eID-start 5/10мин→429), спек 16:31-53 `RATE_LIMITS`+429. Есть только OTP-cooldown. | grep `429/retry_after/RateLimit` по `src/core/` → только `telnyx/errors.py`; [handlers.py:458-473](../../src/core/api/handlers.py) cooldown | per-user rate-limiter ИЛИ пометить спек RATE_LIMITS как DEFERRED |
| **G-2** | HIGH | Аудит телефона — in-memory; нет таблицы `phone_audit_events`; IP/UA не хешируются. Спек 16:105,144-159 + AC требуют durable + hashed IP/UA. | [`InMemoryPhoneAuditLogRepository` repositories.py:362](../../src/core/infrastructure/repositories.py); eID-аудит хардкодит `ip_hash=None` [handlers.py:162-163](../../src/core/api/handlers.py); миграции `phone_audit_events` нет | Supabase phone-audit + миграция; пробросить IP/UA в `_log_*_audit` ИЛИ задокументировать demo-only |
| **G-3** | MEDIUM | Phone-сессии (ожидание OTP) — in-memory only; рестарт теряет (в отличие от OAUTH-03 durable). | [`InMemoryPhoneVerificationSessionStore` repositories.py:284](../../src/core/infrastructure/repositories.py), [providers.py:121](../../src/core/infrastructure/providers.py); в `db_supabase.py` нет phone-session стора | Supabase phone-session стор при `DB_BACKEND=supabase` ИЛИ зафиксировать в 04-security |
| **G-4** | LOW (eID deferred) | `CODE_VERIFIER_ENCRYPTION_KEY`(спек 07/11/12/16) ≠ `EID_SESSION_ENC_KEY`(код); Fernet ≠ AES-GCM(спек). Используется только отложенным eID. | [schema.py:156](../../src/core/config/schema.py); [`FernetSessionSecretBox` session_secret.py:28-45](../../src/core/security/session_secret.py) | подтвердить ADR-переименование, обновить спеки ИЛИ при EID-02 |
| **G-5** | LOW | JWT `aud=authenticated` не валидируется (спек 09:42 требует); форма импорта ключа `OctKey.import_key(raw)` vs b64url(спек 09:97). Сюита зелёная → реальный секрет, видимо, raw. | [supabase_validator.py:17-22](../../src/core/auth/supabase_validator.py) | добавить `aud` в registry ИЛИ отметить в 09 как намеренно; сверить импорт ключа на живом токене |

---

## 4. 📝 Doc-stale (код — истина; правится без решения — Q1 «актуализировать»)

| Док | Стале́ть | Действие |
|-----|---------|----------|
| [`runtime-docs/01-api.md`](../runtime-docs/01-api.md) | нет роутов `/auth/phone/*`, `/webhooks/telnyx/*`; OAuth помечен «501» (построен); line-анкеры устарели (`/health`:145 vs :257 и т.д.) | добавить роуты, снять «501», обновить анкеры |
| [`runtime-docs/04-security.md`](../runtime-docs/04-security.md) | line-анкеры | освежить (низкий) |
| [`runtime-docs/08-ui-expectations.md`](../runtime-docs/08-ui-expectations.md) | только eID-redirect; нет активного phone inline-verify | добавить phone inline-UX |
| `requirements/11,12,17,18` | отстали от descriptor-рефактора eID; redirect-маркеры (`?eid_status=` vs `?context=`); subject_hash | баннер «eID DEFERRED + код ушёл вперёд», точечно |
| [`../docs/Identity/identity-backend.md`](../../../docs/Identity/identity-backend.md) | FR-BE-010 ещё eID (`/auth/eid/start`, `eid_verified`, `identity_already_linked`); шапка «OAuth 501» | синхронизировать с 04-security/09 (OAuth built; phone-gate; `profile_conflict`) |
| [`../docs/Identity/identity-overview.md`](../../../docs/Identity/identity-overview.md) | «OAuth /oauth/* 501» | OAuth built |
| `runtime-docs/06-eid-providers.md`, `07-web3-foundation.md` | актуальны (06 описывает текущий код; 07 само-флагнут «заготовка») | без действий |

**Доменные ⏸️ deferred (by design, не gap):** Authentigate OIDC-клиент + PKCE и eID-Easy provider — descriptor-заглушки `build()→ProviderNotRegisteredError (STORY-IDS-EID-02)`; OIDC-примитивы (discovery/JWKS/RS256 id_token) построены и протестированы, но не подключены к живому провайдеру.

---

## 5. ✅ Что подтверждено верным (no action)
- Envelope (`{data}` / `{error:{code,message,trace_id}}`) — точное совпадение с 01-api/epic-02 ([envelope.py](../../src/core/api/envelope.py)).
- DI/SOA: `ApiDependencies(frozen)` + `@lru_cache(1)` + backend-switch с `ValueError` fail-fast — совпадает с 03-soa-roles ([providers.py:62-89](../../src/core/infrastructure/providers.py)).
- Supabase JWT: HS256/joserfc, `iss/sub/exp` essential, `role=authenticated`, only-HS256 — совпадает с 09 (кроме `aud` G-5).
- 3 identity-таблицы + RLS + индексы — все имеют реальные миграции (срез B).
- OAuth-сервер (OAUTH-01..04) — построен и протестирован; introspection `{active,sub,phone_verified}`; verify-gate `verification_required` (403); см. отдельные аудиты `epic-ids-11-oauth-0{1..4}-*`.
- Phone-крипто: HMAC-SHA256 (`hashing.py:9`), сырой телефон не хранится (только `phone_hash`/`verified_phone_hash`); OTP 6-значный, TTL 300s, 5 попыток, `secrets.choice`, `hmac.compare_digest`; Telnyx Ed25519-подпись fail-closed. (Срез F.)

---

## 6. Регрессии
**366 passed, 11 deselected** — изменения этого аудита **doc-only** (код не трогаем по Q2). Регрессий нет и не ожидается.

---

## 7. Addendum (2026-06-26): G-1 после SEC-01 / pkg-000035

| Состояние G-1 | Роуты | Доказательство |
|---------------|-------|----------------|
| **Закрыто** | `POST /auth/eid/start`, `GET /auth/{provider}/callback` | [`rate_limit_dependency.py`](../../src/core/api/rate_limit_dependency.py), [`asgi_app.py:283-342`](../../src/core/api/asgi_app.py) |
| **Остаток (follow-up)** | `POST /auth/phone/request` | Нет `Depends(rate_limit)` — [`asgi_app.py:344-358`](../../src/core/api/asgi_app.py); только OTP cooldown [`handlers.py:456-473`](../../src/core/api/handlers.py) |

**SSOT решения и требований к отдельной стори:** [`sec-01-g1-rate-limit-split-2026-06-26.md`](./sec-01-g1-rate-limit-split-2026-06-26.md) · backlog [`STORY-IDS-SEC-01b`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md).

**Offline suite post-SEC-01:** 369 passed (`pytest -m "not live_integration"`).

## 7. Что актуализируется (план doc-правок по решениям)
1. **Q3:** `requirements/10-me-endpoint.md` → фактический `/me` + no-auto-provision.
2. **Q4:** `requirements/13-verified-person-hash-and-conflict.md` → subject_hash + `profile_conflict`/409 + phone-ветка.
3. **Q1:** создать `requirements/19-phone-verification-flow.md` + индекс; статус-заголовки 08/09 → «реализовано» (+ phone/OAuth-миграции в 08); баннеры eID-deferred на 11; story-authz 15 → built; reference-only баннеры на 06/07 + impl-epic-01..06; runtime-docs 01-api/08-ui + docs/Identity (backend/overview) синхронизация.
4. **Q2:** G-1..G-5 — только этот отчёт (severity зафиксирован).

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 6 доменных срезов, каждый код-grounded.
- [x] Жёсткие расхождения вынесены в интервью; решения зафиксированы (§0).
- [x] Doc-stale отделён от code-gap; deferred-by-design (eID) отделён от gap.
- [x] Регрессий нет (366 passed, doc-only).
- [x] Spec→code и code→spec (поля schema/роуты/миграции, отсутствующие в спеке) проверены в обе стороны.
