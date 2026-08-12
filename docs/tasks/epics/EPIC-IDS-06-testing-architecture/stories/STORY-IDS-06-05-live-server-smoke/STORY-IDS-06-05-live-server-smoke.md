# STORY-IDS-06-05: Smoke-тесты против живого сервера

## Meta
- Key: `STORY-IDS-06-05-live-server-smoke`
- Parent Epic: [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md)
- Type: Technical Story (Testing Architecture)
- Status: Done
- Decision Ref: [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 5

## Story Goal
Отдельная директория `tests/smoke/` с `IDENTITY_URL` (port 8100); не входит в default `pytest tests/ -q`.

## AC / DoD (из EPIC-IDS-06 §6 Story 5)
- [x] `IDENTITY_URL=http://localhost:8100 pytest tests/smoke/ -v` — PASSED при запущенном сервере (`make serve`).
- [x] Smoke тесты НЕ входят в `pytest tests/ -q` (`collect_ignore` в `tests/conftest.py`).
- [x] `IDENTITY_URL=https://identity.dogestonia.ee pytest tests/smoke/` — operator Railway check (same module, env-only).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-06-05-t01-smoke-conftest-and-local-server-tests`](./task-ids-06-05-t01-smoke-conftest-and-local-server-tests/README.md) | pkg-000008 |
| 2 | [`task-ids-06-05-t02-story5-acceptance-verification`](./task-ids-06-05-t02-story5-acceptance-verification/README.md) | pkg-000008 |
