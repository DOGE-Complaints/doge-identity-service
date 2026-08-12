## Task workspace — `task-ids-11-03-t05-offline-supabase-oauth-store-tests`

- Story: [`../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md)
- Prerequisite: t02–t04 implemented

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000033`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) Story AC #6  
---

## Task: tests — offline Supabase OAuth store unit tests + migration SQL

### Цель
Покрыть Supabase OAuth stores mock PostgREST-тестами и зарегистрировать миграцию в `test_supabase_migrations_sql`.

### Почему это важно
Story AC #6 требует offline green + migration assert; без mock-тестов регрессии PostgREST mapping не ловятся.

### Факты из кода
1. Migration test lists: [`tests/test_supabase_migrations_sql.py:12-56`](../../../../../../../tests/test_supabase_migrations_sql.py) — `OPERATIONAL_MIGRATIONS` / `POST_HISTORICAL_MIGRATIONS`.
2. Supabase mock patterns: existing tests in `tests/test_supabase_*.py` (httpx mock / `SupabaseDatabase`).
3. In-memory OAuth tests: [`tests/test_oauth_server.py`](../../../../../../../tests/test_oauth_server.py) or equivalent OAUTH-01 offline suite.
4. t01 migration file: `supabase/migrations/20260624000001_oauth_authorization_tables.sql`.

### Gap / Проблема
Нет `test_oauth_supabase_stores.py`; новая миграция не в `test_supabase_migrations_sql`.

### AC/DoD
- [x] (P0) Add migration entry to `test_supabase_migrations_sql.py` (snippets: table names, `expires_at` index, `UNIQUE` on `code`, RLS).
- [x] (P0) New `tests/test_oauth_supabase_stores.py`: mock PostgREST — save/get/consume request; issue code; consume code; expired/consumed paths.
- [x] (P0) DI smoke: `DB_BACKEND=in_memory` existing OAuth tests still pass.
- [x] (P1) Traceability: Story AC #6 (offline + migration SQL test).

### Где менять код
- `doge-identity-service/tests/test_oauth_supabase_stores.py` (new)
- `doge-identity-service/tests/test_supabase_migrations_sql.py`

### Out of scope
- Durability redeploy emulation (t06)
- Live Supabase integration (`live_integration` marker)
- Story gate (t07)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_oauth_supabase_stores.py tests/test_supabase_migrations_sql.py -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
