## Task workspace — `task-ids-11-02-t03-oauth-introspection-handler`

- Story: [`../STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../STORY-IDS-OAUTH-02-introspection-and-service-token.md)
- Prerequisite: t01–t02; OAUTH-01 token service

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000030`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md) Scope §introspection + §модель phone из профиля; Story AC #1, #3  
---

## Task: implement — OAuth introspection handler (profile-backed)

### Цель
Handler: по пользовательскому OAuth access token вернуть `{active, sub, phone_verified}`; при invalid/expired → `{active: false}`. `phone_verified` — из `ProfileRepository`, не из JWT claims.

### Почему это важно
Gateway introspection layer ([`09-gateway-expectations`](../../../../../../../runtime-docs/09-gateway-expectations.md)) требует свежий `phone_verified` из профиля; отдельный `/oauth/introspect` (не `/me` formalization).

### Факты из кода
1. [`repositories.py:536-545`](../../../../../../../src/core/infrastructure/repositories.py) — `validate_access_token` → `OAuthTokenClaims.sub`.
2. [`me_response.py:42`](../../../../../../../src/core/api/me_response.py) — `phone_verified` from `ProfileRecord`.
3. [`core/oauth/handlers.py`](../../../../../../../src/core/oauth/handlers.py) — existing OAuth handler module pattern.
4. `/oauth/introspect` — **0 routes** in [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py).

### Gap / Проблема
Нет introspection business logic; API-1 gap.

### AC/DoD
- [x] (P0) Valid OAuth access token → `{active: true, sub, phone_verified}` (bool).
- [x] (P0) Expired/invalid token → `{active: false}` (no error leak).
- [x] (P0) `phone_verified` loaded via profile lookup by `sub`, not from token payload.
- [x] (P1) eID fields omitted or DEFERRED (phone-pivot only).
- [x] (P1) Traceability: Story AC #1, #3.

### Где менять код
- `doge-identity-service/src/core/oauth/` (new `introspection.py` or extend `handlers.py`)
- `doge-identity-service/src/core/api/dependencies.py` (wire profile + token service)

### Out of scope
- HTTP route registration (t04)
- Formalizing `/me` as introspection (rejected path per plan)
- Supabase JWT introspection (OAuth access token only for MVP)
- Gateway client code

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q -k introspection
```
