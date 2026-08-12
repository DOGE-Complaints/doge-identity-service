# Acceptance verification — task-ids-02-03-t02

- **Gate:** PASS (2026-05-29)

## Evidence

- `StubBearerTokenAuth`, `get_current_user` in `security.py`
- `dependencies.py` — `ApiDependencies.bearer_token_auth`, `get_api_dependencies()`
- Tests: `test_stub_validate_*`, `test_get_current_user_uses_deps_bearer_auth`
