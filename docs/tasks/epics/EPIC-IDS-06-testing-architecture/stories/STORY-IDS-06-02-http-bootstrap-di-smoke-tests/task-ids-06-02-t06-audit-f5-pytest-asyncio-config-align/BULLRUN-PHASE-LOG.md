# BULLRUN phase log — task-ids-06-02-t06-audit-f5-pytest-asyncio-config-align

| Phase | Status | Notes |
|-------|--------|-------|
| Implement | Done | путь A: removed `asyncio_mode`, `pytest-asyncio` dev dep; epic §6 S2 → TestClient |
| Verify | Done | `pytest -m "not live_integration" -q` → 196 passed |
