# STORY-IDS-05-06: Backend switch — provide_service_factory

## Meta
- Key: `STORY-IDS-05-06-backend-switch-provide-service-factory`
- Parent Epic: [`../../../EPIC-IDS-05-supabase-persistence.md`](../../../EPIC-IDS-05-supabase-persistence.md)
- Type: Technical Story (Supabase Infrastructure)
- Status: Done
- Decision Ref: [`../../../EPIC-IDS-05-supabase-persistence.md`](../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 6

## Story Goal
`DB_BACKEND=supabase` → реальные Supabase-репозитории в `provide_service_factory()` (без InMemory fallback).

## AC / DoD (из EPIC-IDS-05 §6 Story 6)
- [x] `provide_service_factory(config_with_db_backend_supabase)` возвращает factory с `SupabaseProfileRepository` и т.д.
- [x] `build_api_dependencies()` при `DB_BACKEND=supabase` — `db_checks` заполнен, `db_ready` отражает реальность.
- [x] Переключение `DB_BACKEND=in_memory ↔ supabase` через env — единственный механизм.

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-05-06-t01-provide-service-factory-supabase-branch`](./task-ids-05-06-t01-provide-service-factory-supabase-branch/README.md) | pkg-000006 |
| 2 | [`task-ids-05-06-t02-supabase-fallback-test-migration`](./task-ids-05-06-t02-supabase-fallback-test-migration/README.md) | pkg-000006 |
| 3 | [`task-ids-05-06-t03-story6-acceptance-verification`](./task-ids-05-06-t03-story6-acceptance-verification/README.md) | pkg-000006 |
