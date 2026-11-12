# Acceptance verification — task-ids-15-01-t01-migration-identity-verified

- **Gate:** PASS
- **Wave:** pkg-000050
- **Story:** STORY-IDS-VB-01-persist-identity-verified
- **Date:** 2026-09-21T20:24:31Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| Migration adds `identity_verified BOOLEAN NOT NULL DEFAULT FALSE` | PASS | [`20260921000001_profiles_identity_verified.sql`](../../../../../../../supabase/migrations/20260921000001_profiles_identity_verified.sql) |
| Bootstrap includes same column | PASS | [`000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) section `[5b]` |
| No `/me` payload change | PASS | VB-02 OOS; `me_response.py` untouched this wave |
| No phone/eID success write hooks | PASS | VB-03 OOS; attach_* unchanged for opaque set |
