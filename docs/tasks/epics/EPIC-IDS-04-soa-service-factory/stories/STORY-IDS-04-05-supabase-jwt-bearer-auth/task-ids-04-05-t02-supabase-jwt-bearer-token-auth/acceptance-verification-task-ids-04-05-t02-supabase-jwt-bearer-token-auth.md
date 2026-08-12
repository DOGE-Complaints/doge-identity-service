# Acceptance verification — task-ids-04-05-t02-supabase-jwt-bearer-token-auth

- **Gate:** PASS (2026-05-30)
- **Wave:** pkg-000005
- **Evidence:** `src/core/api/security.py` — `SupabaseJwtBearerTokenAuth` delegates to validator; `JwtValidationError` → `UnauthorizedError(code="AUTHENTICATION_REQUIRED")`; `StubBearerTokenAuth` preserved; `get_current_user` uses `deps.bearer_token_auth`
