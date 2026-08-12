## Task workspace — `task-ids-08-01-t01-remove-story-drafts-required-tables`

- Story: [`../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) Scope п.1

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000011`  
**Skill declared:** python-pro  
---

## Task: fix — remove story_drafts from _REQUIRED_TABLES

### Цель
Убрать `story_drafts` из `_REQUIRED_TABLES` в Supabase healthcheck, чтобы `/ready` возвращал **200** (`schema:true`) на базе из bootstrap (без таблицы `story_drafts`).

### Почему это важно
Gap SB-1 (HIGH): на корректно поднятой базе `/ready` отдаёт **503**, потому что healthcheck требует отсутствующую таблицу. Story AC #1.

### Факты из кода
1. [`db_supabase.py:315-320`](../../../../../../../src/core/infrastructure/db_supabase.py) — `_REQUIRED_TABLES` включает `"story_drafts"`.
2. [`bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) — `story_drafts` уже исключён из bootstrap (backlog «Уже сделано»).
3. [`test_db_supabase_healthcheck.py`](../../../../../../../tests/test_db_supabase_healthcheck.py) — тесты завязаны на текущий список таблиц.

### Gap / Проблема
Healthcheck считает схему невалидной без `story_drafts` → `/ready` 503 при `DB_BACKEND=supabase`.

### AC/DoD
- [x] (P0) `story_drafts` удалён из `_REQUIRED_TABLES` в `db_supabase.py`.
- [x] (P0) Story AC #1: на bootstrap-базе без `story_drafts` → `/ready` = 200, `schema:true`.
- [x] (P1) `test_db_supabase_healthcheck.py` обновлён под новый список (без story_drafts).

### Где менять код
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) — `_REQUIRED_TABLES`
- [`tests/test_db_supabase_healthcheck.py`](../../../../../../../tests/test_db_supabase_healthcheck.py)

### Out of scope
- Удаление story-роутов, модели, репозиториев — t02–t04
- Миграция / req-15 — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_db_supabase_healthcheck.py -q
# P3+: curl /ready с DB_BACKEND=supabase на bootstrap-базе → 200 schema:true
```
