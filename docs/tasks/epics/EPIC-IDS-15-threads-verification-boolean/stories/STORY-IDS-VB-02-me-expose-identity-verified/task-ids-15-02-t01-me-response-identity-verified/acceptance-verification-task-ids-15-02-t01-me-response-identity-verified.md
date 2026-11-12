# Acceptance verification — task-ids-15-02-t01-me-response-identity-verified

- **Gate:** PASS
- **Wave:** pkg-000051
- **Story:** STORY-IDS-VB-02-me-expose-identity-verified
- **Date:** 2026-09-21T20:40:59Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| `build_me_data` always includes `identity_verified` (default false) | PASS | [`me_response.py:35`](../../../../../../../src/core/api/me_response.py) |
| With profile: from `profile.identity_verified` | PASS | [`me_response.py:51`](../../../../../../../src/core/api/me_response.py) |
| Legacy method flags still present | PASS | `phone_verified` / `eid_verified` defaults + profile copy unchanged |
| No new `/me` route; account_status not verified boolean | PASS | `asgi_app.py:302` sole `@app.get("/me")`; `account_status` still `"active"` |
