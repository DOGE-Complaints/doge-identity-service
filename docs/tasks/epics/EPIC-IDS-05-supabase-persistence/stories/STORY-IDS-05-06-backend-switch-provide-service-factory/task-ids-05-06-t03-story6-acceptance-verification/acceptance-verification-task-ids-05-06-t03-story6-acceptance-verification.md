# Acceptance verification — task-ids-05-06-t03-story6-acceptance-verification

- **Gate:** PASS (2026-05-31)
- **Wave:** pkg-000006
- **Evidence:** `tests/test_epic_ids_05_integration.py` — Story 6 AC epic L228–231

| AC | Result |
|----|--------|
| `provide_service_factory` → Supabase repos | PASS |
| `build_api_dependencies` supabase → `db_checks` + Supabase profile | PASS |
| Env-only `DB_BACKEND` switch | PASS |
