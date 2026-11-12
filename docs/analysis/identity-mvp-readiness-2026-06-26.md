# Оценка фактической готовности identity к MVP (GPT-submit + web-signup)

> **Дата:** 2026-06-26
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`; готовность = по фактическому коду, не по докам.
> **Якорь флоу:** [`04-security.md`](../runtime-docs/04-security.md) (целевой процесс + as-is).
> **MVP-scope (запрос):** (A) подача истории из Custom GPT; (B) полный signup через веб-аппку + redirect.
> **База регрессий:** **386 passed, 12 deselected** (offline).

## TL;DR — вердикт

| Слой | Готовность | Комментарий |
|------|-----------|-------------|
| **identity-backend** | **≈ 95% — MVP-ready** | весь критичный путь обоих флоу построен и протестирован; единственный identity-остаток — `ONB-01` (email в `/me`), не блокер |
| Внешнее/ops | ⚠️ требует настройки | реальные secrets, ChatGPT OAuth-регистрация, Telnyx-аккаунт, Supabase-проект, `DB_BACKEND=supabase`, деплой |
| Frontend (spa-app) | ⛔ вне репо | `/login` (OAuth-handshake), `/verify` (inline phone OTP), disclosure-копирайт |
| Gateway | ⛔ вне репо | вызов introspection + enforcement `verification_required` на submit |
| eID | 🟦 post-MVP | заменён телефоном; не блокирует MVP |

**Итог:** на стороне **identity-сервиса MVP практически готов** — оба флоу замкнуты в коде. «Запуститься» мешает не identity-бэкенд, а **склейка компонентов** (spa-app страницы, gateway-enforcement) и **операционная настройка** (secrets/аккаунты/durable backend).

---

## A. Флоу «подача истории из GPT» — по шагам vs код

| Шаг (04-security §A) | Код | Готовность |
|----------------------|-----|------------|
| GPT (OAuth-клиент) без токена → `/oauth/authorize` (PKCE S256, client_id/redirect/scope/state) | [`handlers.py:22-99`](../../src/core/oauth/handlers.py), [`asgi_app.py:370`](../../src/core/api/asgi_app.py) | ✅ |
| authorize → redirect на `<spa>/login?oauth_request_id=…` | [`build_spa_oauth_login_url`](../../src/core/oauth/spa_login.py) (base = первый `CORS_ALLOWED_ORIGINS`) | ✅ identity-side; **spa `/login` — frontend** |
| Вход (Supabase Auth) → `/oauth/authorize/complete` (Bearer JWT) → выдаёт code | [`handlers.py:102-153`](../../src/core/oauth/handlers.py) | ✅ |
| **verify-gate:** если `requested_action=stories:submit` и `phone_verified=false` → 403 `verification_required`+`verify_url` (до выдачи code) | [`handlers.py:126-137`](../../src/core/oauth/handlers.py), [`verification_required.py`](../../src/core/oauth/verification_required.py) (OAUTH-04 🟢) | ✅ |
| `/oauth/token` (code → access-token; PKCE verify; `client_secret` enforced; reuse → `invalid_grant`) | [`handlers.py:156-163`](../../src/core/oauth/handlers.py), [`verify_client_secret`](../../src/core/oauth/client_secret.py) | ✅ |
| GPT → gateway (история); gateway → `/oauth/introspect` (service-token) → `{active, sub, phone_verified}` | [`introspection.py`](../../src/core/oauth/introspection.py), [`asgi_app.py:407`](../../src/core/api/asgi_app.py) + `require_service_token` (OAUTH-02 🟢) | ✅ identity-side; **enforcement — gateway** |
| Сервисный слой доверия (`SERVICE_API_TOKEN`, обязателен в pilot) | [`ServiceTokenAuth` security.py:89-116](../../src/core/api/security.py), fail-fast [`schema.py`](../../src/core/config/schema.py) | ✅ |
| Durable handshake/codes (переживают редеплой) | `SupabaseOAuthTokenService`/`SupabaseAuthorizationRequestStore` при `DB_BACKEND=supabase` (OAUTH-03 🟢) | ✅ при supabase; ⚠️ in-memory по умолчанию |

**Identity-side флоу A — построен полностью.** GPT-client регистрируется из конфига (`GPT_OAUTH_CLIENT_ID` default `openai-custom-gpt`, `GPT_OAUTH_CLIENT_SECRET` pilot-required, [`schema.py:223-224`](../../src/core/config/schema.py)).

---

## B. Флоу «web signup + redirect» — по шагам vs код

| Шаг | Код | Готовность |
|-----|-----|------------|
| Email-signup через Supabase Auth | — (делает **spa-app** + Supabase) | ✅ вне identity |
| Проверка пользовательского токена (Bearer Supabase JWT; iss/aud/sub/exp/role) | [`supabase_validator.py:12-46`](../../src/core/auth/supabase_validator.py) (SEC-03: `aud` ✅) | ✅ |
| `GET /me` (профиль + `phone_verified`) | [`me_response.py`](../../src/core/api/me_response.py), AUTHCORE-01 | ✅ |
| **Ленивый гейт телефона** (consumer читает `phone_verified`, иначе verify) | контракт [`09:28`](../runtime-docs/09-gateway-expectations.md) + [`08-ui §3b`](../runtime-docs/08-ui-expectations.md) (DOC-ONB-01 🟢) | ✅ контракт; **экран — frontend** |
| Inline phone-verify: `/auth/phone/request` → SMS-OTP → `/auth/phone/confirm` (+372, 6-значный, TTL 300s, 5 попыток) | [`asgi_app.py:322,338`](../../src/core/api/asgi_app.py), `core/phone/` (PV-01…07) | ✅ |
| Один номер = один аккаунт (409 `profile_conflict`) | `phone_one_account_per_number` + unique index | ✅ |
| Telnyx SMS + delivery webhook (Ed25519) | `phone/telnyx/`, `/webhooks/telnyx/messaging` (PV-06/07) | ✅ код; **аккаунт — SPIKE-PV-08** |
| `email` в `/me` (+ нота Supabase «Confirm email») | **отсутствует** ([`me_response.py`](../../src/core/api/me_response.py) — 0 упоминаний email) | ⚪ **ONB-01 — единственный identity-остаток** |
| eID-redirect-модель (`return_url` → 303 callback) | [`eid_callback.py`](../../src/core/api/eid_callback.py) | 🟦 post-MVP (mock; реальный провайдер отложен) |

**Identity-side флоу B — построен;** единственный недостающий бэкенд-кусок — `email` в `/me` (ONB-01), и он **не критичен** (signup делает Supabase; `email` в `/me` — удобство).

---

## Кросс-режимная безопасность (по 04-security §B) — всё ✅

- Supabase-JWT (HS256, `aud=authenticated` — SEC-03) · Bearer-gate · OAuth-движок (PKCE/client_secret) · HMAC-хэш PII · RLS · CORS · **rate-limit 429** на `/auth/eid/start`+`/callback`+`/auth/phone/request` (SEC-01/01b, XFF-spoof закрыт) · **аудит с хэш IP/UA** (SEC-02) · pilot fail-fast секретов. Регрессий нет (386 passed).

---

## Что мешает MVP (категоризировано)

### 1. Identity-backend (в этом репо) — почти ничего
- **ONB-01** (⚪ LOW): `email` в `/me` + нота «Confirm email» в runbook. **Не блокер** для подачи историй/верификации; нужен, если фронту требуется email в профиле.

### 2. Конфиг/ops (внешнее — обязательно для боевого запуска)
- **Реальные secrets** (pilot fail-fast их требует): `SUPABASE_*`, `DATABASE_URL`, `OAUTH_ACCESS_TOKEN_SECRET`, `GPT_OAUTH_CLIENT_SECRET`, `SERVICE_API_TOKEN`, `DOGESTONIA_EID_SECRET`, `EID_SESSION_ENC_KEY`, `API_BASE_URL` ([`schema.py:174-187`](../../src/core/config/schema.py)).
- **`DB_BACKEND=supabase`** — иначе OAuth-handshake/codes и phone-сессии in-memory (теряются на редеплое). ⚠️ см. F1.
- **ChatGPT Custom GPT OAuth-регистрация** — `client_id`/`secret`/`redirect_uri` должны совпасть с identity-конфигом и реестром клиента.
- **Telnyx-аккаунт + sender** (SPIKE-PV-08) — гейтит реальную отправку SMS.
- **Supabase-проект identity** + накат `000_full_init.sql` (8/8: profiles/eid/oauth/phone — паритет есть, PV-09).

### 3. Frontend (spa-app — отдельный репо)
- `/login` — страница входа, завершает OAuth-handshake (`oauth_request_id` → `/oauth/authorize/complete`).
- `/verify` — inline phone-OTP экран (`/auth/phone/request` → `/confirm`) + ленивый гейт по защищённому действию.
- disclosure-копирайт (DOC-ONB-02), non-EE waitlist (DOC-ONB-04).

### 4. Gateway (doge-complaints-gateway — отдельный репо)
- Вызов `/oauth/introspect` (service-token) + enforcement `verification_required` (403) на `POST` истории. В 04-security §A: «gateway intake ещё не подключён». Контракт со стороны identity готов ([`09-gateway-expectations`](../runtime-docs/09-gateway-expectations.md)); под это есть пакет требований `gpt-submit-authz` в репо gateway.

### 5. eID — 🟦 post-MVP
- Реальный Authentigate (EID-02/09…14) — ждёт донейшнов на оплату SK. Телефон закрывает MVP-потребность «реальный уникальный человек». **Не блокер.**

---

## Findings (severity + как закрыть)

| ID | Severity | Суть | Как закрыть |
|----|----------|------|-------------|
| **F1** | **MEDIUM** (ops) | `DB_BACKEND` дефолт `in_memory` и **не** в pilot fail-fast ([`schema.py:145`](../../src/core/config/schema.py)) → боевой `APP_PROFILE=pilot` может стартовать с in-memory OAuth/phone-сторами (теряются на редеплое; multi-replica не работает). | Добавить `DB_BACKEND=supabase` в pilot-инвариант ИЛИ зафиксировать в runbook как обязательный для прод-деплоя |
| **F2** | LOW (doc) | [`04-security.md:68,92`](../runtime-docs/04-security.md) as-is-врезка/таблица всё ещё пишут «Оставшийся разрыв: verify-gate (OAUTH-04)» / «⚪ relay через OAuth» — OAUTH-04 уже 🟢 Done. | Снять «остаток verify-gate»: пометить OAUTH-04 ✅ |
| **F3** | LOW | `ONB-01` (email в `/me`) — не сделано; единственный identity-backend остаток. | Реализовать или явно отложить (не критично для MVP-флоу) |
| **F4** | none (cleanup) | Осиротевшие стабы `_not_implemented` ([`handlers.py:647,768`](../../src/core/api/handlers.py)) — **не вызываются из роутов** (проверено grep'ом), наследие. | Удалить при CLEANUP (не влияет на MVP) |

---

## Итог: что нужно, чтобы «поехало»

**Identity-сервис готов под оба MVP-флоу** (≈95%): OAuth-сервер (authorize/complete/token/introspect + verify-gate), phone-верификация, `/me`, rate-limit, аудит, durable-стор — построены и протестированы (386 offline). 

**Чтобы запустить MVP**, нужно (вне identity-бэкенда):
1. **Ops:** реальные secrets + `DB_BACKEND=supabase` + Supabase-проект + деплой (F1).
2. **ChatGPT:** зарегистрировать Custom GPT как OAuth-клиента (redirect/creds ↔ identity-конфиг).
3. **Telnyx:** аккаунт + sender (SPIKE-PV-08) для реальных SMS.
4. **spa-app:** страницы `/login` и `/verify` (identity отдаёт redirect/API, экраны — фронт).
5. **gateway:** подключить introspection + enforcement `verification_required` на submit.

**Опционально/не блокер:** ONB-01 (email в /me); eID — post-MVP.

## Quality gate (analysis.mdc)
- [x] Готовность по фактическому коду с `file:line`; оба флоу прослежены end-to-end.
- [x] Разделено: identity-backend (готово) vs frontend/gateway/ops (вне репо) vs post-MVP (eID).
- [x] Конфиг-инварианты проверены (pilot fail-fast, DB_BACKEND default) → F1.
- [x] Doc-drift в 04-security (verify-gate) зафиксирован (F2); стабы вне живого пути (F4).
- [x] Регрессии: 386 passed — база актуальна.
