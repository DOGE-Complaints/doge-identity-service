## Task workspace — `task-ids-05-03-t03-story3-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 3  
**Story:** [`../STORY-IDS-05-03-five-level-healthcheck.md`](../STORY-IDS-05-03-five-level-healthcheck.md)  
---

## Task: tests — Story 3 acceptance verification

### Цель
Pytest для verbatim AC Story 3 (epic L151–155): health methods never raise, network error → False, `/ready` 503 degraded, startup log shape.

### Почему это важно
Readiness contract зафиксирован в EPIC-IDS-02/03; Story 3 заменяет stub на реальные checks.

### Факты из кода
1. Story 3 AC — [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) L151–155.
2. [`tests/test_asgi_transport.py:119-138`](../../../../../../../tests/test_asgi_transport.py) — existing supabase degraded test (extend for `db_checks` envelope).
3. [`tests/test_api_dependencies.py:159`](../../../../../../../tests/test_api_dependencies.py) — asserts TODO EPIC-IDS-05 (update after t02).

### Gap
Нет полного pytest coverage для AC L151–155.

### AC/DoD
- [x] (P0) Все 5 healthcheck-методов возвращают `bool`, никогда не raise (внутри `try/except Exception: return False`).
- [x] (P0) При сетевой ошибке → `False`.
- [x] (P0) `GET /ready` при `db_backend=supabase` + `db_ready=False` → HTTP 503, envelope `{"data": {"status": "degraded", ..., "db_checks": {...}}}`.
- [x] (P0) Startup-лог содержит `db_checks={'connectivity': True/False, ...}` (после `configure_logging`).

### Где менять код
- `doge-identity-service/tests/test_db_supabase_healthcheck.py` (новый, unit)
- `doge-identity-service/tests/test_asgi_transport.py` (extend)
- `doge-identity-service/tests/test_api_dependencies.py` (update TODO assertion)

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_db_supabase_healthcheck.py tests/test_asgi_transport.py -v -k "health or ready or supabase"
```
