## Task workspace — `task-ids-11-01-t05-oauth-access-token-bearer-dependency`

- Story: [`../STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../STORY-IDS-OAUTH-01-oauth-server-endpoints.md)
- Prerequisite: t04 (access tokens issued)

---
**Приоритет:** P1  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000029`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) Scope bullet OAuth access token acceptance on protected routes  
---

## Task: implement — OAuth access token bearer dependency

### Цель
Позволить защищённым маршрутам принимать OAuth access token от ChatGPT (dual scheme или отдельная dependency поверх `OAuthTokenService.validate_access_token`).

### Почему это важно
[`security.py:51-56`](../../../../../../../src/core/api/security.py) — `get_current_user` валидирует **только** Supabase JWT; без dual acceptance OAuth-токен бесполезен для API после выдачи.

### Факты из кода
1. [`security.py:51-56`](../../../../../../../src/core/api/security.py) — Supabase-only JWT validation.
2. [`repositories.py:430-506`](../../../../../../../src/core/infrastructure/repositories.py) — `validate_access_token` on token service (if present).
3. [`dependencies.py`](../../../../../../../src/core/api/dependencies.py) — current auth deps.

### Gap / Проблема
Нет пути аутентификации через issued OAuth access token на protected endpoints.

### AC/DoD
- [x] (P0) Dependency (e.g. `get_current_user_or_oauth`) tries Supabase JWT first, then OAuth access token via `OAuthTokenService.validate_access_token`.
- [x] (P0) Resolved principal includes `supabase_user_id` + granted scopes from token.
- [x] (P1) Document which routes use dual scheme vs Supabase-only.
- [x] (P1) Unit test: valid OAuth token accepted; invalid rejected.

### Где менять код
- `doge-identity-service/src/core/api/security.py`
- `doge-identity-service/src/core/api/dependencies.py`
- `doge-identity-service/tests/` (auth dependency tests)

### Out of scope
- Gateway introspection (OAUTH-02)
- Changing all routes to OAuth-only (dual is MVP)
- Full E2E GPT flow (t06 covers server flow)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```
