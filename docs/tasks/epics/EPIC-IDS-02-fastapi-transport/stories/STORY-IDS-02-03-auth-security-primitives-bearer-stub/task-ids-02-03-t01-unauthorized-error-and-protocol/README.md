## Task workspace — `task-ids-02-03-t01-unauthorized-error-and-protocol`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000003`  
---

## Task: implement — UnauthorizedError и BearerTokenAuth protocol

### Цель
В `security.py` описать `UnauthorizedError` с кодом `AUTHENTICATION_REQUIRED` и protocol `BearerTokenAuth`.

### AC/DoD
- [x] `UnauthorizedError.code == "AUTHENTICATION_REQUIRED"`.
- [x] `BearerTokenAuth` реализован как `Protocol`.

### Acceptance
- [acceptance-verification-task-ids-02-03-t01.md](./acceptance-verification-task-ids-02-03-t01.md) — PASS

### Где менять код
- `doge-identity-service/src/core/api/security.py`
