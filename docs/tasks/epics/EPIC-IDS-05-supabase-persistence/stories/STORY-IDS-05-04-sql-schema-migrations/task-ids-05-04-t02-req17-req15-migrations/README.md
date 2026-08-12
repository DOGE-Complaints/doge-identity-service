## Task workspace — `task-ids-05-04-t02-req17-req15-migrations`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 4  
**Story:** [`../STORY-IDS-05-04-sql-schema-migrations.md`](../STORY-IDS-05-04-sql-schema-migrations.md)  
---

## Task: data — req-17 provider abstraction and req-15 story_drafts migrations

### Цель
Создать миграции `20260526000001_eid_sessions_provider_abstraction.sql` и `20260527000001_create_story_drafts.sql` (epic L169–174).

### Почему это важно
`provider_state_ready()` и `SupabaseStoryDraftRepository` требуют колонок req-17 и таблицы req-15.

### Факты из кода
1. Epic L169–173 — ALTER: `provider`, `provider_session_data`, nullable legacy columns, index `idx_eid_sessions_provider`.
2. Epic L174 — `story_drafts` table from [`docs/requirements/15-story-authorization.md`](../../../../../../../docs/requirements/15-story-authorization.md).
3. [`docs/requirements/17-eid-provider-abstraction.md`](../../../../../../../docs/requirements/17-eid-provider-abstraction.md) — §"Изменения в DB схеме".
4. Epic L131–133 — `story_drafts` in `required_tables_ready()` list.

### Gap
req-17 ALTER and req-15 table migrations отсутствуют.

### AC/DoD
- [x] (P0) `20260526000001_eid_sessions_provider_abstraction.sql` matches epic L170–173.
- [x] (P0) `20260527000001_create_story_drafts.sql` — `draft_id UUID PK`, `supabase_user_id UUID FK`, `payload JSONB`, `status CHECK`, timestamps, RLS, service_role policy.
- [x] (P0) Idempotent `IF NOT EXISTS` / safe ALTER patterns.

### Где менять код
- `doge-identity-service/supabase/migrations/20260526000001_eid_sessions_provider_abstraction.sql` (новый)
- `doge-identity-service/supabase/migrations/20260527000001_create_story_drafts.sql` (новый)

### Out of scope
- req-08 core migrations — [`task-ids-05-04-t01-req08-core-migrations`](../task-ids-05-04-t01-req08-core-migrations/README.md)

### Проверка
```bash
ls doge-identity-service/supabase/migrations/20260526000001_*.sql \
   doge-identity-service/supabase/migrations/20260527000001_*.sql
```
