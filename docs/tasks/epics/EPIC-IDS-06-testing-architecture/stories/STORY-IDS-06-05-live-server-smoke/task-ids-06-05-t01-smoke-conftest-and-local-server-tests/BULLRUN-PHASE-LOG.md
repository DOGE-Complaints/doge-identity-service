# BULLRUN-PHASE-LOG

- **Wave:** pkg-000008
- **Process:** P3 Execute STORY-IDS-06-05 t01
- **Date:** 2026-06-02

| Phase | Status | Evidence |
|-------|--------|----------|
| Tests | Done | `tests/smoke/conftest.py`, `test_local_server_smoke.py`; `collect_ignore` in `tests/conftest.py` |

```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_smoke_collection_contract.py -q
IDENTITY_URL=http://localhost:8100 .venv/bin/python -m pytest tests/smoke/ -v
```
