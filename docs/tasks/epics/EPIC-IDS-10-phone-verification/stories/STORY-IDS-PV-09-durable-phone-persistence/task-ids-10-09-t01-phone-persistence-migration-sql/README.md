## Task workspace — `task-ids-10-09-t01-phone-persistence-migration-sql`

- Story: [`../STORY-IDS-PV-09-durable-phone-persistence.md`](../STORY-IDS-PV-09-durable-phone-persistence.md)
- Prerequisite: STORY-IDS-PV-03 🟢 Done (pkg-000024); STORY-IDS-PV-04 🟢 Done (pkg-000025)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000039`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md) Scope §«Миграция(и) Supabase»; Story AC #5  
---

## Task: implement — Supabase migration for phone persistence tables

### Цель
Добавить SQL-миграцию с таблицами `phone_verification_sessions` и `phone_audit_events` — Story Scope bullet «Миграция(и) Supabase».

### Почему это важно
Phone session store и audit repo in-memory only; без durable schema нельзя закрыть G-3/G-2a из identity-backend-full-audit.

### Факты из кода
1. Phone session in-memory: [`repositories.py:284+`](../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryPhoneVerificationSessionStore`.
2. Phone audit in-memory: [`repositories.py:362+`](../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryPhoneAuditLogRepository`.
3. Контракт session store: [`contracts.py:74-93`](../../../../../../../src/core/domain/contracts.py) — `PhoneVerificationSessionStore`.
4. Контракт audit repo: [`contracts.py:97-106`](../../../../../../../src/core/domain/contracts.py) — `PhoneAuditLogRepository`.
5. RLS/policy pattern: [`20260525000003_create_eid_audit_events.sql`](../../../../../../../supabase/migrations/20260525000003_create_eid_audit_events.sql).
6. OAuth migration precedent: [`20260624000001_oauth_authorization_tables.sql`](../../../../../../../supabase/migrations/20260624000001_oauth_authorization_tables.sql).
7. Migration test harness: [`tests/test_supabase_migrations_sql.py`](../../../../../../../tests/test_supabase_migrations_sql.py).
8. **Нет** `phone_*` tables в [`supabase/migrations/`](../../../../../../../supabase/migrations/).

### Gap / Проблема
Нет таблиц `phone_verification_sessions` / `phone_audit_events` в `supabase/migrations/`.

### AC/DoD
- [x] (P0) Новая timestamped миграция в `supabase/migrations/` (timestamp ≥ последней существующей).
- [x] (P0) `phone_verification_sessions`: колонки для полей `PhoneVerificationSession` + `expires_at`, status, indexes (incl. `expires_at` для cleanup).
- [x] (P0) `phone_audit_events`: колонки для `PhoneAuditEvent` incl. optional `ip_hash`/`user_agent_hash` (storage only); index по времени.
- [x] (P0) RLS + `service_role` policy (mirror `eid_audit_events` / OAuth tables).
- [x] (P1) Traceability: Story AC #5 — entry in `test_supabase_migrations_sql.py`.

### Где менять код
- `doge-identity-service/supabase/migrations/` (new SQL file)
- `doge-identity-service/tests/test_supabase_migrations_sql.py`

### Out of scope
- IP/UA hashing content (SEC-02 scope)
- Supabase store implementations (t02, t03)
- DI wiring (t04)
- Bootstrap parity (t05)

### Проверка
```bash
cd doge-identity-service
test -f supabase/migrations/*phone*.sql || ls supabase/migrations/
grep -E 'phone_verification_sessions|phone_audit_events|expires_at|RLS' supabase/migrations/*.sql
python3 -m pytest tests/test_supabase_migrations_sql.py -q
```
