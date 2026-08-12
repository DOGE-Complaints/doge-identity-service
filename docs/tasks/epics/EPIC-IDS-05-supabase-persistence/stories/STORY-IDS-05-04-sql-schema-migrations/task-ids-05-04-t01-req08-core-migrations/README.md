## Task workspace — `task-ids-05-04-t01-req08-core-migrations`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 4  
**Story:** [`../STORY-IDS-05-04-sql-schema-migrations.md`](../STORY-IDS-05-04-sql-schema-migrations.md)  
---

## Task: data — req-08 core SQL migrations (1–3)

### Цель
Создать 3 миграции из [`docs/requirements/08-supabase-migrations.md`](../../../../../../../docs/requirements/08-supabase-migrations.md) в `supabase/migrations/` (epic L166–168).

### Почему это важно
Identity bootstrap schema (profiles, sessions, audit) — prerequisite для Supabase repositories и healthchecks.

### Факты из кода
1. [`supabase/migrations/.gitkeep`](../../../../../../../supabase/migrations/.gitkeep) — единственный файл; SQL migrations отсутствуют.
2. Epic L166–168 — filenames: `20260525000001_create_profiles.sql`, `20260525000002_create_eid_verification_sessions.sql`, `20260525000003_create_eid_audit_events.sql`.
3. [`docs/requirements/08-supabase-migrations.md`](../../../../../../../docs/requirements/08-supabase-migrations.md) — SSOT SQL (RLS, partial unique index, triggers).
4. Epic L175 — convention `YYYYMMDDHHMMSS_description.sql`, idempotent `IF NOT EXISTS`.

### Gap
req-08 migrations 1–3 не материализованы в repo.

### AC/DoD
- [x] (P0) `20260525000001_create_profiles.sql` — копия req-08 migration 1 (RLS, partial unique, `update_profiles_updated_at` trigger).
- [x] (P0) `20260525000002_create_eid_verification_sessions.sql` — req-08 migration 2.
- [x] (P0) `20260525000003_create_eid_audit_events.sql` — req-08 migration 3.
- [x] (P0) Each file: `ENABLE ROW LEVEL SECURITY` + service_role policy pattern from req-08.

### Где менять код
- `doge-identity-service/supabase/migrations/20260525000001_create_profiles.sql` (новый)
- `doge-identity-service/supabase/migrations/20260525000002_create_eid_verification_sessions.sql` (новый)
- `doge-identity-service/supabase/migrations/20260525000003_create_eid_audit_events.sql` (новый)

### Out of scope
- req-17/req-15 migrations — [`task-ids-05-04-t02-req17-req15-migrations`](../task-ids-05-04-t02-req17-req15-migrations/README.md)
- `oauth_authorization_codes` — epic Open Question L289 (in-memory MVP)

### Проверка
```bash
ls doge-identity-service/supabase/migrations/2026052500000{1,2,3}_*.sql
grep -l 'ROW LEVEL SECURITY' doge-identity-service/supabase/migrations/2026052500000*.sql
```
