# BULLRUN-PHASE-LOG — t02–t05 (pkg-000015)

- **Wave:** pkg-000015 · **Date:** 2026-06-02

| Task | Status | Evidence |
|------|--------|----------|
| t02 asgi wire | PASS | `asgi_app.py` — `_eid_start_payload_from_request`, `handle_auth_eid_start` |
| t03 mock callback | PASS | `handle_auth_eid_callback`; mock route wired |
| t04 lifecycle + audit | PASS | consumed/replay/expired; audit events in handlers |
| t05 offline tests | PASS | `tests/test_eid_verification_flow.py` (5 tests) |
