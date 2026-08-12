## Task workspace — `task-ids-02-02-t02-logging-verification`

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000003`  
---

## Task: tests — верификация logging setup контрактов

### Цель
Зафиксировать проверками Story 2 AC: уровни/формат логирования и отсутствие исключений в runtime exception logger.

### AC/DoD
- [x] Есть тест на `configure_logging("DEBUG")`.
- [x] Есть тест на `log_format="json"` без исключений.
- [x] Есть тест на `log_runtime_exception(...)` без падений.

### Acceptance
- [acceptance-verification-task-ids-02-02-t02.md](./acceptance-verification-task-ids-02-02-t02.md) — PASS

### Где менять код
- `doge-identity-service/tests/test_logging_setup.py` (или эквивалентный файл)
