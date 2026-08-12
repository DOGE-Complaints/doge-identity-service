# Story acceptance gate — STORY-IDS-02-03

- Gate status: **PASS**
- Scope: t01–t03, `pkg-000003`

## Epic AC

| Criterion | Result |
|-----------|--------|
| `StubBearerTokenAuth().validate({})` → `UnauthorizedError` | PASS |
| `validate({"authorization": "Bearer xyz"})` → stub `UserClaims` | PASS |
| `BearerTokenAuth` — Protocol | PASS |
| `UnauthorizedError.code == "AUTHENTICATION_REQUIRED"` | PASS |
| `get_current_user` → `deps.bearer_token_auth.validate` | PASS |

## Note

`asgi_app.py` route wiring — **Story 4** (не входит в flat 6–8). `dependencies.py` — минимальный кэш для dependency injection.
