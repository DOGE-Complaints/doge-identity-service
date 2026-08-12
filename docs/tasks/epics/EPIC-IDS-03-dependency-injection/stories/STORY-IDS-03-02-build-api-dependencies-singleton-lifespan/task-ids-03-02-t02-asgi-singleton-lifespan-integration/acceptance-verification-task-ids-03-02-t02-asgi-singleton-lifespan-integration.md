# Acceptance verification — task-ids-03-02-t02-asgi-singleton-lifespan-integration

- **Gate:** PASS (2026-05-29)
- **Wave:** pkg-000004
- **Evidence:** `asgi_app.py:46-48` `_cached_dependencies()` → `build_api_dependencies()`; `__init__.py` exports `build_api_dependencies`
