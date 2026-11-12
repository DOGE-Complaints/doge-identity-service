# Run summary — EPIC-IDS-06 audit gaps P3 Execute

- **Date:** 2026-06-02
- **run_mode:** `epic_ids_06_audit_2026_06_02`
- **pkg (unchanged):** `pkg-000008-20260602-epic-ids-06-testing-architecture.yaml`

## Outcome

| Gap | Result |
|-----|--------|
| F1 | lazy `core.api.asgi_app:app` + `tests/test_asgi_import_config_isolation.py` |
| F2 | epic §6 S5 / §8 doc → `collect_ignore` |
| F3 | `tests/integration/__init__.py`, `tests/smoke/__init__.py` |
| F4 | smoke marker SSOT in `pyproject.toml` only |
| F5 | removed dead `pytest-asyncio` config; epic §6 S2 TestClient |

## Verification

```text
pytest -m "not live_integration" -q  → 196 passed, 10 deselected
DB_BACKEND=supabase SUPABASE_URL=... collect-only bootstrap  → OK
```

## Next

P8 commits (runtime + `.github/` + audit gap code; `docs/tasks/**` optional per operator).
