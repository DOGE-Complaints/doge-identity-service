# Story acceptance gate — STORY-IDS-03-02

- Story: `STORY-IDS-03-02-build-api-dependencies-singleton-lifespan`
- Gate status: **PASS** (2026-05-29)
- Scope: tasks t01–t03, `pkg-000004`

## Epic AC (EPIC-IDS-03 §6 Story 2)

| Criterion | Result | Evidence |
|-----------|--------|----------|
| `get_api_dependencies() is get_api_dependencies()` | PASS | `tests/test_api_dependencies.py::test_get_api_dependencies_is_singleton` |
| cache clear → new `id()` | PASS | `tests/test_api_dependencies.py::test_clear_cache_creates_new_singleton` |
| monkeypatch LOG_LEVEL + cache clear | PASS | `tests/test_api_dependencies.py::test_monkeypatch_log_level_reloads_config` |
| startup configure_logging | PASS | `tests/test_api_dependencies.py::test_lifespan_configures_logging` |
| parallel HTTP same ApiDependencies | PASS | `tests/test_api_dependencies.py::test_parallel_requests_share_same_dependencies` |

## Task reports

- [t01 acceptance](./task-ids-03-02-t01-build-api-dependencies-factory/acceptance-verification-task-ids-03-02-t01-build-api-dependencies-factory.md)
- [t02 acceptance](./task-ids-03-02-t02-asgi-singleton-lifespan-integration/acceptance-verification-task-ids-03-02-t02-asgi-singleton-lifespan-integration.md)
- [t03 acceptance](./task-ids-03-02-t03-singleton-behavior-verification/acceptance-verification-task-ids-03-02-t03-singleton-behavior-verification.md)

## Verify

`python3 docs/methodology/builder-queue/builder_resolve_queue.py --project identity --verify` → `ok 7 paths`
