# EPIC-IDS-11 — OAuth-сервер для GPT + межсервисная валидация

> **ID:** `EPIC-IDS-11` · **Alias (код/backlog):** `EPIC-IDS-OAUTH` · **Статус:** 🟡 In Progress · **Тип:** Функциональный
> **Source (backlog):** [`backlog-stories/oauth/EPIC-IDS-OAUTH.md`](../../backlog-stories/oauth/EPIC-IDS-OAUTH.md)
> **Продуктовый зонтик:** [`EPIC-IDS-ONBOARDING`](../../backlog-stories/identity-onboarding/EPIC-IDS-ONBOARDING.md) — вход #2 (редирект из кастомного GPT).

## Назначение
Подключить identity как **OAuth 2.0 сервер** для Custom GPT: выдать authorization code, обменять на access-токен, затем дать gateway межсервисную валидацию (introspection + сервисный токен). **OAUTH-01**, **OAUTH-02** и **OAUTH-03** построены ([`core/oauth/`](../../../src/core/oauth/), `POST /oauth/introspect`, durable Supabase-стор); следующий шаг — OAUTH-04.

## Контекст
- Источник: backlog [`identity-todo-backlog-2026-06-04`](../../../analysis/identity-todo-backlog-2026-06-04.md) (A4/C7/C8/B5/B6; gaps SEC-1, API-1, CFG-1).
- Целевой UX входа из GPT: [`identity-onboarding-ux-2026-06-12`](../../../analysis/identity-onboarding-ux-2026-06-12.md) (gap G1).
- Pre-audit: [`oauth-validation-2026-06-12.md`](../../../analysis/oauth-validation-2026-06-12.md).

## Stories
| Story | Тема | Слой | Статус |
|-------|------|------|--------|
| [STORY-IDS-OAUTH-01](stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) | OAuth-сервер наружу (`/oauth/*` → движок, PKCE, client_secret) | код | 🟢 Done |
| [STORY-IDS-OAUTH-02](stories/STORY-IDS-OAUTH-02-introspection-and-service-token/STORY-IDS-OAUTH-02-introspection-and-service-token.md) | introspection + сервисный токен (склейка с gateway) | код | 🟢 Done |
| [STORY-IDS-OAUTH-03](stories/STORY-IDS-OAUTH-03-persistent-token-store-supabase/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) | durable стор codes/handshake в Supabase Postgres | код/данные | 🟢 Done |
| [STORY-IDS-OAUTH-04](stories/STORY-IDS-OAUTH-04-verify-gate-and-verification-required/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) | verify-gate в OAuth-флоу: relay `requested_action` + канон `verification_required` (phone) | код/контракт | 🟢 Done |

## Документация
- [PLAN-IDS-OAUTH-docs-actualization](../../backlog-stories/oauth/PLAN-IDS-OAUTH-docs-actualization.md) — **🟢 Выполнен 2026-06-24** (`04-security §A`, `09-gateway-expectations`).

## Порядок реализации
**Код:** **OAUTH-01** (снять 501-заглушки, подключить движок, `client_secret`) → **OAUTH-03** (durable Supabase-стор codes/handshake) → **OAUTH-02** (introspection + сервисный токен; отдаёт **`phone_verified`**) → **OAUTH-04** (relay verify-need + канон `verification_required` — замыкает «submit-после-авторизации» под phone).

> **Phone-pivot:** активный гейт — `phone_verified` (eID отложен). Introspection/verify-контракт — под телефон.

> **Почему не Supabase-OAuth-сервер:** ADR-IDS-002 отклонил Supabase OAuth 2.1 Server (меньше контроля над claims/scope); Supabase используется только как Postgres-персистентность (OAUTH-03), сервер — наш. Access-токены — stateless HS256, редеплой их не ломает.

## Связь
Зонтик: [`EPIC-IDS-ONBOARDING`](../../backlog-stories/identity-onboarding/EPIC-IDS-ONBOARDING.md). Парадигма: [`04-security`](../../../runtime-docs/04-security.md), [`09-gateway-expectations`](../../../runtime-docs/09-gateway-expectations.md).

