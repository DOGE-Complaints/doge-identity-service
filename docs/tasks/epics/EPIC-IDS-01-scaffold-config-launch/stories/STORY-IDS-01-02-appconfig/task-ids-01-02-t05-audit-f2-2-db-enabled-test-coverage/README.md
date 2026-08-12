## Task workspace — `task-ids-01-02-t05-audit-f2-2-db-enabled-test-coverage`

- Story: [`../STORY-IDS-01-02-appconfig.md`](../STORY-IDS-01-02-appconfig.md)
- Audit source: [`../../../../audit-report-2026-05-28.md`](../../../../audit-report-2026-05-28.md) (F2-2)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** ready  
**Wave:** `override epic_ids_01_audit_2026_05_28`  
---

## Task: tests — покрыть `db_enabled` в config-тестах

### Цель
Добавить явные asserts для `db_enabled` (`False` при `in_memory`, `True` при `supabase`).

### Факты из кода
1. Аудит F2-2: вычисление `db_enabled` в `schema.py` не покрыто pytest-assert'ами.
2. Story 2 AC включает семантику backend selector.

### AC/DoD
- [ ] (P0) В demo-тесте есть `assert cfg.db_enabled is False`.
- [ ] (P0) Добавлен тест с `DB_BACKEND=supabase` и валидными supabase vars, `assert cfg.db_enabled is True`.

### Где менять код
- `doge-identity-service/tests/test_config_schema.py`
