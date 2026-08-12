# STORY-IDS-CLEANUP-01 — Вынос историй из identity + починка `/ready`

## Meta
- **Key:** `STORY-IDS-CLEANUP-01-remove-stories-from-identity`
- **Parent Epic:** [`../../../../EPIC-IDS-08-cleanup.md`](../../../../EPIC-IDS-08-cleanup.md)
- **Epic alias (backlog):** `EPIC-IDS-CLEANUP`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- **Decision Ref:** [`../../../../backlog-stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md); [`identity-todo-backlog-2026-06-04`](../../../../../analysis/identity-todo-backlog-2026-06-04.md) D11–D15; gap SB-1 (HIGH), SB-2, SB-3, DOC-1
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../../../analysis/identity-todo-backlog-2026-06-04.md) — D11–D15; gap SB-1 (HIGH), SB-2, SB-3, DOC-1
- **Зависит от:** — (можно делать первой; разблокирует чистый старт)

## Зачем простыми словами
По решению 2026-06-04 истории — целиком домен gateway. В identity осталось наследие: story-роуты, таблица `story_drafts` с моделью и репозиториями, и — самое болезненное — `story_drafts` в списке обязательных таблиц healthcheck, из-за чего на правильно поднятой базе `/ready` отдаёт **503**. Эта story всё это убирает и возвращает `/ready` в зелёное.

## Scope
- Убрать `story_drafts` из `_REQUIRED_TABLES` ([`db_supabase.py:315-320`](../../../../../../src/core/infrastructure/db_supabase.py)) — **приоритетный пункт** (чинит `/ready`).
- Удалить story-роуты ([`asgi_app.py:258-310`](../../../../../../src/core/api/asgi_app.py)) и их `PROTECTED_OPTIONS_PATHS`-записи.
- Удалить `StoryDraft`-модель, контракт `StoryDraftRepository`, реализации InMemory/Supabase ([`models.py:95-103`](../../../../../../src/core/domain/models.py), [`db_supabase.py:616-648`](../../../../../../src/core/infrastructure/db_supabase.py), [`repositories.py`](../../../../../../src/core/infrastructure/repositories.py)) и слот в фабрике/DI.
- Удалить пустой пакет `core.stories`.
- Решить судьбу миграции `20260527000001_create_story_drafts.sql` (оставить как исторический файл / отметить deprecated).
- Привести требования: пометить [req-15](../../../../../requirements/15-story-authorization.md) устаревшим (форвард из identity отменён).

## Вне scope
- Реализация приёма историй на стороне gateway (его репозиторий).

## Точки в коде (текущее состояние)
- Healthcheck: [`db_supabase.py:315-320`](../../../../../../src/core/infrastructure/db_supabase.py).
- Роуты: [`asgi_app.py:258-310`](../../../../../../src/core/api/asgi_app.py).
- Модель/репо: [`models.py:95-103`](../../../../../../src/core/domain/models.py), [`db_supabase.py:616-648`](../../../../../../src/core/infrastructure/db_supabase.py), [`repositories.py:349-365`](../../../../../../src/core/infrastructure/repositories.py).
- Уже сделано: `story_drafts` исключён из [`bootstrap/000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql).

## Acceptance Criteria
- [x] При `DB_BACKEND=supabase` на базе из bootstrap (без `story_drafts`) → `/ready` = **200** (`schema:true`).
- [x] В коде нет ссылок на `story_drafts`/`StoryDraft`/story-роуты (grep = 0, кроме исторической миграции/changelog).
- [x] Тесты, завязанные на story, удалены/переписаны; весь offline-набор зелёный.
- [x] req-15 помечен deprecated.

## Парадигма-якорь
[09-gateway-expectations](../../../../../runtime-docs/09-gateway-expectations.md), [05-data-model §на вынос](../../../../../runtime-docs/05-data-model.md), [epic-ids-05-scope-validation](../../../../../analysis/epic-ids-05-scope-validation-2026-06-03.md).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-08-01-t01-remove-story-drafts-required-tables`](./task-ids-08-01-t01-remove-story-drafts-required-tables/README.md) | pkg-000011 |
| 2 | [`task-ids-08-01-t02-remove-story-http-routes`](./task-ids-08-01-t02-remove-story-http-routes/README.md) | pkg-000011 |
| 3 | [`task-ids-08-01-t03-remove-storydraft-domain-and-repos`](./task-ids-08-01-t03-remove-storydraft-domain-and-repos/README.md) | pkg-000011 |
| 4 | [`task-ids-08-01-t04-remove-core-stories-package`](./task-ids-08-01-t04-remove-core-stories-package/README.md) | pkg-000011 |
| 5 | [`task-ids-08-01-t05-migration-fate-and-req15-deprecated`](./task-ids-08-01-t05-migration-fate-and-req15-deprecated/README.md) | pkg-000011 |
| 6 | [`task-ids-08-01-t06-story-related-tests-cleanup`](./task-ids-08-01-t06-story-related-tests-cleanup/README.md) | pkg-000011 |
| 7 | [`task-ids-08-01-t07-story-acceptance-verification`](./task-ids-08-01-t07-story-acceptance-verification/README.md) | pkg-000011 |
| 8 | [`task-ids-08-01-t08-audit-f1-runbook-story-drafts-migration-align`](./task-ids-08-01-t08-audit-f1-runbook-story-drafts-migration-align/README.md) | pkg-000012 (draft) |
| 9 | [`task-ids-08-01-t09-audit-f2-story-migration-tests-residual`](./task-ids-08-01-t09-audit-f2-story-migration-tests-residual/README.md) | pkg-000012 (draft) |
| 10 | [`task-ids-08-01-t10-audit-f3-remove-empty-stories-directory`](./task-ids-08-01-t10-audit-f3-remove-empty-stories-directory/README.md) | pkg-000012 (draft) |
| 11 | [`task-ids-08-01-t11-audit-f4-backlog-story-status-sync`](./task-ids-08-01-t11-audit-f4-backlog-story-status-sync/README.md) | pkg-000012 (draft) |
