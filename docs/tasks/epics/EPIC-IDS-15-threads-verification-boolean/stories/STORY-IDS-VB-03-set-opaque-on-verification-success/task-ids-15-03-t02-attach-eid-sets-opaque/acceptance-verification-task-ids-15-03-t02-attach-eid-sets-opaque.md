# Acceptance verification — task-ids-15-03-t02-attach-eid-sets-opaque

- **Gate:** PASS
- **Wave:** pkg-000052
- **Story:** STORY-IDS-VB-03-set-opaque-on-verification-success
- **Date:** 2026-09-21T20:51:27Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| In-memory eID attach success → opaque true | PASS | [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py) replace `identity_verified=True` |
| Supabase eID attach success → opaque true | PASS | [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) PATCH + create/replace |
| eID method flags unchanged aside from opaque | PASS | eid_verified/provider/method/country still set |
