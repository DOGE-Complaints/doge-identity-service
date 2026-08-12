# Acceptance verification — task-ids-09-06-t03-callback-redirect-render-accept-negotiate

- **Gate:** PASS (2026-06-09)
- **Wave:** pkg-000019

| Criterion | Result |
|-----------|--------|
| Browser success → `303` on `return_url` with `?eid_status=verified` | PASS — `asgi_app.py` |
| Provider/session error with known `return_url` → `303` with `eid_status=error&eid_error=<EidErrorCode>` | PASS — `asgi_app.py` |
| Unknown session / missing safe `return_url` → 400 JSON, no redirect | PASS — safe fallback in `asgi_app.py` |
| `Accept: application/json` → JSON envelope + `json_status` from outcome | PASS — `Accept` negotiate in `asgi_app.py` |
| Story AC #2, #3 traceability | PASS |
| Offline regression | PASS — `pytest -m "not live_integration" -q` |
