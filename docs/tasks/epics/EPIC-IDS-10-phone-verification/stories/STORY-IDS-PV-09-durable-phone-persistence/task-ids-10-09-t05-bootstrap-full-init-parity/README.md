## Task workspace — `task-ids-10-09-t05-bootstrap-full-init-parity`

- Story: [`../STORY-IDS-PV-09-durable-phone-persistence.md`](../STORY-IDS-PV-09-durable-phone-persistence.md)
- Prerequisite: [`task-ids-10-09-t01-phone-persistence-migration-sql`](../task-ids-10-09-t01-phone-persistence-migration-sql/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000039`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md) Scope §«Bootstrap parity»; Story AC #6  
---

## Task: fix — bootstrap 000_full_init.sql parity with migrations

### Цель
Расширить [`supabase/bootstrap/000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) так, чтобы fresh bootstrap == полный накат миграций.

### Почему это важно
Bootstrap создаёт только 3 core-таблицы; phone-колонки, OAuth-таблицы и новые phone-persistence-таблицы отсутствуют — fresh install ≠ migrated schema.

### Факты из кода
1. Bootstrap gap: [`000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) — only `profiles`, `eid_verification_sessions`, `eid_audit_events`.
2. Phone profile cols: [`20260611000001_profiles_phone_verification.sql`](../../../../../../../supabase/migrations/20260611000001_profiles_phone_verification.sql).
3. OAuth tables: [`20260624000001_oauth_authorization_tables.sql`](../../../../../../../supabase/migrations/20260624000001_oauth_authorization_tables.sql), [`20260624000002_oauth_authorization_request_context.sql`](../../../../../../../supabase/migrations/20260624000002_oauth_authorization_request_context.sql).
4. Phone persistence schema from t01 migration.

### Gap / Проблема
`000_full_init.sql` отстаёт от инкрементальных миграций; phone-гейт на чистой БД негде персистить.

### AC/DoD
- [x] (P0) Bootstrap includes phone profile columns from `20260611000001`.
- [x] (P0) Bootstrap includes OAuth tables from `20260624000001` + `20260624000002`.
- [x] (P0) Bootstrap includes phone-persistence tables from t01 migration.
- [x] (P1) Traceability: Story AC #6 — schema diff bootstrap vs migrations verifiable.
- [x] (P1) `test_supabase_migrations_sql.py` or bootstrap test coverage updated if applicable.

### Где менять код
- `doge-identity-service/supabase/bootstrap/000_full_init.sql`

### Out of scope
- New migration SQL (t01 — already defines schema to fold in)
- Runtime store code (t02–t04)
- IP/UA hashing (SEC-02)

### Проверка
```bash
cd doge-identity-service
grep -E 'phone_verified|oauth_authorization|phone_verification_sessions|phone_audit_events' supabase/bootstrap/000_full_init.sql
python3 -m pytest tests/test_supabase_migrations_sql.py -q
```