### Story 1: STORY-IDS-OAUTH-01 — OAuth 2.0 сервер наружу — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](./stories/STORY-IDS-OAUTH-01-oauth-server-endpoints/STORY-IDS-OAUTH-01-oauth-server-endpoints.md)
- **Source (backlog):** [`backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md)

**Acceptance Criteria:**
- [x] `/oauth/authorize` (с валидным Supabase JWT) выдаёт authorization code привязанный к `supabase_user_id`.
- [x] `/oauth/token` обменивает валидный code на access-токен; повторный обмен/просрочка → `invalid_grant`.
- [x] Неверный `client_secret` → отказ (в прод-пути проверка включена).
- [x] PKCE: запрос с `code_challenge` требует корректный `code_verifier`.
- [x] `/oauth/authorize`: незарегистрированный `client_id` → `invalid_client`; неверный `redirect_uri` → `invalid_redirect_uri` (напрямую, не redirect); неверный scope → `invalid_scope`; `state` пробрасывается.
- [x] `authorization_request`-store: `/oauth/authorize` → redirect в spa-login с `oauth_request_id`; `/oauth/authorize/complete` (Bearer Supabase JWT) → code + redirect в ChatGPT.
- [x] Ошибки в формате RFC 6749 (`{error, error_description}`); scope-модель валидируется.
- [x] Покрыто тестами (offline).

### Story 2: STORY-IDS-OAUTH-02 — introspection + сервисный токен — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-OAUTH-02-introspection-and-service-token/STORY-IDS-OAUTH-02-introspection-and-service-token.md`](./stories/STORY-IDS-OAUTH-02-introspection-and-service-token/STORY-IDS-OAUTH-02-introspection-and-service-token.md)
- **Source (backlog):** [`backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md)

**Acceptance Criteria:**
- [x] introspection с валидным токеном → `{active:true, sub, phone_verified}`; с просроченным/битым → `{active:false}`.
- [x] Запрос без валидного сервисного токена → 401/403 (даже с валидным пользовательским токеном).
- [x] `phone_verified` берётся из профиля, не из тела токена.
- [x] Покрыто тестами (offline) + зафиксирован контракт ответа для gateway.

### Story 3: STORY-IDS-OAUTH-03 — durable Supabase OAuth store — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-OAUTH-03-persistent-token-store-supabase/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](./stories/STORY-IDS-OAUTH-03-persistent-token-store-supabase/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md)
- **Source (backlog):** [`backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md)
- **Wave:** pkg-000033 (359 pytest offline, 2026-06-24)

**Acceptance Criteria:**
- [x] Миграция создаёт `oauth_authorization_requests` + `oauth_authorization_codes` (TTL-индекс, single-use).
- [x] `SupabaseOAuthTokenService` реализует контракт `OAuthTokenService` + хранение request-state; single-use/TTL в БД.
- [x] `DB_BACKEND=supabase` → используется Supabase-стор; `in_memory` → прежний (тесты зелёные).
- [x] **Durability-тест:** code/request, «выданный» до пересоздания стора, валиден после (эмуляция редеплоя); просроченный/использованный → `invalid_grant`.
- [x] Access-токен валиден после пересоздания стора **без** обращения к БД (stateless подтверждён тестом).
- [x] Offline-тесты (mock PostgREST) зелёные; миграция — в `test_supabase_migrations_sql`.

### Story 4: STORY-IDS-OAUTH-04 — verify-gate + `verification_required` — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-OAUTH-04-verify-gate-and-verification-required/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](./stories/STORY-IDS-OAUTH-04-verify-gate-and-verification-required/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)
- **Source (backlog):** [`backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)
- **Wave:** pkg-000034 (366 pytest offline, 2026-06-24)

**Acceptance Criteria:**
- [x] `requested_action`/`return_context` проходят authorize→complete и доступны после логина.
- [x] При действии, требующем verify, и `phone_verified=false` — identity сигналит «нужен verify» (маркер/redirect на verify), без выдачи «зелёного» статуса.
- [x] Зафиксирован канон `verification_required` (403) с `verify_url`; единый для web-gate и GPT-петли; **под `phone_verified`**, не `eid_verified`.
- [x] verify-need (403 авторизации) явно отделён от OTP-ошибок (`SmsErrorCode`, 400).
- [x] Покрыто offline-тестами; контракт описан для gateway ([09-gateway-expectations](../../../runtime-docs/09-gateway-expectations.md)).
