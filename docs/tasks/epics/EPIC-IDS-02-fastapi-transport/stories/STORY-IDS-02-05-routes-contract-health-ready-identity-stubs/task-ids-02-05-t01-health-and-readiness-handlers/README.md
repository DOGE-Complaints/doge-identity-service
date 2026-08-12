## Task workspace — `task-ids-02-05-t01-health-and-readiness-handlers`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done
**Wave:** `pkg-000003`  
---

## Task: implement — handlers для /health и /ready

### Цель
Собрать `handle_health` и `handle_readiness` в `handlers.py` по contract Story 5.

### AC/DoD
- [x] `/health` выдаёт 200 + `data.status == "ok"`.
- [x] `/ready` выдаёт 200/503 в зависимости от `db_ready`.
- [x] В ответе присутствуют `trace_id` и readiness fields из story contract.

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`

### Process
- [BULLRUN-PHASE-LOG.md](./BULLRUN-PHASE-LOG.md)
