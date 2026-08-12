## Task workspace — `task-ids-02-05-t04-audit-a2-ready-supabase-503-test`

- Story: [`../STORY-IDS-02-05-routes-contract-health-ready-identity-stubs.md`](../STORY-IDS-02-05-routes-contract-health-ready-identity-stubs.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (A-2)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_02_audit_2026_05_28`  
---

## Task: tests — `/ready` 503 при `db_backend=supabase`

### Цель
Закрыть gap A-2: покрыть тестом degraded readiness для `DB_BACKEND=supabase` (до EPIC-IDS-05).

### Факты из кода
1. [`dependencies.py:25`](../../../../../../../src/core/api/dependencies.py): `db_ready = db_backend == "in_memory"`.
2. [`handlers.py:17–26`](../../../../../../../src/core/api/handlers.py): `handle_readiness` → 503 если `not deps.db_ready`.
3. [`tests/test_asgi_transport.py`](../../../../../../../tests/test_asgi_transport.py): `test_ready_in_memory_backend` покрывает только `in_memory`.
4. Audit A-2 предлагает паттерн: `_clear_api_dependencies_cache()` + `create_app(provide_app_config({...}))` + `TestClient`.

### AC/DoD
- [x] (P0) `test_ready_supabase_backend_reports_degraded`: HTTP 503, `data.db_ready is False`, `data.db_backend == "supabase"`.

### Acceptance
- [acceptance-verification-task-ids-02-05-t04-audit-a2-ready-supabase-503-test.md](./acceptance-verification-task-ids-02-05-t04-audit-a2-ready-supabase-503-test.md) — PASS

### Где менять код
- `doge-identity-service/tests/test_asgi_transport.py`

### Out of scope
- Изменение логики `db_ready` / реальная supabase healthcheck (EPIC-IDS-05)

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_asgi_transport.py -q -k ready_supabase
```
