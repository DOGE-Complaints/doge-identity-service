# STORY-IDS-CLEANUP-03 — Устранение рассинхрона документации

## Meta
- **Key:** `STORY-IDS-CLEANUP-03-doc-drift`
- **Parent Epic:** [`../../../../EPIC-IDS-08-cleanup.md`](../../../../EPIC-IDS-08-cleanup.md)
- **Epic alias (backlog):** `EPIC-IDS-CLEANUP`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-CLEANUP-03-doc-drift.md`](../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-03-doc-drift.md)
- **Decision Ref:** [`../../../../backlog-stories/STORY-IDS-CLEANUP-03-doc-drift.md`](../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-03-doc-drift.md); [`identity-todo-backlog-2026-06-04`](../../../../../analysis/identity-todo-backlog-2026-06-04.md) G25, G26; [`gap-analysis-full-2026-06-04`](../../../../../analysis/gap-analysis-full-2026-06-04.md) DOC-1/DOC-3/CFG-3
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../../../analysis/identity-todo-backlog-2026-06-04.md) — G25, G26 + `.env` redirect; gap DOC-1/DOC-3/CFG-3
- **Зависит от:** — (можно в любой момент; после CLEANUP-01 для req-15)

## Зачем простыми словами
Несколько мест в требованиях/конфиге разошлись с кодом. Само по себе не ломает рантайм, но вводит в заблуждение тех, кто будет реализовывать следующие эпики. Эта story приводит документацию в соответствие с фактом.

## Scope
- **DOC-3:** [req-08](../../../../../requirements/08-supabase-migrations.md) и [req-02:20](../../../../../requirements/02-scope-and-boundaries.md) говорят «3 миграции» — фактически 4 (добавить provider_abstraction).
- **CFG-3:** [`.env.example:51`](../../../../../../../.env.example) `AUTHENTIGATE_REDIRECT_URI=.../auth/eid/callback` указывает на несуществующий роут (есть `/auth/authentigate/callback`) — поправить.
- **DOC-1:** [req-15](../../../../../requirements/15-story-authorization.md) — пометить устаревшим (форвард identity→gateway отменён; пересекается с CLEANUP-01).
- Сверить упоминание направления identity↔gateway в [req-02](../../../../../requirements/02-scope-and-boundaries.md)/[req-03](../../../../../requirements/03-architecture-formula.md) с решённой моделью (gateway→identity).

## Вне scope
- Изменения кода (это чисто документная синхронизация, кроме `.env.example`).

## Точки в коде (текущее состояние, P1 facts)
- DOC-3: [`req-08:12-16`](../../../../../../../docs/requirements/08-supabase-migrations.md) — 3 migration files listed; [`req-02:20`](../../../../../../../docs/requirements/02-scope-and-boundaries.md) — «3 таблицы»; operational migrations incl. [`20260526000001_eid_sessions_provider_abstraction.sql`](../../../../../../../supabase/migrations/20260526000001_eid_sessions_provider_abstraction.sql); [`02-data-bootstrap.md:26-33`](../../../../../../../docs/runtime-docs/02-data-bootstrap.md) already lists 4 migrations.
- CFG-3: [`.env.example:51`](../../../../../../../.env.example) → `.../auth/eid/callback`; route [`asgi_app.py:209`](../../../../../../../src/core/api/asgi_app.py) `@app.get("/auth/authentigate/callback")`; [`conftest.py:42-44`](../../../../../../../tests/conftest.py) uses correct URI.
- DOC-1: [`req-15:3`](../../../../../../../docs/requirements/15-story-authorization.md) — DEPRECATED banner from CLEANUP-01 t05.
- req-02/03: [`req-02:18-19`](../../../../../../../docs/requirements/02-scope-and-boundaries.md) story rows in MVP scope; [`req-03:39,78-115`](../../../../../../../docs/requirements/03-architecture-formula.md) identity story endpoints / forward model.
- AC#4 drift: `grep story_drafts src/` = 0; [`runtime-docs/02-data-bootstrap.md:49`](../../../../../../../docs/runtime-docs/02-data-bootstrap.md) stale `/ready` + `story_drafts`; [`01-api.md:40`](../../../../../../../docs/runtime-docs/01-api.md) references removed story routes.

## Acceptance Criteria
- [x] req-08/req-02 отражают фактические 4 миграции.
- [x] `.env.example` `AUTHENTIGATE_REDIRECT_URI` указывает на существующий роут.
- [x] req-15 помечен deprecated; направление в req-02/03 согласовано с моделью gateway→identity.
- [x] Нет противоречий между требованиями и [runtime-docs](../../../../../runtime-docs/).

## Парадигма-якорь
[runtime-docs](../../../../../runtime-docs/), [gap-analysis-full](../../../../../analysis/gap-analysis-full-2026-06-04.md).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-08-03-t01-req08-req02-migration-count-doc3`](./task-ids-08-03-t01-req08-req02-migration-count-doc3/README.md) | pkg-000014 |
| 2 | [`task-ids-08-03-t02-env-example-authentigate-redirect-cfg3`](./task-ids-08-03-t02-env-example-authentigate-redirect-cfg3/README.md) | pkg-000014 |
| 3 | [`task-ids-08-03-t03-req15-deprecated-verify-doc1`](./task-ids-08-03-t03-req15-deprecated-verify-doc1/README.md) | pkg-000014 |
| 4 | [`task-ids-08-03-t04-req02-req03-gateway-direction-sync`](./task-ids-08-03-t04-req02-req03-gateway-direction-sync/README.md) | pkg-000014 |
| 5 | [`task-ids-08-03-t05-requirements-runtime-docs-crosscheck-ac4`](./task-ids-08-03-t05-requirements-runtime-docs-crosscheck-ac4/README.md) | pkg-000014 |
| 6 | [`task-ids-08-03-t06-story-acceptance-verification`](./task-ids-08-03-t06-story-acceptance-verification/README.md) | pkg-000014 |
