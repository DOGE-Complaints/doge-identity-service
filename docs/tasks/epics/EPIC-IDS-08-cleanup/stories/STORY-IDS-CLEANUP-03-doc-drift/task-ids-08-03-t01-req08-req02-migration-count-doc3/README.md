## Task workspace — `task-ids-08-03-t01-req08-req02-migration-count-doc3`

- Story: [`../STORY-IDS-CLEANUP-03-doc-drift.md`](../STORY-IDS-CLEANUP-03-doc-drift.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-03-doc-drift.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-03-doc-drift.md) Scope DOC-3; [`../../../../../../analysis/gap-analysis-full-2026-06-04.md`](../../../../../../analysis/gap-analysis-full-2026-06-04.md) DOC-3

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000014`  
**Skill declared:** python-pro  
---

## Task: fix/docs — req-08 and req-02 migration count (DOC-3)

### Цель
Закрыть gap DOC-3: requirements должны отражать **4 operational migrations** (включая `provider_abstraction`), а не «3 миграции».

### Почему это важно
Story AC #1; onboarding по Supabase опирается на req-08/req-02. [`02-data-bootstrap.md:26-33`](../../../../../../../docs/runtime-docs/02-data-bootstrap.md) уже описывает 4 migrations — requirements отстают.

### Факты из кода
1. [`req-08:12-16`](../../../../../../../docs/requirements/08-supabase-migrations.md) — перечислены только 3 файла миграций.
2. [`req-02:20`](../../../../../../../docs/requirements/02-scope-and-boundaries.md) — «3 таблицы: profiles, eid_verification_sessions, eid_audit_events» без migration #4.
3. [`supabase/migrations/20260526000001_eid_sessions_provider_abstraction.sql`](../../../../../../../supabase/migrations/20260526000001_eid_sessions_provider_abstraction.sql) — 4-я operational migration (exists).
4. [`02-data-bootstrap.md:31`](../../../../../../../docs/runtime-docs/02-data-bootstrap.md) — migration #4 уже задокументирована в runtime-docs.

### Gap / Проблема
req-08/req-02 утверждают «3 миграции»; фактически 4 (добавить provider_abstraction). 5-й файл `story_drafts` — deprecated, вне operational set (backlog Scope).

### AC/DoD
- [x] (P0) Story AC #1: [`08-supabase-migrations.md`](../../../../../../../docs/requirements/08-supabase-migrations.md) §structure включает migration 4 (`provider_abstraction`).
- [x] (P0) Story AC #1: [`02-scope-and-boundaries.md:20`](../../../../../../../docs/requirements/02-scope-and-boundaries.md) согласован с 4 migrations (wording без «3 миграции» drift).
- [x] (P1) BULLRUN-PHASE-LOG + acceptance-verification в этой папке (P3).

### Где менять код
- [`docs/requirements/08-supabase-migrations.md`](../../../../../../../docs/requirements/08-supabase-migrations.md) — §«Структура миграций»
- [`docs/requirements/02-scope-and-boundaries.md`](../../../../../../../docs/requirements/02-scope-and-boundaries.md) — таблица MVP scope, строка Supabase migrations

### Out of scope
- Изменение SQL миграций или bootstrap
- Deprecated `20260527000001_create_story_drafts.sql` (historical; не в operational count)
- Полный rewrite req-08 body (только migration count/structure alignment)

### Проверка
```bash
cd doge-identity-service
ls supabase/migrations/202605*.sql
grep -n "3 миграц\|3 таблицы\|provider_abstraction" docs/requirements/08-supabase-migrations.md docs/requirements/02-scope-and-boundaries.md
```
