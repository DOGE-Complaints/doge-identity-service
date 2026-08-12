# Acceptance verification — task-ids-09-01-t05-mock-eid-flow-offline-tests

- **Gate:** PASS · **File:** `tests/test_eid_verification_flow.py`

| Test | AC |
|------|-----|
| `test_eid_start_creates_session_and_returns_redirect` | #1 |
| `test_mock_callback_verifies_profile_and_me_reflects_status` | #2, #6 |
| `test_mock_callback_replay_is_idempotent` | #3 |
| `test_mock_callback_expired_session_does_not_verify_profile` | #3 |
| `test_mock_callback_profile_hash_conflict_returns_409` | #4 |
