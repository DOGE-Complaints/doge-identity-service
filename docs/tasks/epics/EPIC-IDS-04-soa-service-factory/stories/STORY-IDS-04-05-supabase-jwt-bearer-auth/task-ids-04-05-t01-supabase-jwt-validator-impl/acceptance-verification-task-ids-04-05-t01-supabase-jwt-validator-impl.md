# Acceptance verification — task-ids-04-05-t01-supabase-jwt-validator-impl

- **Gate:** PASS (2026-05-30)
- **Wave:** pkg-000005
- **Evidence:** `src/core/auth/supabase_validator.py` — `SupabaseJwtValidatorImpl` with joserfc HS256, `JWTClaimsRegistry` for iss/sub/exp, role check; re-exports `UserClaims`, `JwtValidationError` from domain
