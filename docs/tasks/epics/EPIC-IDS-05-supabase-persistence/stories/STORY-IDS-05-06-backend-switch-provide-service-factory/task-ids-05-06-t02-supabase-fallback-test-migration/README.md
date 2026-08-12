## Task workspace — `task-ids-05-06-t02-supabase-fallback-test-migration`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 6  
**Story:** [`../STORY-IDS-05-06-backend-switch-provide-service-factory.md`](../STORY-IDS-05-06-backend-switch-provide-service-factory.md)  
---

## Task: tests — migrate EPIC-IDS-04 supabase fallback test

### Цель
Обновить [`tests/test_epic_ids_04_integration.py`](../../../../../../../tests/test_epic_ids_04_integration.py) L100–110: заменить `test_provide_service_factory_supabase_falls_back_with_warning` на поведение EPIC-IDS-05 (`ValueError` without creds или Supabase repos).

### Почему это важно
[`EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) L316 фиксирует смену контракта между EPIC-IDS-04 (fallback) и EPIC-IDS-05 (raise / real repos).

### Факты из кода
1. [`tests/test_epic_ids_04_integration.py:100-110`](../../../../../../../tests/test_epic_ids_04_integration.py) — `test_provide_service_factory_supabase_falls_back_with_warning`.
2. Epic L212–214 — `ValueError` when `DB_BACKEND=supabase` without URL/service_role.
3. [`docs/tasks/epics/EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) L316 — test switch note.
4. [`tests/test_api_dependencies.py:159`](../../../../../../../tests/test_api_dependencies.py) — may still assert TODO EPIC-IDS-05 (updated in Story 3 t03).

### Gap
Integration test still encodes pre-EPIC-IDS-05 fallback semantics.

### AC/DoD
- [x] (P0) Remove or replace fallback+warning test with EPIC-IDS-05 behavior.
- [x] (P0) Test documents contract change vs EPIC-IDS-04 in comment (ref EPIC-IDS-06 L316).
- [x] (P0) `provide_service_factory` with valid supabase config returns Supabase repo types (mock httpx or isinstance checks).

### Где менять код
- `doge-identity-service/tests/test_epic_ids_04_integration.py`

### Out of scope
- Full factory DI AC — [`task-ids-05-06-t03-story6-acceptance-verification`](../task-ids-05-06-t03-story6-acceptance-verification/README.md)

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_epic_ids_04_integration.py -v
```
