# Story acceptance gate — STORY-IDS-02-04

- Gate status: **PASS** (2026-05-29)
- Evidence: `tests/test_asgi_transport.py` — title, trace-id, `/me` 401, CORS OPTIONS; `src/core/api/asgi_app.py`

| Epic AC | Test / file |
|---------|-------------|
| `app.title == "doge-identity-service"` | `test_app_title` |
| `x-trace-id` → `data.trace_id` | `test_health_propagates_x_trace_id` |
| `GET /me` без auth → 401 | `test_me_without_auth_returns_401` |
| CORS in `create_app` | `create_app` + CORSMiddleware |
| Lifespan + `get_api_dependencies` | `_lifespan` in `asgi_app.py` |
| `_clear_api_dependencies_cache` | `asgi_app.py` + `conftest.py` |
