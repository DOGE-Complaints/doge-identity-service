# Acceptance verification — task-ids-06-01-t02-story1-acceptance-verification

- **Gate:** PASS (2026-06-02)
- **Wave:** pkg-000008
- **Evidence:** `tests/test_conftest_env_isolation.py` (4 passed); offline suite 160 passed / 2 deselected

| AC (epic L144–149) | Result |
|--------------------|--------|
| `pytest tests/ -q` без `.env` — `DB_BACKEND=in_memory`, `EID_PROVIDER=mock` | PASS — `test_autouse_sets_in_memory_and_mock_eid` + full suite |
| `pytest tests/ -q` с `.env` supabase+creds — in_memory (env перезаписан) | PASS — `test_provide_app_config_stays_in_memory_when_dotenv_has_supabase` |
| `tests/integration/supabase/*.py` auto `live_integration` | PASS — `test_auto_marker_applied_via_collection_hook` |
| `pytest -m "not live_integration" -q` пропускает Supabase | PASS — 2 deselected in integration/supabase |
| monkeypatch после autouse переопределяет env | PASS — `test_monkeypatch_can_override_autouse_env` |
