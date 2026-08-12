# Acceptance verification — task-ids-10-04-t06-story-acceptance-verification

- **Gate:** PASS (2026-06-11)
- **Wave:** pkg-000025
- **Story:** STORY-IDS-PV-04-profile-flag-migration

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| Миграция добавляет phone-колонки + индекс на `verified_phone_hash` | PASS | t01 — `20260611000001_profiles_phone_verification.sql`; `test_profiles_phone_verification_columns_and_index`, `test_post_historical_migration_file_exists_with_required_sql` |
| `attach_phone_verification` ставит `phone_verified=true` + хэш/префикс/время | PASS | t03/t04 — `repositories.py`, `db_supabase.py`; `test_attach_phone_verification_sets_profile_fields` |
| При `PHONE_ONE_ACCOUNT_PER_NUMBER=true` повтор номера на другом аккаунте → `ProfileConflictError`/409 (тест на дедуп) | PASS | t03/t04 — `test_attach_phone_verification_enforces_unique_hash_when_one_account`, `test_profile_attach_phone_verification_maps_409_to_profile_conflict_error` |
| `/me` отдаёт `phone_verified` и поля | PASS | t05 — `me_response.py`; `test_me_with_phone_verified_profile_returns_phone_fields` |
| Offline-набор зелёный (in-memory + миграционный тест если применимо) | PASS | 288 passed offline |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
# 288 passed; ok 6 paths
```
