# SEC-03 JWT `aud` decision record (2026-06-26)

**Story:** STORY-IDS-SEC-03-jwt-validation-hardening · **Gap:** G-5

## Decision

**Validate `aud=authenticated`** in `SupabaseJwtValidatorImpl` via `JWTClaimsRegistry` (`aud` essential, value `authenticated`).

## Evidence

| Source | Finding |
|--------|---------|
| [`09-supabase-jwt-validation.md:43`](../requirements/09-supabase-jwt-validation.md) | Target requirement: `aud=authenticated` |
| [`supabase_validator.py`](../../src/core/auth/supabase_validator.py) (pre-SEC-03) | `aud` not in registry; `role` checked separately |
| [`test_supabase_jwt_validator.py`](../../tests/test_supabase_jwt_validator.py) | Synthetic tokens use `aud=authenticated`; offline rejects wrong/missing `aud` after SEC-03 |
| Supabase GoTrue (user access JWT) | Standard user session tokens carry `aud: "authenticated"` (distinct from `role`) |
| Live sanity | [`test_supabase_jwt_live_sanity.py`](../../tests/integration/supabase/test_supabase_jwt_live_sanity.py) — runs when operator sets `SUPABASE_TEST_ACCESS_TOKEN` + JWT secret in `.env`; skipped locally without token |

## Key import decision

**Raw string:** `OctKey.import_key(jwt_secret)` — matches Supabase HS256 signing. Base64url JWK wrapper does not verify tokens signed with the raw secret ([`test_b64url_wrapped_key_import_fails_on_raw_signed_token`](../../tests/test_supabase_jwt_validator.py)).

## Waiver not chosen

Intentional skip of `aud` validation rejected: spec 09 target + defense-in-depth vs tokens minted for other audiences.
