## Task workspace — `task-ids-02-03-t02-stub-bearer-auth-and-current-user`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000003`  
---

## Task: implement — StubBearerTokenAuth и get_current_user dependency

### Цель
Добавить stub bearer validator и dependency `get_current_user(...)` для transport-уровня EPIC-IDS-02.

### AC/DoD
- [x] `StubBearerTokenAuth().validate({})` бросает `UnauthorizedError`.
- [x] `validate({"authorization": "Bearer xyz"})` возвращает stub `UserClaims`.
- [x] `get_current_user(...)` использует `deps.bearer_token_auth.validate(headers)`.

### Где менять код
- `doge-identity-service/src/core/api/security.py`
- `doge-identity-service/src/core/api/dependencies.py` (минимальный DI для dependency; `asgi_app` — Story 4)

### Acceptance
- [acceptance-verification-task-ids-02-03-t02.md](./acceptance-verification-task-ids-02-03-t02.md) — PASS
