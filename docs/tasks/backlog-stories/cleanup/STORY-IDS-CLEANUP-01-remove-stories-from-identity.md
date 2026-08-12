# STORY-IDS-CLEANUP-01 — Вынос историй из identity + починка `/ready`

## Meta
- **Key:** `STORY-IDS-CLEANUP-01-remove-stories-from-identity`
- **Epic:** `EPIC-IDS-CLEANUP` → pipeline [`EPIC-IDS-08-cleanup`](../../epics/EPIC-IDS-08-cleanup/EPIC-IDS-08-cleanup.md)
- **Status:** 🟢 Done (P3 pkg-000011 + audit gaps pkg-000012, 2026-06-05)
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../analysis/identity-todo-backlog-2026-06-04.md) — D11–D15; gap SB-1 (HIGH), SB-2, SB-3, DOC-1
- **Зависит от:** — (можно делать первой; разблокирует чистый старт)

## Зачем простыми словами
По решению 2026-06-04 истории — целиком домен gateway. В identity осталось наследие: story-роуты, таблица `story_drafts` с моделью и репозиториями, и — самое болезненное — `story_drafts` в списке обязательных таблиц healthcheck, из-за чего на правильно поднятой базе `/ready` отдаёт **503**. Эта story всё это убирает и возвращает `/ready` в зелёное.

## Scope
- Убрать `story_drafts` из `_REQUIRED_TABLES` ([`db_supabase.py:315-320`](../../../../src/core/infrastructure/db_supabase.py)) — **приоритетный пункт** (чинит `/ready`).
- Удалить story-роуты ([`asgi_app.py:258-310`](../../../../src/core/api/asgi_app.py)) и их `PROTECTED_OPTIONS_PATHS`-записи.
- Удалить `StoryDraft`-модель, контракт `StoryDraftRepository`, реализации InMemory/Supabase ([`models.py:95-103`](../../../../src/core/domain/models.py), [`db_supabase.py:616-648`](../../../../src/core/infrastructure/db_supabase.py), [`repositories.py`](../../../../src/core/infrastructure/repositories.py)) и слот в фабрике/DI.
- Удалить пустой пакет `core.stories`.
- Решить судьбу миграции `20260527000001_create_story_drafts.sql` (оставить как исторический файл / отметить deprecated).
- Привести требования: пометить [req-15](../../../requirements/15-story-authorization.md) устаревшим (форвард из identity отменён).

## Вне scope
- Реализация приёма историй на стороне gateway (его репозиторий).

## Точки в коде (после P3 EPIC-IDS-08, 2026-06-05)
- Healthcheck: [`db_supabase.py:287-291`](../../../../src/core/infrastructure/db_supabase.py) — `_REQUIRED_TABLES` = 3 identity tables (без `story_drafts`).
- Story routes: **удалены** (были `asgi_app.py:258-310`); `PROTECTED_OPTIONS_PATHS` — [`asgi_app.py:26-32`](../../../../src/core/api/asgi_app.py).
- StoryDraft / repos / DI: **удалены** из `src/` (grep `StoryDraft|story_drafts` = 0).
- `core.stories`: **удалён** (pkg-000011 t04 + pkg-000012 t10).
- Миграция: [`20260527000001_create_story_drafts.sql`](../../../../supabase/migrations/20260527000001_create_story_drafts.sql) — historical, DEPRECATED; runbook §3 — operational migrations 1–4 only.
- Уже сделано ранее: `story_drafts` исключён из [`bootstrap/000_full_init.sql`](../../../../supabase/bootstrap/000_full_init.sql).

## Acceptance Criteria
- [x] При `DB_BACKEND=supabase` на базе из bootstrap (без `story_drafts`) → `/ready` = **200** (`schema:true`).
- [x] В коде нет ссылок на `story_drafts`/`StoryDraft`/story-роуты (grep = 0, кроме исторической миграции/changelog).
- [x] Тесты, завязанные на story, удалены/переписаны; весь offline-набор зелёный.
- [x] req-15 помечен deprecated.

## Парадигма-якорь
[09-gateway-expectations](../../../runtime-docs/09-gateway-expectations.md), [05-data-model §на вынос](../../../runtime-docs/05-data-model.md), [epic-ids-05-scope-validation](../../../analysis/epic-ids-05-scope-validation-2026-06-03.md).
