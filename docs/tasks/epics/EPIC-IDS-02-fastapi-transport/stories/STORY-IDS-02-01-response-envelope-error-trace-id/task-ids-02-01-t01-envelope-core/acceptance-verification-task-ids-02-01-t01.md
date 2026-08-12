# Acceptance verification — task-ids-02-01-t01-envelope-core

- **Gate:** PASS
- **Wave:** `pkg-000003`
- **Verified:** 2026-05-29

## Evidence

- `src/core/api/envelope.py` — `build_success_envelope`, `build_error_envelope`, `ensure_trace_id` per [`impl-epic-02-fastapi-transport.md`](../../../../../../tech-requirements/impl-epic-02-fastapi-transport.md) Story 1 Task 1.1.
- `tests/test_api_envelope.py` — AC для success/error envelope и `ensure_trace_id`.
- `cd doge-identity-service && .venv/bin/python -m pytest tests/test_api_envelope.py -q` → **8 passed** (включая t03 scope).

## AC mapping

| AC | Result |
|----|--------|
| `build_success_envelope({"status":"ok"})` → `{"data":{"status":"ok"}}` | PASS |
| `build_error_envelope(..., trace_id="abc")["error"]["trace_id"] == "abc"` | PASS |
| `ensure_trace_id(None)` → valid UUID4 | PASS |
