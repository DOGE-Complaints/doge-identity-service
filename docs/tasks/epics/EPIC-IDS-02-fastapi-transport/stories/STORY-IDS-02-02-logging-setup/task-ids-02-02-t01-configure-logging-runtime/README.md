## Task workspace — `task-ids-02-02-t01-configure-logging-runtime`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000003`  
---

## Task: implement — configure_logging и runtime exception logger

### Цель
Собрать `configure_logging(...)` и `log_runtime_exception(...)` в `src/core/logging_setup.py` по Story 2.

### Факты из кода
1. Story 2 outputs и AC зафиксированы в [`../../../../EPIC-IDS-02-fastapi-transport.md`](../../../../EPIC-IDS-02-fastapi-transport.md).
2. EPIC-IDS-02 uses lifecycle logging initialization for ASGI startup.

### AC/DoD
- [x] `configure_logging("DEBUG")` выставляет DEBUG для root logger.
- [x] `configure_logging(..., log_format="json")` выполняется без исключений.
- [x] `log_runtime_exception(...)` логирует через `core.runtime`.

### Acceptance
- [acceptance-verification-task-ids-02-02-t01.md](./acceptance-verification-task-ids-02-02-t01.md) — PASS

### Где менять код
- `doge-identity-service/src/core/logging_setup.py`
