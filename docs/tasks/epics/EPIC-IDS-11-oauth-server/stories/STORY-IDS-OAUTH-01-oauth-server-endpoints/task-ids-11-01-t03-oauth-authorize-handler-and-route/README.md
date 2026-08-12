## Task workspace — `task-ids-11-01-t03-oauth-authorize-handler-and-route`

- Story: [`../STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../STORY-IDS-OAUTH-01-oauth-server-endpoints.md)
- Prerequisite: t01 (store), t02 (errors/scope)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000029`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) Scope bullet `/oauth/authorize` validations; Story AC #5, #6; [req-14 §GET/authorize](../../../../../requirements/14-oauth-server-custom-gpt.md)  
---

## Task: implement — GET `/oauth/authorize` handler and route

### Цель
Заменить 501 stub на рабочий `GET /oauth/authorize`: валидации client/redirect_uri/scope/state, сохранение authorization request, redirect в spa-login с `oauth_request_id`. **Без** Supabase JWT на authorize (req-14 §GET).

### Почему это важно
Сейчас [`asgi_app.py:334-371`](../../../../../../../src/core/api/asgi_app.py) направляет `/oauth/*` в `handle_bearer_stub` → 501.

### Факты из кода
1. [`asgi_app.py:334-371`](../../../../../../../src/core/api/asgi_app.py) — oauth routes → `handle_bearer_stub`.
2. [`handlers.py`](../../../../../../../src/core/api/handlers.py) — `handle_bearer_stub` returns 501.
3. [`repositories.py:405-427`](../../../../../../../src/core/infrastructure/repositories.py) — client lookup + redirect_uri validation source.
4. t01 — `AuthorizationRequestStore` (to be wired).

### Gap / Проблема
Нет handler для authorize; stub + Bearer на GET authorize блокирует ChatGPT entry flow.

### AC/DoD
- [x] (P0) `GET /oauth/authorize` — **no** Bearer required (public entry).
- [x] (P0) Unknown `client_id` → `invalid_client` (RFC JSON, direct response).
- [x] (P0) Bad `redirect_uri` → `invalid_redirect_uri` (**direct**, not redirect).
- [x] (P0) Bad scope → `invalid_scope`.
- [x] (P0) Valid request → save to store → 302 redirect to spa-login URL with `oauth_request_id`; `state` preserved for later.
- [x] (P1) Remove stub/Bearer requirement for GET authorize in `asgi_app.py`.

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`
- `doge-identity-service/src/core/api/asgi_app.py`

### Out of scope
- `/oauth/authorize/complete`, `/oauth/token` (t04)
- OAuth access token on protected routes (t05)
- E2E tests (t06)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```
