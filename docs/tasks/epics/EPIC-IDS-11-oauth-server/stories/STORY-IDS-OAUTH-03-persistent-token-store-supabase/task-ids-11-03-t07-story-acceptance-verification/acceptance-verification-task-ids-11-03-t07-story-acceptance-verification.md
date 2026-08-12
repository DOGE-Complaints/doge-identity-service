# Acceptance verification — task-ids-11-03-t07-story-acceptance-verification

- **Gate:** PASS
- **Date:** 2026-06-24
- **Wave:** pkg-000033
- **Story:** STORY-IDS-OAUTH-03-persistent-token-store-supabase

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| Миграция создаёт `oauth_authorization_requests` + `oauth_authorization_codes` (TTL-индекс, single-use) | PASS | `supabase/migrations/20260624000001_oauth_authorization_tables.sql`; `tests/test_supabase_migrations_sql.py` POST_HISTORICAL entry |
| `SupabaseOAuthTokenService` реализует контракт + хранение request-state; single-use/TTL в БД | PASS | `SupabaseAuthorizationRequestStore` + `SupabaseOAuthTokenService` in `db_supabase.py`; atomic PATCH consume |
| `DB_BACKEND=supabase` → Supabase-стор; `in_memory` → прежний | PASS | `providers.py` backend branch; `tests/test_epic_ids_05_integration.py` |
| Durability-тест: code валиден после пересоздания стора; expired/consumed → `invalid_grant` | PASS | `tests/test_oauth_supabase_stores.py` — durability + expired/consumed |
| Access-токен валиден после пересоздания стора без обращения к БД | PASS | `tests/test_oauth_supabase_stores.py::test_stateless_access_token_validates_without_db_reads` |
| Offline-тесты + `test_supabase_migrations_sql` | PASS | `tests/test_oauth_supabase_stores.py` (7 tests); 359 pytest offline green |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
# 359 passed; ok 7 paths
```
