## Task workspace — `task-ids-02-01-t03-envelope-acceptance-tests`

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000003`  
---

## Task: tests — проверка envelope helpers и trace-id

### Цель
Добавить тесты для AC Story 1: success/error envelope, UUID trace-id и idempotency resolver.

### Факты из кода
1. AC Story 1 перечислены в [`../../../../EPIC-IDS-02-fastapi-transport.md`](../../../../EPIC-IDS-02-fastapi-transport.md).
2. Transport smoke/tests зависят от стабильного response envelope контракта.

### AC/DoD
- [x] Тесты покрывают `build_success_envelope`.
- [x] Тесты покрывают `build_error_envelope` и `trace_id`.
- [x] Тесты валидируют UUID формат из `ensure_trace_id(None)`.
- [x] Тесты покрывают `resolve_idempotency_key`.

### Acceptance
- [acceptance-verification-task-ids-02-01-t03.md](./acceptance-verification-task-ids-02-01-t03.md) — PASS

### Где менять код
- `doge-identity-service/tests/test_api_envelope.py` (или профильный transport test file)
