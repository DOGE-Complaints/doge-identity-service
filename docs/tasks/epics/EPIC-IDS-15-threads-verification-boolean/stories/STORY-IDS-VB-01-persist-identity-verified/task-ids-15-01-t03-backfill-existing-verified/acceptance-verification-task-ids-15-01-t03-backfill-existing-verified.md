# Acceptance verification — task-ids-15-01-t03-backfill-existing-verified

- **Gate:** PASS
- **Wave:** pkg-000050
- **Story:** STORY-IDS-VB-01-persist-identity-verified
- **Date:** 2026-09-21T20:24:31Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| One-shot SQL sets opaque true where phone OR eid | PASS | [`20260921000002_profiles_identity_verified_backfill.sql`](../../../../../../../supabase/migrations/20260921000002_profiles_identity_verified_backfill.sql) |
| Neither method → remains false (default) | PASS | UPDATE WHERE only; column DEFAULT FALSE |
| No clear-on-failure introduced | PASS | No failure-path clear logic; VB-03 owns success writers |
| Bootstrap parity | PASS | [`000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) `[5b]` includes same UPDATE |
