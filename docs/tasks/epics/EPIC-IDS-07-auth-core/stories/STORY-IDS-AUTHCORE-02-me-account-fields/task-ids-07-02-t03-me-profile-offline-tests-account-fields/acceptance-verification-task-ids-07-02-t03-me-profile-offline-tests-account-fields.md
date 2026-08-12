# Acceptance verification — task-ids-07-02-t03-me-profile-offline-tests-account-fields

- **Gate:** PASS
- **Wave:** pkg-000044
- **Story:** STORY-IDS-AUTHCORE-02-me-account-fields

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| С профилем: ISO created_at + account_status active | PASS | `test_me_with_valid_jwt_and_profile_returns_200_envelope` |
| Без профиля: created_at null + account_status active | PASS | `test_me_missing_profile_returns_200_not_verified_no_db_write` |
| test_me_profile.py green | PASS | 5 passed |
| offline suite green | PASS | 405 passed, 12 deselected |
