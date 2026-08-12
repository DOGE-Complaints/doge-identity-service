# BULLRUN-PHASE-LOG

- **Wave:** pkg-000004
- **Skill declared:** python-pro
- **Process:** bullrun-start + run-task (P3 Execute)
- **Date:** 2026-05-29

## Phases

| Phase | Status | Evidence |
|-------|--------|----------|
| Implement | Done | `asgi_app.py` — removed `_config_for_dependencies`; `_cached_dependencies()` → `build_api_dependencies()` |
| Tests | Done | `conftest.py`, transport/security tests — env via monkeypatch |
| Acceptance | Done | `acceptance-verification-task-ids-03-02-t02-asgi-singleton-lifespan-integration.md` |

## Verification command

```bash
cd doge-identity-service && .venv/bin/python -c "
from core.api.asgi_app import get_api_dependencies, _clear_api_dependencies_cache
_clear_api_dependencies_cache()
d1 = get_api_dependencies()
d2 = get_api_dependencies()
assert d1 is d2
print('singleton OK')
"
```
