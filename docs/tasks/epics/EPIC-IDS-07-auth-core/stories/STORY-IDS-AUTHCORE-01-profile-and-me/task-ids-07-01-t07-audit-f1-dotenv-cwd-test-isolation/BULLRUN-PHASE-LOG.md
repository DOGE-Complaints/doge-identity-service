# BULLRUN-PHASE-LOG

- **Wave:** pkg-000010
- **Process:** P3 Execute gap F1
- **Date:** 2026-06-05

| Phase | Status | Evidence |
|-------|--------|----------|
| Fix | Done | `monkeypatch.chdir(tmp_path)` in isolation test |

**Решение:** изоляция теста от cwd `.env` через `tmp_path` (без изменения `merge_dotenv_from_cwd` в prod).

```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_asgi_import_config_isolation.py -q
.venv/bin/python -m pytest -m "not live_integration" -q
# 200 passed
```
