# Story acceptance gate — STORY-IDS-02-05

- Gate status: **PASS** (2026-05-29)
- Evidence: `handlers.py`, `asgi_app.py` routes, `tests/test_asgi_transport.py`

| Epic AC | Test |
|---------|------|
| `GET /health` → `data.status == "ok"` | `test_health_returns_ok_envelope` |
| `GET /ready` in_memory | `test_ready_in_memory_backend` |
| `GET /me` Bearer → 501 NOT_IMPLEMENTED | `test_me_with_bearer_returns_501_stub` |
| `OPTIONS /me` → 200 | `test_options_me_returns_200` |
| Route table 14 paths | `test_route_table_contains_identity_contract_paths` |
