## Task workspace — `task-ids-08-01-t09-audit-f2-story-migration-tests-residual`

- Story: [`../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- Audit source: [`../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md) (F2)
- Depends on: t08 (F1 runbook align) — стратегия historical migration

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000012` (draft, `activation: none`)  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md) §F2 · Story AC #3  
---

## Task: tests — story migration tests residual cleanup (F2)

### Цель
Убрать или переписать тесты, которые **энфорсят** наличие `story_drafts` в runbook/migration-наборе, согласовав со стратегией «historical migration on disk only».

### Почему это важно
Story AC #3 требует удалить/переписать story-тесты. Сейчас offline зелёный **потому что** runbook и тесты сохраняют story_drafts — это фиксирует рассогласование F1.

### Факты из кода
1. [`tests/test_supabase_runbook_docs.py:12-17`](../../../../../../../tests/test_supabase_runbook_docs.py) — `EXPECTED_MIGRATION_FILES` включает `20260527000001_create_story_drafts.sql`.
2. [`tests/test_supabase_migrations_sql.py:44-55`](../../../../../../../tests/test_supabase_migrations_sql.py) — SQL-контент `story_drafts` в `EXPECTED_MIGRATIONS`.
3. [`tests/test_supabase_migrations_sql.py:78-88`](../../../../../../../tests/test_supabase_migrations_sql.py) — `test_core_tables_covered_by_migrations` assert `story_drafts`.
4. [`src/`](../../../../../../../src/) — grep `StoryDraft|story_drafts` = 0 (runtime чист).

### Gap / Проблема
Два test-модуля закрепляют story_drafts как часть identity migration contract, хотя bootstrap и `_REQUIRED_TABLES` его не требуют.

### AC/DoD
- [x] (P0) Story AC #3: тесты не требуют story_drafts в operational migration/runbook contract (historical file exempt).
- [x] (P0) `pytest -m "not live_integration" -q` — 0 failed после изменений.
- [x] (P1) Согласовано с t08 runbook wording (одна стратегия в BULLRUN).

### Где менять код
- [`tests/test_supabase_runbook_docs.py`](../../../../../../../tests/test_supabase_runbook_docs.py)
- [`tests/test_supabase_migrations_sql.py`](../../../../../../../tests/test_supabase_migrations_sql.py)

### Out of scope
- Удаление файла миграции с диска
- Runbook правки — t08 (координация)

### Проверка
```bash
cd doge-identity-service
rg "story_drafts" tests --glob '!*live*'
# после P3: только historical-exempt assertions или 0
.venv/bin/python -m pytest tests/test_supabase_runbook_docs.py tests/test_supabase_migrations_sql.py -q
```
