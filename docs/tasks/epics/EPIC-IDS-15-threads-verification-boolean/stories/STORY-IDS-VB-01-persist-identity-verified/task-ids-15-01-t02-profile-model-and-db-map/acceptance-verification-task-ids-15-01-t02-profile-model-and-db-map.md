# Acceptance verification — task-ids-15-01-t02-profile-model-and-db-map

- **Gate:** PASS
- **Wave:** pkg-000050
- **Story:** STORY-IDS-VB-01-persist-identity-verified
- **Date:** 2026-09-21T20:24:31Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| `ProfileRecord.identity_verified: bool` | PASS | [`models.py`](../../../../../../../src/core/domain/models.py) field after `phone_verified_at` |
| `_profile_to_row` / `_profile_from_row` include field (default false) | PASS | [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) |
| Constructors/defaults set `identity_verified=False` | PASS | [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py); supabase create paths in `db_supabase.py` |
| No `/me` response field | PASS | VB-02 OOS |
