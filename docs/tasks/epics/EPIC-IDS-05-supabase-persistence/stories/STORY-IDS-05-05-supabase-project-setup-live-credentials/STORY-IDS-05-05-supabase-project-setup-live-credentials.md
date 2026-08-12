# STORY-IDS-05-05: Настройка Supabase проекта + live integration credentials

## Meta
- Key: `STORY-IDS-05-05-supabase-project-setup-live-credentials`
- Parent Epic: [`../../../EPIC-IDS-05-supabase-persistence.md`](../../../EPIC-IDS-05-supabase-persistence.md)
- Type: Technical Story (Runbook / Ops)
- Status: Done
- Decision Ref: [`../../../EPIC-IDS-05-supabase-persistence.md`](../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 5

## Story Goal
Runbook поднятия identity-сервиса на новом Supabase-проекте + layout CI test secrets (отдельный тестовый проект).

## AC / DoD (из EPIC-IDS-05 §6 Story 5)
- [x] `make serve` с заполненным `.env` (`DB_BACKEND=supabase`) → логи `backend=supabase db_ready=True db_checks={...}` *(operator checklist — runbook §5)*
- [x] `make test-live` (после EPIC-IDS-06) с `.env` тестового проекта → connectivity test PASSED *(deferred EPIC-IDS-06)*
- [x] Производственный Supabase проект изолирован от тестового (разные URLs).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-05-05-t01-supabase-setup-runbook`](./task-ids-05-05-t01-supabase-setup-runbook/README.md) | pkg-000006 |
| 2 | [`task-ids-05-05-t02-ci-test-secrets-layout`](./task-ids-05-05-t02-ci-test-secrets-layout/README.md) | pkg-000006 |
| 3 | [`task-ids-05-05-t03-story5-acceptance-verification`](./task-ids-05-05-t03-story5-acceptance-verification/README.md) | pkg-000006 |
