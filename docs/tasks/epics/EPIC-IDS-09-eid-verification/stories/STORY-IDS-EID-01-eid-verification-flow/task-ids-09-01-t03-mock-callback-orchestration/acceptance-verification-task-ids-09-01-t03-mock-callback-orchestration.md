# Acceptance verification — task-ids-09-01-t03-mock-callback-orchestration

- **Gate:** PASS

| Criterion | Evidence |
|-----------|----------|
| session-binding via session.supabase_user_id | `handlers.py:handle_auth_eid_callback` |
| attach_eid_verification + hash_secret | same; profile updated in e2e test |
| ProfileConflictError → 409 | `test_mock_callback_profile_hash_conflict_returns_409` |
