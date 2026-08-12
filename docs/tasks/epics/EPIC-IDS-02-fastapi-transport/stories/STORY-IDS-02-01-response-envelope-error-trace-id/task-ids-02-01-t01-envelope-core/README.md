## Task workspace — `task-ids-02-01-t01-envelope-core`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000003`  
---

## Task: implement — envelope helpers и trace-id generation

### Цель
Реализовать в `envelope.py` функции `build_success_envelope`, `build_error_envelope`, `ensure_trace_id` строго по Story 1 EPIC-IDS-02.

### Факты из кода
1. Story 1 outputs и AC определены в [`../../../../EPIC-IDS-02-fastapi-transport.md`](../../../../EPIC-IDS-02-fastapi-transport.md).
2. Целевой файл зафиксирован в epic §5: `src/core/api/envelope.py`.

### AC/DoD
- [x] `build_success_envelope({"status":"ok"})` возвращает `{"data":{"status":"ok"}}`.
- [x] `build_error_envelope(..., trace_id="abc", status_code=404)` включает `error.trace_id == "abc"`.
- [x] `ensure_trace_id(None)` возвращает валидный UUID4.

### Acceptance
- [acceptance-verification-task-ids-02-01-t01.md](./acceptance-verification-task-ids-02-01-t01.md) — PASS

### Где менять код
- `doge-identity-service/src/core/api/envelope.py`
