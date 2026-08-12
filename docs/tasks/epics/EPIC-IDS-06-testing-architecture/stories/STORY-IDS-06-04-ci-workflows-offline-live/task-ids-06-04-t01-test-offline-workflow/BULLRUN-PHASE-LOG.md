# BULLRUN-PHASE-LOG

- **Wave:** pkg-000008
- **Process:** P3 Execute STORY-IDS-06-04 t01
- **Date:** 2026-06-02

| Phase | Status | Evidence |
|-------|--------|----------|
| Tests | Done | `.github/workflows/test-offline.yml` — push/PR, Python 3.11, junit artifact |

```bash
cd doge-identity-service && .venv/bin/python -m pytest -q -m "not live_integration" --tb=short
```
