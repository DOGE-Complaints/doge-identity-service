## Task workspace — `task-ids-11-01-t04-oauth-complete-token-handlers-and-routes`

- Story: [`../STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../STORY-IDS-OAUTH-01-oauth-server-endpoints.md)
- Prerequisite: t01–t03

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** done  
**Wave:** `pkg-000029`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) Scope bullets connect endpoints to `OAuthTokenService`; Story AC #1, #2, #4, #6  
---

## Task: implement — `/oauth/authorize/complete` + `/oauth/token` handlers and routes

### Цель
Подключить complete и token endpoints к `OAuthTokenService`: complete с Bearer Supabase JWT резолвит `oauth_request_id` → code → redirect ChatGPT; token exchange с PKCE wire.

### Почему это важно
Замыкает OAuth code flow: authorize (t03) → login → complete → ChatGPT callback → token.

### Факты из кода
1. [`repositories.py:430-506`](../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryOAuthTokenService` (issue code, exchange, PKCE).
2. [`security.py:51-56`](../../../../../../../src/core/api/security.py) — `get_current_user` for Supabase JWT on complete.
3. [`asgi_app.py:334-371`](../../../../../../../src/core/api/asgi_app.py) — stubs for complete/token.
4. t01 — authorization request store; t02 — RFC errors + client_secret.

### Gap / Проблема
Complete/token routes still 501; no wiring from HTTP to token service + auth request store.

### AC/DoD
- [x] (P0) `POST /oauth/authorize/complete` — requires Bearer Supabase JWT; consumes `oauth_request_id`; issues code bound to `supabase_user_id`; redirects to client `redirect_uri` with `?code&state`.
- [x] (P0) `POST /oauth/token` — **no** Bearer; exchanges code for access token via `OAuthTokenService`.
- [x] (P0) PKCE: `code_challenge` at authorize requires matching `code_verifier` at token (Story AC #4).
- [x] (P0) Reuse/expired code → `invalid_grant` (t02 error format).
- [x] (P1) Remove remaining oauth stubs in `asgi_app.py` for complete/token.

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`
- `doge-identity-service/src/core/api/asgi_app.py`
- `doge-identity-service/src/core/api/dependencies.py` (if new deps)

### Out of scope
- OAuth bearer on general protected routes (t05)
- Comprehensive test suite (t06)
- Introspection (OAUTH-02)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```
