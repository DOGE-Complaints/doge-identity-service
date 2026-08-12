# STORY-IDS-OAUTH-01 — OAuth 2.0 сервер наружу (`/oauth/authorize`, `/oauth/token`)

## Meta
- **Key:** `STORY-IDS-OAUTH-01-oauth-server-endpoints`
- **Parent Epic:** [`../../EPIC-IDS-11-oauth-server.md`](../../EPIC-IDS-11-oauth-server.md)
- **Epic alias (код/backlog):** `EPIC-IDS-OAUTH` · продуктовый зонтик [`EPIC-IDS-ONBOARDING`](../../../../backlog-stories/identity-onboarding/EPIC-IDS-ONBOARDING.md)
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md)
- **Decision Ref:** [`../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md); [`14-oauth-server-custom-gpt.md`](../../../../../requirements/14-oauth-server-custom-gpt.md); [`oauth-validation-2026-06-12.md`](../../../../../analysis/oauth-validation-2026-06-12.md)
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../../../analysis/identity-todo-backlog-2026-06-04.md) — A4, C7, C8; gap SEC-1
- **Зависит от:** [STORY-IDS-AUTHCORE-01](../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-01-profile-and-me.md) (логин/профиль) — 🟢 Done

## Зачем простыми словами
Чтобы ChatGPT (Custom GPT) мог действовать от имени пользователя, identity должен работать как OAuth 2.0 сервер: выдать authorization code, обменять его на access-токен. Движок токенов уже написан, но **наружу не подключён** — маршруты `/oauth/*` пока 501.

## Scope
- Подключить `/oauth/authorize`, `/oauth/authorize/complete`, `/oauth/token` к рабочему `OAuthTokenService` (заменить `handle_bearer_stub`).
- Включить проверку `client_secret` в прод-пути (сейчас намеренно отключена).
- Соблюсти PKCE S256 (уже реализован в движке).
- **`/oauth/authorize` валидации** (по [req-14 §GET/authorize](../../../../../requirements/14-oauth-server-custom-gpt.md)): `invalid_client`, `invalid_redirect_uri` (отдавать напрямую, не через redirect), `invalid_scope`, проброс `state`.
- **`authorization_request`-store + `oauth_request_id`-handshake**: `/oauth/authorize` сохраняет запрос (client_id/redirect_uri/scope/state/PKCE/TTL) и редиректит в spa-login с `oauth_request_id`; `/oauth/authorize/complete` (Bearer Supabase JWT) резолвит его → выдаёт code → redirect в ChatGPT (`?code&state`). **В движке этого стора пока нет** — добавить.
- **Приём OAuth-access-token эндпоинтами**: определить, как защищённые маршруты принимают OAuth-токен от ChatGPT (сейчас `get_current_user` валидирует только Supabase JWT) — двойная схема или отдельная зависимость.
- **Формат ошибок RFC 6749** (`{error, error_description}`) и **scope-модель** (`profile:read`/`stories:draft`/`stories:create`, [req-14 §Scope Model](../../../../../requirements/14-oauth-server-custom-gpt.md)).

## Вне scope
- Межсервисная валидация токена gateway'ем (introspection) — [STORY-IDS-OAUTH-02](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md).
- eID-проверка (статус берётся из профиля, ставится в EID-эпике).

## Точки в коде (текущее состояние)
- Маршруты-заглушки: [`asgi_app.py:334-371`](../../../../../../src/core/api/asgi_app.py) → `handle_bearer_stub` → 501.
- Готовый движок: `InMemoryOAuthTokenService` ([`repositories.py:430-506`](../../../../../../src/core/infrastructure/repositories.py)) — code/token/PKCE. ⚠️ **in-memory** (теряется на редеплое) → durable Supabase-стор в [STORY-IDS-OAUTH-03](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md). Access-токен — stateless HS256, хранить не нужно.
- ⚠️ `client_secret` не проверяется: [`repositories.py:466-467`](../../../../../../src/core/infrastructure/repositories.py) (gap SEC-1).
- Клиент GPT: `OAuthClientStore` ([`contracts.py:122-125`](../../../../../../src/core/domain/contracts.py)).
- `get_current_user` — только Supabase JWT: [`security.py:51-56`](../../../../../../src/core/api/security.py).

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
[04-security §3](../../../../../runtime-docs/04-security.md), [09-gateway-expectations](../../../../../runtime-docs/09-gateway-expectations.md) — identity = OAuth-сервер, токен потом проверяет gateway.

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-11-01-t01-authorization-request-store-and-contracts`](./task-ids-11-01-t01-authorization-request-store-and-contracts/README.md) | pkg-000029 |
| 2 | [`task-ids-11-01-t02-rfc6749-errors-scope-validation-client-secret`](./task-ids-11-01-t02-rfc6749-errors-scope-validation-client-secret/README.md) | pkg-000029 |
| 3 | [`task-ids-11-01-t03-oauth-authorize-handler-and-route`](./task-ids-11-01-t03-oauth-authorize-handler-and-route/README.md) | pkg-000029 |
| 4 | [`task-ids-11-01-t04-oauth-complete-token-handlers-and-routes`](./task-ids-11-01-t04-oauth-complete-token-handlers-and-routes/README.md) | pkg-000029 |
| 5 | [`task-ids-11-01-t05-oauth-access-token-bearer-dependency`](./task-ids-11-01-t05-oauth-access-token-bearer-dependency/README.md) | pkg-000029 |
| 6 | [`task-ids-11-01-t06-offline-oauth-server-tests`](./task-ids-11-01-t06-offline-oauth-server-tests/README.md) | pkg-000029 |
| 7 | [`task-ids-11-01-t07-story-acceptance-verification`](./task-ids-11-01-t07-story-acceptance-verification/README.md) | pkg-000029 |
