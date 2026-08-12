# STORY-IDS-06-03: Live Supabase Integration тесты

## Meta
- Key: `STORY-IDS-06-03-live-supabase-integration`
- Parent Epic: [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md)
- Type: Technical Story (Testing Architecture)
- Status: Done
- Decision Ref: [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 3

## Story Goal
Live integration под `tests/integration/supabase/`: connectivity, schema probes, identity roundtrip; skip без creds, cleanup с UUID4.

## AC / DoD (из EPIC-IDS-06 §6 Story 3)
- [x] Без `.env` с Supabase creds — все `live_integration` тесты SKIPPED (не FAILED).
- [x] С правильными creds (тестового, **не** production проекта) — все тесты PASSED (operator re-run с `SUPABASE_TEST_*` в `.env`).
- [x] После тестов в Supabase **не остаётся** новых profiles/sessions/events с `test-*` префиксами (teardown DELETE в roundtrip-модуле).
- [x] Тесты используют **тестовый** Supabase проект (`SUPABASE_TEST_URL`, не production URL).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-06-03-t01-supabase-connectivity-health-tests`](./task-ids-06-03-t01-supabase-connectivity-health-tests/README.md) | pkg-000008 |
| 2 | [`task-ids-06-03-t02-supabase-identity-roundtrip-tests`](./task-ids-06-03-t02-supabase-identity-roundtrip-tests/README.md) | pkg-000008 |
| 3 | [`task-ids-06-03-t03-story3-acceptance-verification`](./task-ids-06-03-t03-story3-acceptance-verification/README.md) | pkg-000008 |
