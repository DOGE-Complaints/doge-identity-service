# Acceptance verification — task-ids-09-01-t01-handle-auth-eid-start-orchestration

- **Wave:** pkg-000015 · **Date:** 2026-06-02 · **Gate:** PASS

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| start orchestration + session started | PASS | `handlers.py:handle_auth_eid_start`; `test_eid_start_creates_session_and_returns_redirect` |
| validate_return_url preserved | PASS | `test_auth_eid_start_rejects_foreign_return_url` |
| audit eid_verification_started | PASS | `test_eid_start_creates_session_and_returns_redirect` — list_events |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q tests/test_eid_verification_flow.py::test_eid_start_creates_session_and_returns_redirect
```
