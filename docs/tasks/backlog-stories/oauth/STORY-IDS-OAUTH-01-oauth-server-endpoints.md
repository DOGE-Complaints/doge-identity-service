# STORY-IDS-OAUTH-01 — OAuth 2.0 сервер наружу (`/oauth/authorize`, `/oauth/token`)

## Meta
- **Key:** `STORY-IDS-OAUTH-01-oauth-server-endpoints`
- **Epic:** `EPIC-IDS-ONBOARDING` (продуктовый зонтик — [`identity-onboarding/`](../identity-onboarding/EPIC-IDS-ONBOARDING.md)); код-алиас `EPIC-IDS-OAUTH` (`next_epic` в `asgi_app.py`); pipeline — [`EPIC-IDS-11`](../../epics/EPIC-IDS-11-oauth-server/EPIC-IDS-11-oauth-server.md) (pkg-000029)
- **Status:** 🟢 Done
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../analysis/identity-todo-backlog-2026-06-04.md) — A4, C7, C8; gap SEC-1
- **Зависит от:** [STORY-IDS-AUTHCORE-01](../auth-core/STORY-IDS-AUTHCORE-01-profile-and-me.md) (логин/профиль)

## Зачем простыми словами
Чтобы ChatGPT (Custom GPT) мог действовать от имени пользователя, identity работает как OAuth 2.0 сервер: выдаёт authorization code, обменивает его на access-токен. Маршруты `/oauth/authorize`, `/oauth/authorize/complete`, `/oauth/token` подключены к движку (EPIC-IDS-11, pkg-000029).

## Scope
- Подключить `/oauth/authorize`, `/oauth/authorize/complete`, `/oauth/token` к рабочему `OAuthTokenService` (заменить `handle_bearer_stub`).
- Включить проверку `client_secret` в прод-пути (сейчас намеренно отключена).
- Соблюсти PKCE S256 (уже реализован в движке).
- **`/oauth/authorize` валидации** (по [req-14 §GET/authorize](../../../requirements/14-oauth-server-custom-gpt.md)): `invalid_client`, `invalid_redirect_uri` (отдавать напрямую, не через redirect), `invalid_scope`, проброс `state`.
- **`authorization_request`-store + `oauth_request_id`-handshake**: `/oauth/authorize` сохраняет запрос (client_id/redirect_uri/scope/state/PKCE/TTL) и редиректит в spa-login с `oauth_request_id`; `/oauth/authorize/complete` (Bearer Supabase JWT) резолвит его → выдаёт code → redirect в ChatGPT (`?code&state`). **В движке этого стора пока нет** — добавить.
- **Приём OAuth-access-token эндпоинтами**: определить, как защищённые маршруты принимают OAuth-токен от ChatGPT (сейчас `get_current_user` валидирует только Supabase JWT) — двойная схема или отдельная зависимость.
- **Формат ошибок RFC 6749** (`{error, error_description}`) и **scope-модель** (`profile:read`/`stories:draft`/`stories:create`, [req-14 §Scope Model](../../../requirements/14-oauth-server-custom-gpt.md)).

## Вне scope
- Межсервисная валидация токена gateway'ем (introspection) — [STORY-IDS-OAUTH-02](STORY-IDS-OAUTH-02-introspection-and-service-token.md).
- eID-проверка (статус берётся из профиля, ставится в EID-эпике).

## Точки в коде (текущее состояние)
- Маршруты: [`asgi_app.py:368-403`](../../../../src/core/api/asgi_app.py) — `/oauth/authorize`, `/oauth/authorize/complete`, `/oauth/token`.
- Handlers: [`core/oauth/handlers.py`](../../../../src/core/oauth/handlers.py) (`handle_oauth_authorize`, `handle_oauth_authorize_complete`, `handle_oauth_token`).
- Authorization request store: `InMemoryAuthorizationRequestStore` ([`repositories.py:431`](../../../../src/core/infrastructure/repositories.py)). ⚠️ **in-memory** (теряется на редеплое) → durable Supabase-стор в [STORY-IDS-OAUTH-03](STORY-IDS-OAUTH-03-persistent-token-store-supabase.md).
- OAuth token service: `InMemoryOAuthTokenService` ([`repositories.py:430+`](../../../../src/core/infrastructure/repositories.py)) — code/token/PKCE. Access-токен — stateless HS256.
- `client_secret` проверяется: [`verify_client_secret`](../../../../src/core/oauth/client_secret.py) в [`repositories.py:495-501`](../../../../src/core/infrastructure/repositories.py) (SEC-1 закрыт).
- OAuth + Supabase JWT: `CompositeBearerTokenAuth` ([`security.py:34`](../../../../src/core/api/security.py)).
- Клиент GPT: `OAuthClientStore` ([`contracts.py`](../../../../src/core/domain/contracts.py)).

## Acceptance Criteria
- [x] `/oauth/authorize` (с валидным Supabase JWT) выдаёт authorization code привязанный к `supabase_user_id`.
- [x] `/oauth/token` обменивает валидный code на access-токен; повторный обмен/просрочка → `invalid_grant`.
- [x] Неверный `client_secret` → отказ (в прод-пути проверка включена).
- [x] PKCE: запрос с `code_challenge` требует корректный `code_verifier`.
- [x] `/oauth/authorize`: незарегистрированный `client_id` → `invalid_client`; неверный `redirect_uri` → `invalid_redirect_uri` (напрямую, не redirect); неверный scope → `invalid_scope`; `state` пробрасывается.
- [x] `authorization_request`-store: `/oauth/authorize` → redirect в spa-login с `oauth_request_id`; `/oauth/authorize/complete` (Bearer Supabase JWT) → code + redirect в ChatGPT.
- [x] Ошибки в формате RFC 6749 (`{error, error_description}`); scope-модель валидируется.
- [x] Покрыто тестами (offline).

## Парадигма-якорь
[04-security §3](../../../runtime-docs/04-security.md), [09-gateway-expectations](../../../runtime-docs/09-gateway-expectations.md) — identity = OAuth-сервер, токен потом проверяет gateway.

**Related (UI contract):** GPT verify landing + возврат после phone — [`08-ui-expectations.md` §3c](../../../runtime-docs/08-ui-expectations.md) ([DOC-IDS-ONB-03](../identity-onboarding/DOC-IDS-ONB-03-gpt-verify-landing-contract.md)).
