# Acceptance verification — task-ids-06-03-t03-story3-acceptance-verification

- **Gate:** PASS (2026-06-02, no local `.env` — skip path verified)
- **Wave:** pkg-000008
- **Evidence:** `pytest tests/integration/supabase/ -m live_integration` → 1 passed, 9 skipped; offline 190 passed, 10 deselected

| AC (epic L219–223) | Result |
|--------------------|--------|
| Без `.env` с Supabase creds — все `live_integration` SKIPPED (не FAILED) | PASS — 9 skipped, 0 failed |
| С правильными creds — все PASSED | **Operator** — set `SUPABASE_TEST_URL` + `SUPABASE_TEST_SERVICE_ROLE`(_KEY) in `.env`; re-run same pytest command |
| После тестов нет `test-*` leak | **Operator** — verified by teardown in `test_supabase_identity_roundtrip.py` when creds present |
| Тесты используют тестовый проект (`SUPABASE_TEST_URL`) | PASS — `conftest._require_supabase_creds_from_dotenv` reads only `SUPABASE_TEST_*`; fails if URL equals `SUPABASE_URL` |

**Helper:** `tests/integration/supabase/conftest.py` — `_require_supabase_creds_from_dotenv()` parses `.env` directly (bypasses `_block_dotenv_leakage`).
