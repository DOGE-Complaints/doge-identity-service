# STORY-IDS-03-03: Hook расширения для EPIC-IDS-04 — контракт

## Meta
- Key: `STORY-IDS-03-03-epic-ids-04-extension-hook-contract`
- Parent Epic: [`../../../EPIC-IDS-03-dependency-injection.md`](../../../EPIC-IDS-03-dependency-injection.md)
- Type: Technical Story (DI Contract)
- Status: Done
- Decision Ref: [`../../../EPIC-IDS-03-dependency-injection.md`](../../../EPIC-IDS-03-dependency-injection.md) §6 Story 3

## Story Goal
Зафиксировать документационный контракт интеграции `build_api_dependencies()` с `provide_service_factory()` (EPIC-IDS-04) через TODO-маркеры и закомментированный target block.

## AC / DoD (из EPIC-IDS-03)
- [x] В EPIC-IDS-03 — комментарии `# TODO EPIC-IDS-04: replace with provide_service_factory(...)` стоят над хардкодным `StubBearerTokenAuth()`.
- [x] В EPIC-IDS-03 — комментарии `# TODO EPIC-IDS-05: run 5-level Supabase healthchecks` стоят над `db_checks: dict[str, bool] = {}`.
- [x] Список целевых полей в Story 1 совпадает с тем, что EPIC-IDS-04 реализует через `provide_service_factory`.

## Field alignment checklist (t02)

| Epic §3 optional field | Dataclass | Factory getter (commented block) |
|------------------------|-----------|----------------------------------|
| `supabase_jwt_validator` | yes | `get_supabase_jwt_validator()` |
| `profile_repository` | yes | `get_profile_repository()` |
| `verification_session_store` | yes | `get_verification_session_store()` |
| `eid_audit_log_repository` | yes | `get_eid_audit_log_repository()` |
| `eid_provider_registry` | yes | `get_eid_provider_registry()` |
| `oauth_client_store` | yes | `get_oauth_client_store()` |
| `oauth_token_service` | yes | `get_oauth_token_service()` |
| `story_draft_repository` | yes | `get_story_draft_repository()` |

SSOT constant: `EPIC_IDS_04_OPTIONAL_FIELDS` in [`dependencies.py`](../../../../../../src/core/api/dependencies.py).

## Story gate
- [story-acceptance-gate-STORY-IDS-03-03.md](./story-acceptance-gate-STORY-IDS-03-03.md) — **PASS** (2026-05-29)

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-03-03-t01-todo-epic-hooks-in-build-factory`](./task-ids-03-03-t01-todo-epic-hooks-in-build-factory/README.md) | pkg-000004 |
| 2 | [`task-ids-03-03-t02-contract-field-list-alignment`](./task-ids-03-03-t02-contract-field-list-alignment/README.md) | pkg-000004 |
| 3 | [`task-ids-03-03-t03-audit-di-3-unreachable-block-lint`](./task-ids-03-03-t03-audit-di-3-unreachable-block-lint/README.md) | override epic_ids_03_audit_2026_05_28 |
| 4 | [`task-ids-03-03-t04-audit-di-4-optional-fields-test-cleanup`](./task-ids-03-03-t04-audit-di-4-optional-fields-test-cleanup/README.md) | override epic_ids_03_audit_2026_05_28 |

## Open audit gaps (post-audit 2026-05-28)

| Finding | Gap task | Status |
|---------|----------|--------|
| DI-3 [LOW] | [t03 unreachable block lint](./task-ids-03-03-t03-audit-di-3-unreachable-block-lint/README.md) | done |
| DI-4 [LOW] | [t04 optional fields test cleanup](./task-ids-03-03-t04-audit-di-4-optional-fields-test-cleanup/README.md) | done |
