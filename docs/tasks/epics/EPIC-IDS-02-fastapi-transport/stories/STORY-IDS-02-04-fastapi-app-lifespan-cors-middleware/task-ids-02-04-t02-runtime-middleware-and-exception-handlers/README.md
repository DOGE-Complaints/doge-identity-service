## Task workspace — `task-ids-02-04-t02-runtime-middleware-and-exception-handlers`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done
**Wave:** `pkg-000003`  
---

## Task: implement — runtime middleware и exception handlers

### Цель
Добавить middleware для trace-id propagation/runtime diagnostics и exception handlers для `UnauthorizedError` и `ConfigError`.

### AC/DoD
- [x] Trace-id передаётся в envelope.
- [x] `UnauthorizedError` конвертируется в 401 `AUTHENTICATION_REQUIRED`.
- [x] `ConfigError` конвертируется в 500 `CONFIG_ERROR`.

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py`
- `doge-identity-service/src/core/api/envelope.py`

### Process
- [BULLRUN-PHASE-LOG.md](./BULLRUN-PHASE-LOG.md)
