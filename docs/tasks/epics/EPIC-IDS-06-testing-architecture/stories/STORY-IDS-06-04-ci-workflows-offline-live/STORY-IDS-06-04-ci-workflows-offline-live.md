# STORY-IDS-06-04: CI workflows — offline + live

## Meta
- Key: `STORY-IDS-06-04-ci-workflows-offline-live`
- Parent Epic: [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md)
- Type: Technical Story (Testing Architecture)
- Status: Done
- Decision Ref: [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 4

## Story Goal
GitHub Actions: `test-offline.yml` (каждый push/PR) и `integration-live.yml` (main / workflow_dispatch) + документация test secrets.

## AC / DoD (из EPIC-IDS-06 §6 Story 4)
- [x] `test-offline.yml` запускается на каждый push и PR.
- [x] `integration-live.yml` — только merge в `main` или ручной запуск.
- [x] В offline workflow нет `SUPABASE_*` secrets → live-тесты SKIPPED.
- [x] Offline workflow < 5 минут (setup + install + tests).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-06-04-t01-test-offline-workflow`](./task-ids-06-04-t01-test-offline-workflow/README.md) | pkg-000008 |
| 2 | [`task-ids-06-04-t02-integration-live-workflow-and-secrets-doc`](./task-ids-06-04-t02-integration-live-workflow-and-secrets-doc/README.md) | pkg-000008 |
| 3 | [`task-ids-06-04-t03-story4-acceptance-verification`](./task-ids-06-04-t03-story4-acceptance-verification/README.md) | pkg-000008 |
