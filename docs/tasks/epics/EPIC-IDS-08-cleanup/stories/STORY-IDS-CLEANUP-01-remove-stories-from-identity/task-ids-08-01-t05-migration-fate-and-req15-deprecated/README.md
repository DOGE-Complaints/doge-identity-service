## Task workspace — `task-ids-08-01-t05-migration-fate-and-req15-deprecated`

- Story: [`../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) Scope п.5–6

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000011`  
**Skill declared:** python-pro  
---

## Task: fix/docs — migration fate and req-15 deprecated

### Цель
Зафиксировать судьбу миграции `20260527000001_create_story_drafts.sql` (оставить на диске, пометить deprecated) и пометить req-15 устаревшим.

### Почему это важно
Story AC #2 допускает историческую миграцию; AC #4 требует deprecated req-15. Форвард story из identity отменён (решение 2026-06-04).

### Факты из кода
1. [`supabase/migrations/20260527000001_create_story_drafts.sql`](../../../../../../../supabase/migrations/20260527000001_create_story_drafts.sql) — создаёт `story_drafts`.
2. [`docs/requirements/15-story-authorization.md`](../../../../../../../docs/requirements/15-story-authorization.md) — требование story authorization в identity scope.
3. [`bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) — уже без `story_drafts`.

### Gap / Проблема
Миграция и req-15 не отражают, что story scope убран из identity.

### Решение (зафиксировать в P3 BULLRUN)
- **Migration:** файл **не удалять**; добавить SQL-комментарий / header `DEPRECATED — identity scope removed 2026-06`.
- **req-15:** добавить banner `deprecated` с ссылкой на gateway ownership.

### AC/DoD
- [x] (P0) Миграция остаётся на диске с явной DEPRECATED-меткой (комментарий в начале файла).
- [x] (P0) Story AC #4: req-15 помечен deprecated, форвард из identity отменён.
- [x] (P1) Story AC #2: grep `story_drafts` в migration — допустимое исключение.

### Где менять код
- [`supabase/migrations/20260527000001_create_story_drafts.sql`](../../../../../../../supabase/migrations/20260527000001_create_story_drafts.sql) — header comment only
- [`docs/requirements/15-story-authorization.md`](../../../../../../../docs/requirements/15-story-authorization.md)

### Out of scope
- Удаление файла миграции
- Обновление runtime-docs (вне scope story)
- Gateway story implementation

### Проверка
```bash
cd doge-identity-service
head -5 supabase/migrations/20260527000001_create_story_drafts.sql | rg -i deprecated
head -10 docs/requirements/15-story-authorization.md | rg -i deprecated
```
