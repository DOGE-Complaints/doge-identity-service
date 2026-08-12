# EPIC-IDS-08 — Cleanup (scope, placeholders, docs)

> **ID:** `EPIC-IDS-08` · **Alias (backlog):** `EPIC-IDS-CLEANUP` · **Статус:** ⚪ Todo (materialized 2026-06-05, backlog intake)
> **Layer:** Tech-debt / Hygiene
> **Зависит от:** — (EPIC-IDS-01..06 Done)
> **Блокирует:** чистая база для функциональных эпиков (AUTH-CORE / EID / OAUTH)

---

## 1. Назначение

Привести identity к согласованной парадигме (решения 2026-06-04): убрать всё, что относится к историям (домен gateway), закрыть «заготовки без поведения» и устранить рассинхрон документации с кодом. Это не новая функциональность, а наведение порядка.

Парадигма: [`09-gateway-expectations`](../../../runtime-docs/09-gateway-expectations.md), [`05-data-model`](../../../runtime-docs/05-data-model.md), [`gap-analysis-full-2026-06-04`](../../../analysis/gap-analysis-full-2026-06-04.md).

## 2. Источники

- Backlog epic: [`EPIC-IDS-CLEANUP.md`](../../backlog-stories/cleanup/EPIC-IDS-CLEANUP.md)
- Backlog intake (Story 1): [`STORY-IDS-CLEANUP-01-remove-stories-from-identity`](../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- Backlog intake (Story 2): [`STORY-IDS-CLEANUP-02-placeholders-hardening`](../../backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md)
- Backlog intake (Story 3): [`STORY-IDS-CLEANUP-03-doc-drift`](../../backlog-stories/cleanup/STORY-IDS-CLEANUP-03-doc-drift.md)
- Анализ: [`identity-todo-backlog-2026-06-04`](../../../analysis/identity-todo-backlog-2026-06-04.md), [`epic-ids-05-scope-validation-2026-06-03`](../../../analysis/epic-ids-05-scope-validation-2026-06-03.md)

## 3. Почему отдельный эпик

Задачи-чистки не ложатся в инфраструктурные эпики 01–06 (они Done) и не относятся к функциональным AUTH-CORE/EID/OAUTH. Объединять их по смыслу логично в одном hygiene-эпике.

## 4. Вне scope эпика (backlog)

- Story 3 (CLEANUP-03) materialized в pipeline — см. §6 Story 3, pkg-000014.

## 5. Целевые файлы (Story 1 — CLEANUP-01)

```
src/core/infrastructure/db_supabase.py
src/core/api/asgi_app.py
src/core/domain/models.py
src/core/domain/contracts.py
src/core/infrastructure/repositories.py
src/core/infrastructure/providers.py
src/core/api/dependencies.py
src/core/infrastructure/service_factory.py
src/core/application/factory.py
src/core/stories/
supabase/migrations/20260527000001_create_story_drafts.sql
docs/requirements/15-story-authorization.md
tests/ (story-related modules)
```

## 5b. Целевые файлы (Story 2 — CLEANUP-02)

```
src/core/config/schema.py          # E17, E20
src/core/api/security.py           # E18
src/core/api/idempotency.py        # E21
src/core/audit/__init__.py         # E22
src/core/oauth/__init__.py         # E22
src/core/profiles/__init__.py      # E22
tests/                             # traceability AC #2–#4
.env.example, tests/conftest.py    # E20 pilot/conftest refs
docs/runtime-docs/03-soa-roles.md  # E22 mention (CLEANUP-03 overlap — только если t06 удаляет пакеты)
```

## 5c. Целевые файлы (Story 3 — CLEANUP-03)

```
docs/requirements/08-supabase-migrations.md   # DOC-3
docs/requirements/02-scope-and-boundaries.md  # DOC-3, gateway direction
docs/requirements/03-architecture-formula.md  # gateway direction
docs/requirements/15-story-authorization.md   # DOC-1 verify
.env.example                                   # CFG-3
docs/runtime-docs/01-api.md                    # AC#4
docs/runtime-docs/02-data-bootstrap.md         # AC#4
docs/runtime-docs/05-data-model.md             # AC#4
```

## 6. Stories

### Story 1: STORY-IDS-CLEANUP-01 — Вынос историй из identity + починка `/ready`

- **Pipeline story:** [`stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](./stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)
- **Source (backlog):** [`backlog-stories/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md`](../../backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md)

**Acceptance Criteria:**
- [x] При `DB_BACKEND=supabase` на базе из bootstrap (без `story_drafts`) → `/ready` = **200** (`schema:true`).
- [x] В коде нет ссылок на `story_drafts`/`StoryDraft`/story-роуты (grep = 0, кроме исторической миграции/changelog).
- [x] Тесты, завязанные на story, удалены/переписаны; весь offline-набор зелёный.
- [x] req-15 помечен deprecated.

### Story 2: STORY-IDS-CLEANUP-02 — Чистка заготовок и хардненинг

- **Pipeline story:** [`stories/STORY-IDS-CLEANUP-02-placeholders-hardening/STORY-IDS-CLEANUP-02-placeholders-hardening.md`](./stories/STORY-IDS-CLEANUP-02-placeholders-hardening/STORY-IDS-CLEANUP-02-placeholders-hardening.md)
- **Source (backlog):** [`backlog-stories/STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../../backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md)

**Acceptance Criteria:**
- [x] По каждому пункту зафиксировано решение владельца (оставить/довести/убрать) и оно выполнено.
- [x] Если `ALLOWED_RETURN_URLS` остаётся — `return_url` валидируется, есть тест на отклонение чужого домена.
- [x] Удалённые заготовки: grep по их идентификаторам = 0.
- [x] Offline-набор зелёный.

### Story 3: STORY-IDS-CLEANUP-03 — Устранение рассинхрона документации

- **Pipeline story:** [`stories/STORY-IDS-CLEANUP-03-doc-drift/STORY-IDS-CLEANUP-03-doc-drift.md`](./stories/STORY-IDS-CLEANUP-03-doc-drift/STORY-IDS-CLEANUP-03-doc-drift.md)
- **Source (backlog):** [`backlog-stories/STORY-IDS-CLEANUP-03-doc-drift.md`](../../backlog-stories/cleanup/STORY-IDS-CLEANUP-03-doc-drift.md)

**Acceptance Criteria:**
- [x] req-08/req-02 отражают фактические 4 миграции.
- [x] `.env.example` `AUTHENTIGATE_REDIRECT_URI` указывает на существующий роут.
- [x] req-15 помечен deprecated; направление в req-02/03 согласовано с моделью gateway→identity.
- [x] Нет противоречий между требованиями и [runtime-docs](../../../runtime-docs/).

## 7. Верификация эпика (Story 1)

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
rg "story_drafts|StoryDraft|story-drafts|submit-story" src tests --glob '!*migrations*'
```
