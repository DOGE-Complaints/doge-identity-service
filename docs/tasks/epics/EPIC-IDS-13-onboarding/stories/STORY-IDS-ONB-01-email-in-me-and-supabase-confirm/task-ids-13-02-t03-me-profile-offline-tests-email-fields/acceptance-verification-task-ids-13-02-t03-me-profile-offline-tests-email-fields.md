# Acceptance verification — task-ids-13-02-t03-me-profile-offline-tests-email-fields

- **Gate:** PASS
- **Wave:** pkg-000045
- **Story:** STORY-IDS-ONB-01-email-in-me-and-supabase-confirm
- **Date:** 2026-07-24T18:57:53Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| Default JWT email: `data["email"]` == claim; `email_verified is True` | PASS | `test_me_with_valid_jwt_and_profile_returns_200_envelope`; missing-profile asserts |
| Без email claim: `email is None`; `email_verified is True` | PASS | `test_me_email_null_when_jwt_has_no_email_claim` |
| AUTHCORE-02 asserts intact | PASS | `created_at` / `account_status` в profile + missing-profile tests |
| `pytest tests/test_me_profile.py -q` | PASS | 6 passed |
| Offline suite `-m "not live_integration"` | PASS | 406 passed, 12 deselected |
