# STORY-IDS-CLEANUP-03 — Устранение рассинхрона документации

## Meta
- **Key:** `STORY-IDS-CLEANUP-03-doc-drift`
- **Epic:** `EPIC-IDS-CLEANUP` (новый, см. [EPIC-IDS-CLEANUP.md](EPIC-IDS-CLEANUP.md))
- **Status:** 🟢 Done
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../analysis/identity-todo-backlog-2026-06-04.md) — G25, G26 + `.env` redirect; gap DOC-1/DOC-3/CFG-3
- **Зависит от:** — (можно в любой момент; после CLEANUP-01 для req-15)

## Зачем простыми словами
Несколько мест в требованиях/конфиге разошлись с кодом. Само по себе не ломает рантайм, но вводит в заблуждение тех, кто будет реализовывать следующие эпики. Эта story приводит документацию в соответствие с фактом.

## Scope
- **DOC-3:** [req-08](../../../requirements/08-supabase-migrations.md) и [req-02:20](../../../requirements/02-scope-and-boundaries.md) говорят «3 миграции» — фактически 4 (добавить provider_abstraction).
- **CFG-3:** [`.env.example:51`](../../../../.env.example) `AUTHENTIGATE_REDIRECT_URI=.../auth/eid/callback` указывает на несуществующий роут (есть `/auth/authentigate/callback`) — поправить.
- **DOC-1:** [req-15](../../../requirements/15-story-authorization.md) — пометить устаревшим (форвард identity→gateway отменён; пересекается с CLEANUP-01).
- Сверить упоминание направления identity↔gateway в [req-02](../../../requirements/02-scope-and-boundaries.md)/[req-03](../../../requirements/03-architecture-formula.md) с решённой моделью (gateway→identity).

## Вне scope
- Изменения кода (это чисто документная синхронизация, кроме `.env.example`).

## Acceptance Criteria
- [x] req-08/req-02 отражают фактические 4 миграции.
- [x] `.env.example` `AUTHENTIGATE_REDIRECT_URI` указывает на существующий роут.
- [x] req-15 помечен deprecated; направление в req-02/03 согласовано с моделью gateway→identity.
- [x] Нет противоречий между требованиями и [runtime-docs](../../../runtime-docs/).

## Парадигма-якорь
[runtime-docs](../../../runtime-docs/), [gap-analysis-full](../../../analysis/gap-analysis-full-2026-06-04.md).
