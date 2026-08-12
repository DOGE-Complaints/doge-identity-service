# Story acceptance gate — STORY-IDS-03-03

- Story: `STORY-IDS-03-03-epic-ids-04-extension-hook-contract`
- Gate status: **PASS** (2026-05-29)
- Scope: tasks t01–t02, `pkg-000004`

## Epic AC (EPIC-IDS-03 §6 Story 3)

| Criterion | Result | Evidence |
|-----------|--------|----------|
| `# TODO EPIC-IDS-04` над `StubBearerTokenAuth()` | PASS | `dependencies.py:63` |
| `# TODO EPIC-IDS-05` над `db_checks` | PASS | `dependencies.py:58` |
| Поля Story 1 = EPIC-IDS-04 factory getters | PASS | `EPIC_IDS_04_OPTIONAL_FIELDS` + `test_epic_ids_04_optional_fields_match_factory_getters` |

## Task reports

- [t01 acceptance](./task-ids-03-03-t01-todo-epic-hooks-in-build-factory/acceptance-verification-task-ids-03-03-t01-todo-epic-hooks-in-build-factory.md)
- [t02 acceptance](./task-ids-03-03-t02-contract-field-list-alignment/acceptance-verification-task-ids-03-03-t02-contract-field-list-alignment.md)

## Verify

`python3 docs/methodology/builder-queue/builder_resolve_queue.py --project identity --verify` → `ok 7 paths`
