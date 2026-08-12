# Acceptance verification — task-ids-09-01-t06-story-acceptance-verification

- **Gate:** PASS (2026-06-02)
- **Wave:** pkg-000015
- **Story:** STORY-IDS-EID-01-eid-verification-flow

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| `POST /auth/eid/start` (JWT) → session `started`, redirect | PASS | `test_eid_start_creates_session_and_returns_redirect` |
| callback → `eid_verified=true`, hash/at in profile | PASS | `test_mock_callback_verifies_profile_and_me_reflects_status`; `attach_eid_verification` in repo |
| replay / expired → no terminal overwrite | PASS | replay + expired tests |
| hash conflict → 409 | PASS | `test_mock_callback_profile_hash_conflict_returns_409` |
| audit without PII | PASS | audit events in start/conflict tests; no subject_hash in audit payload |
| full mock offline flow | PASS | `tests/test_eid_verification_flow.py` |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
# 211 passed, 10 deselected
```
