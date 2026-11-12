# Run summary — EPIC-IDS-04 Story 06 (pkg-000005)

- **Date:** 2026-05-30
- **Story:** STORY-IDS-04-06-provide-factory-di-integration
- **Tasks:** t01–t03
- **Gate:** PASS
- **pytest:** 102 passed (`pytest -m "not live_integration"`)

## Runtime files

- `src/core/infrastructure/providers.py`
- `src/core/api/dependencies.py`
- `tests/test_epic_ids_04_integration.py`

## Test adjustments (factory wiring)

- `tests/test_api_dependencies.py` — integration expectations
- `tests/test_asgi_transport.py` — valid demo JWT for `/me` stub path
- `tests/test_security_primitives.py` — `get_current_user` with real bearer auth
