# Acceptance verification — task-ids-02-03-t01

- **Gate:** PASS (2026-05-29)

## Evidence

- `src/core/api/security.py` — `UnauthorizedError`, `BearerTokenAuth` (`Protocol`), `UserClaims`
- `tests/test_security_primitives.py::test_unauthorized_error_code`, `test_bearer_token_auth_is_protocol`
