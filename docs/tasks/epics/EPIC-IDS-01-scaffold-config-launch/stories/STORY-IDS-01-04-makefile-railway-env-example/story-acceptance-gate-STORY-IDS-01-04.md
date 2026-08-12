# Story Acceptance Gate — STORY-IDS-01-04

- Story: `STORY-IDS-01-04-makefile-railway-env-example`
- Epic: `EPIC-IDS-01`
- Status: PASS

## Checks

- `make check-env` -> prints `APP_PROFILE`, `PORT`, `SUPABASE_URL`, `SUPABASE_JWT_SECRET`, `AUTHENTIGATE_ISSUER`, `EID_PROVIDER`
- `python3 -m json.tool railpack.json` -> OK
- `.env.example` contains `APP_PROFILE`, `DOGESTONIA_EID_SECRET`, `EID_PROVIDER`, `OIDC_REQUEST_TIMEOUT_S`

## Note

- `make serve` may raise `ImportError` for `core.api.asgi_app` until EPIC-IDS-02; this is expected by EPIC-IDS-01 Story 4 acceptance text.
