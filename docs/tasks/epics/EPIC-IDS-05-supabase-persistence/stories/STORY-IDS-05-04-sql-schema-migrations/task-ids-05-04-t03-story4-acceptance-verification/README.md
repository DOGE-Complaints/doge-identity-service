## Task workspace — `task-ids-05-04-t03-story4-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 4  
**Story:** [`../STORY-IDS-05-04-sql-schema-migrations.md`](../STORY-IDS-05-04-sql-schema-migrations.md)  
---

## Task: tests — Story 4 acceptance verification

### Цель
Статическая верификация SQL migrations + checklist для live apply; optional pytest on migration file contents (epic L176–180).

### Почему это важно
Healthchecks assume schema exists; broken SQL blocks entire supabase backend.

### Факты из кода
1. Story 4 AC — [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) L176–180.
2. Tasks t01/t02 — создают 5 migration files.
3. Epic L178–179 — post-apply: `required_tables_ready`, `required_columns_ready`, `provider_state_ready`, `service_role_policy_probe`.

### Gap
Нет verification для migration SQL quality и AC checklist.

### AC/DoD
- [x] (P0) Все миграции применяются на чистый Supabase-проект последовательно без ошибок.
- [x] (P0) После применения: `required_tables_ready() == True`, `required_columns_ready() == True`, `provider_state_ready() == True`.
- [x] (P0) `service_role_policy_probe()` → True (RLS не блокирует service_role).
- [x] (P0) Каждая таблица имеет `service_role` policy (либо bypass через service_role API key, явная policy для INSERT/SELECT/UPDATE).

### Где менять код
- `doge-identity-service/tests/test_supabase_migrations_sql.py` (новый — static asserts: RLS, IF NOT EXISTS, filenames)
- Task README checklist section for manual SQL Editor apply (5 files in order)

### Out of scope
- Automated Supabase CLI push — optional per epic L291
- Live probe in CI — EPIC-IDS-06

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_supabase_migrations_sql.py -v
# Manual (live): apply 5 migrations in SQL Editor, then run epic §8 connectivity snippet
```
