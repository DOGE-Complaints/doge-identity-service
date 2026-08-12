## Task workspace — `task-ids-02-03-t03-auth-primitives-verification`

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000003`  
---

## Task: tests — верификация auth primitives stub behavior

### Цель
Добавить проверку AC Story 3 для `UnauthorizedError`, protocol compliance и stub bearer поведения.

### AC/DoD
- [x] Проверен `UnauthorizedError.code`.
- [x] Проверен сценарий без заголовка Authorization -> `UnauthorizedError`.
- [x] Проверен сценарий с `Bearer` -> stub `UserClaims`.

### Acceptance
- [acceptance-verification-task-ids-02-03-t03.md](./acceptance-verification-task-ids-02-03-t03.md) — PASS

### Где менять код
- `doge-identity-service/tests/test_security_primitives.py` (или профильный transport test file)
