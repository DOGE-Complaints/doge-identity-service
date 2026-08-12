## Task workspace — `task-ids-11-03-t01-oauth-supabase-migration-sql`

- Story: [`../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md)
- Prerequisite: STORY-IDS-OAUTH-01 🟢 Done (pkg-000029)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000033`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) Scope §миграция; Story AC #1  
---

## Task: implement — Supabase migration for OAuth authorization tables

### Цель
Добавить SQL-миграцию с таблицами `oauth_authorization_requests` (handshake) и `oauth_authorization_codes` (выданные codes) — Story Scope bullet 1.

### Почему это важно
In-memory OAuth state теряется на редеплое; без durable schema нельзя реализовать Supabase-стор (durability MEDIUM из oauth-validation-2026-06-12).

### Факты из кода
1. OAuth codes in-memory: [`repositories.py:452-461`](../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryOAuthTokenService._codes`.
2. Handshake in-memory: [`repositories.py:431-449`](../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryAuthorizationRequestStore`.
3. Последняя миграция: [`20260611000001_profiles_phone_verification.sql`](../../../../../../../supabase/migrations/20260611000001_profiles_phone_verification.sql); OAuth tables **отсутствуют**.
4. RLS/policy pattern: [`20260525000002_create_eid_verification_sessions.sql`](../../../../../../../supabase/migrations/20260525000002_create_eid_verification_sessions.sql).
5. Migration test harness: [`tests/test_supabase_migrations_sql.py`](../../../../../../../tests/test_supabase_migrations_sql.py).

### Gap / Проблема
Нет таблиц `oauth_authorization_requests` / `oauth_authorization_codes` в `supabase/migrations/`.

### AC/DoD
- [x] (P0) Новая миграция `supabase/migrations/20260624000001_oauth_authorization_tables.sql` (timestamp ≥ `20260611000001`).
- [x] (P0) `oauth_authorization_requests`: `oauth_request_id` (PK/unique), `client_id`, `redirect_uri`, `scopes`, `code_challenge`, `code_challenge_method`, `state`, `expires_at`, `created_at`.
- [x] (P0) `oauth_authorization_codes`: `code` UNIQUE, optional `request_id`, `supabase_user_id`, `client_id`, `redirect_uri`, `scopes`, PKCE fields, `expires_at`, `consumed` bool, `created_at`.
- [x] (P0) Index on `expires_at` (cleanup); UNIQUE on `code`; RLS + `service_role` policy (mirror eID sessions).
- [x] (P1) Traceability: Story AC #1 (migration SQL); t05 adds `test_supabase_migrations_sql` entry.

### Где менять код
- `doge-identity-service/supabase/migrations/20260624000001_oauth_authorization_tables.sql` (new)

### Out of scope
- PostgREST repository code (t02, t03)
- DI wiring (t04)
- Refresh tokens / revocation (backlog «Вне scope»)

### Проверка
```bash
cd doge-identity-service
test -f supabase/migrations/20260624000001_oauth_authorization_tables.sql
grep -E 'oauth_authorization_requests|oauth_authorization_codes|expires_at|UNIQUE' supabase/migrations/20260624000001_oauth_authorization_tables.sql
```
