## Task workspace — `task-ids-05-06-t03-story6-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 6  
**Story:** [`../STORY-IDS-05-06-backend-switch-provide-service-factory.md`](../STORY-IDS-05-06-backend-switch-provide-service-factory.md)  
---

## Task: tests — Story 6 acceptance verification

### Цель
Pytest для verbatim AC Story 6 (epic L228–231): factory returns Supabase repos; `build_api_dependencies` db_checks; env-only backend switch.

### Почему это важно
Story 6 — epic integration gate: supabase backend end-to-end wiring without code changes for switch.

### Факты из кода
1. Story 6 AC — [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) L228–231.
2. [`src/core/infrastructure/providers.py`](../../../../../../../src/core/infrastructure/providers.py) — target after t01.
3. [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py) — db_checks from Story 3 t02.
4. [`tests/test_api_dependencies.py`](../../../../../../../tests/test_api_dependencies.py) — DI integration patterns.

### Gap
Нет pytest covering Story 6 AC L228–231 holistically.

### AC/DoD
- [x] (P0) `provide_service_factory(config_with_db_backend_supabase)` возвращает factory с `SupabaseProfileRepository` и т.д.
- [x] (P0) `build_api_dependencies()` при `DB_BACKEND=supabase` — `db_checks` заполнен, `db_ready` отражает реальность.
- [x] (P0) Переключение `DB_BACKEND=in_memory ↔ supabase` через env — единственный механизм; код не модифицируется.

### Где менять код
- `doge-identity-service/tests/test_epic_ids_05_integration.py` (новый) or extend `tests/test_epic_ids_04_integration.py`

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_epic_ids_05_integration.py -v
# Full suite:
cd doge-identity-service && .venv/bin/python -m pytest -m "not live_integration" -q
```
