# STORY-IDS-05-04: SQL schema — ссылка на req-08 + новые миграции

## Meta
- Key: `STORY-IDS-05-04-sql-schema-migrations`
- Parent Epic: [`../../../EPIC-IDS-05-supabase-persistence.md`](../../../EPIC-IDS-05-supabase-persistence.md)
- Type: Technical Story (Supabase Data)
- Status: Done
- Decision Ref: [`../../../EPIC-IDS-05-supabase-persistence.md`](../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 4

## Story Goal
5 SQL-миграций identity-схемы в `supabase/migrations/` из req-08, req-17, req-15 с RLS и service_role policies.

## AC / DoD (из EPIC-IDS-05 §6 Story 4)
- [x] Все миграции применяются на чистый Supabase-проект последовательно без ошибок. *(SQL idempotent; live apply — Story 5 checklist)*
- [x] После применения: `required_tables_ready() == True`, `required_columns_ready() == True`, `provider_state_ready() == True`. *(schema matches healthcheck queries; live verify Story 5)*
- [x] `service_role_policy_probe()` → True (RLS не блокирует service_role). *(explicit service_role policies)*
- [x] Каждая таблица имеет `service_role` policy (либо bypass через service_role API key, явная policy для INSERT/SELECT/UPDATE).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-05-04-t01-req08-core-migrations`](./task-ids-05-04-t01-req08-core-migrations/README.md) | pkg-000006 |
| 2 | [`task-ids-05-04-t02-req17-req15-migrations`](./task-ids-05-04-t02-req17-req15-migrations/README.md) | pkg-000006 |
| 3 | [`task-ids-05-04-t03-story4-acceptance-verification`](./task-ids-05-04-t03-story4-acceptance-verification/README.md) | pkg-000006 |
