# Acceptance verification — task-ids-15-01-t04-offline-persist-tests

- **Gate:** PASS
- **Wave:** pkg-000050
- **Story:** STORY-IDS-VB-01-persist-identity-verified
- **Date:** 2026-09-21T20:24:31Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| Default false | PASS | [`tests/test_identity_verified_persist.py`](../../../../../../../tests/test_identity_verified_persist.py) `test_identity_verified_defaults_false_on_new_profile` |
| Map round-trip | PASS | `test_identity_verified_map_round_trip_false_and_true` + missing-key default |
| Backfill semantics | PASS | `test_backfill_semantics_method_or_to_opaque` + `test_backfill_migration_sql_on_disk` |
| Suite `-m "not live_integration"` green | PASS | 450 passed, 13 deselected (2026-09-21T20:24:31Z) |
