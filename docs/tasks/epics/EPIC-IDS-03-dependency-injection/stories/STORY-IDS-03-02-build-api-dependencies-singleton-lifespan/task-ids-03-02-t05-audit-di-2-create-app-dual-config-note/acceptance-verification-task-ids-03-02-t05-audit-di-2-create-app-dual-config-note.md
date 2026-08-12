# Acceptance verification — task-ids-03-02-t05-audit-di-2-create-app-dual-config-note

- **Gate:** PASS
- **Wave:** `override epic_ids_03_audit_2026_05_28`
- **Verified:** 2026-05-29
- **Audit finding:** DI-2

## Evidence

- `src/core/api/asgi_app.py::create_app` — docstring documents CORS-only `config` vs env-driven DI
- `pytest tests/ -q -m "not live_integration"` → 56 passed (no behavior change)

## Audit DI-2

Closed — dual-config footgun documented in runtime code.
