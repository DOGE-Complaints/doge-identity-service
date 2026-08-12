## Task workspace — `task-ids-02-01-t02-idempotency-key-resolver`

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000003`  
---

## Task: implement — case-insensitive Idempotency-Key resolver

### Цель
Добавить `resolve_idempotency_key(headers)` в `idempotency.py` с case-insensitive поиском `Idempotency-Key`.

### Факты из кода
1. Story 1 outputs явно требует `src/core/api/idempotency.py` и `resolve_idempotency_key`.
2. Story 1 AC фиксирует ожидаемый результат для `{"idempotency-key": "K"}`.

### AC/DoD
- [x] `resolve_idempotency_key({"idempotency-key":"K"}) == "K"`.
- [x] Поиск ключа нечувствителен к регистру.

### Acceptance
- [acceptance-verification-task-ids-02-01-t02.md](./acceptance-verification-task-ids-02-01-t02.md) — PASS

### Где менять код
- `doge-identity-service/src/core/api/idempotency.py`
