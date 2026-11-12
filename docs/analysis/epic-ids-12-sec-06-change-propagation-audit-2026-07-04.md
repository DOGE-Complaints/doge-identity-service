# EPIC-IDS-12 SEC-06 — change-propagation audit (t01)

**Date:** 2026-07-04  
**Story:** STORY-IDS-SEC-06-supabase-jwks-es256-hardening  
**Decision:** D-1 JWKS-only, D-2 real URL gate, D-5 remove `SUPABASE_JWT_SECRET`

## src/ consumers (remove)

| Symbol / pattern | Path |
|------------------|------|
| `_validate_hs256`, `OctKey`, `jwt_secret` | `src/core/auth/supabase_validator.py` |
| `demo.local` heuristic | `src/core/auth/supabase_validator.py:51` |
| `test-secret-for-demo`, `supabase_jwt_secret` | `src/core/infrastructure/providers.py:109-110` |
| `supabase_jwt_secret` field, load, pilot-required | `src/core/config/schema.py:34,160,190,215` |

## src/ excluded (keep)

| Path | Reason |
|------|--------|
| `src/core/oauth/access_token_jwt.py` | OAuth access-token HS256 (`OAUTH_ACCESS_TOKEN_SECRET`) |

## tests/ HS256 Supabase minters (migrate t05)

- `tests/test_supabase_jwt_validator.py`
- `tests/test_supabase_jwt_auth.py`
- `tests/test_me_profile.py`
- `tests/test_phone_verification_flow.py`
- `tests/test_audit_ip_ua_hashing.py`
- `tests/test_eid_callback_redirect.py`
- `tests/test_eid_verification_flow.py`
- `tests/test_oauth_introspection.py`
- `tests/test_oauth_server_flow.py`
- `tests/test_epic_ids_04_integration.py`
- `tests/test_asgi_transport.py`
- `tests/test_http_transport_smoke.py`
- `tests/test_canonical_provider_contract.py`
- `tests/test_security_primitives.py`
- `tests/test_rate_limiting.py`
- `tests/conftest.py` (`SUPABASE_JWT_SECRET` autouse)

## tests/ config fixtures (t04)

- `tests/test_config_schema.py` (pilot-required)
- `tests/test_service_factory.py`, `test_inmemory_repositories.py`, `test_eid_providers.py`, `tests/test_oauth_supabase_stores.py` (`supabase_jwt_secret` in AppConfig kwargs)

## live integration (coordinate, not offline gate)

- `tests/integration/supabase/conftest.py` — JWT creds helper
- `tests/integration/supabase/test_supabase_jwt_live_sanity.py`

## docs (t07)

- `.env.example`
- `docs/requirements/07-env-configuration-spec.md`
- `docs/requirements/09-supabase-jwt-validation.md`
- `docs/runtime-docs/04-security.md`
- `docs/runbook/supabase-project-setup.md`
- `docs/runbook/run-and-healthcheck.md`
- `tests/test_supabase_runbook_docs.py`

## Migration order (approved)

1. t02 — JWKS-only validator  
2. t03 — DI `JwksCache` in `providers.py`  
3. t04 — remove `SUPABASE_JWT_SECRET` from schema/env  
4. t05 — `tests/supabase_jwt_harness.py` + migrate 14 files + conftest  
5. t06 — validator ES256/JWKS unit tests  
6. t07 — docs sync  
7. t08 — story gate greps + full offline pytest  
