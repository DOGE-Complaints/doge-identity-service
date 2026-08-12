## Task workspace — `task-ids-08-01-t08-audit-f1-runbook-story-drafts-migration-align`

- Story: [`../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- Audit source: [`../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md) (F1)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000012` (draft, `activation: none`)  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-01-audit-2026-06-05.md) §F1  
---

## Task: fix/docs — runbook story_drafts migration align (F1)

### Цель
Выровнять runbook §3 с решением t05: миграция `20260527000001_create_story_drafts.sql` — **historical only**, не применять на новых identity deployments.

### Почему это важно
Оператор по runbook применит deprecated-миграцию и пересоздаст `story_drafts`, что противоречит выносу stories в gateway. Блокирует чистое закрытие AC2/AC3 (связано с F2).

### Факты из кода
1. [`supabase/migrations/20260527000001_create_story_drafts.sql:1-2`](../../../../../../../supabase/migrations/20260527000001_create_story_drafts.sql) — `DEPRECATED` · `do not apply on new identity deployments`.
2. [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) — `story_drafts` исключён из bootstrap.
3. [`docs/runbook/supabase-project-setup.md:62`](../../../../../../../docs/runbook/supabase-project-setup.md) — migration #5 `story_drafts` в обязательном списке «выполните по порядку».
4. [`tests/test_supabase_runbook_docs.py:17`](../../../../../../../tests/test_supabase_runbook_docs.py) — тест ожидает story_drafts в `EXPECTED_MIGRATION_FILES` (связь F2).

### Gap / Проблема
Три источника о судьбе `story_drafts`-миграции рассогласованы (migration / bootstrap / runbook).

### AC/DoD
- [x] (P0) Runbook §3 не предписывает применять `20260527000001` на новых deployments (убрать из обязательного списка или пометить historical/optional).
- [x] (P0) Текст runbook согласован с шапкой миграции и bootstrap.
- [x] (P1) Направление зафиксировано в BULLRUN-PHASE-LOG (P3).

### Где менять код
- [`docs/runbook/supabase-project-setup.md`](../../../../../../../docs/runbook/supabase-project-setup.md) — §3 migration table
- **Не** удалять файл миграции (t05 decision)

### Out of scope
- Переписывание `test_supabase_runbook_docs.py` — t09 (F2)
- Reopen pkg-000011

### Проверка
```bash
grep -n "story_drafts" doge-identity-service/docs/runbook/supabase-project-setup.md
# ожидание после P3: historical/optional wording, не «apply in order» без оговорки
```
