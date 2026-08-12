# BULLRUN-PHASE-LOG

- **Wave:** pkg-000011
- **Process:** P3 Execute STORY-IDS-CLEANUP-01 t02
- **Date:** 2026-06-05

| Phase | Status | Evidence |
|-------|--------|----------|
| Implement | Done | Removed 4 POST handlers + `PROTECTED_OPTIONS_PATHS` entries from `asgi_app.py` |
| Verify | Done | `rg "story-drafts|submit-story" src/core/api/asgi_app.py` → 0 matches |

```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_asgi_transport.py tests/test_http_transport_smoke.py -q
# passed
```
