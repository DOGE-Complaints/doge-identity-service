# Жёсткий аудит исполнения STORY-IDS-CLEANUP-01 (вынос историй + починка `/ready`)

> **Дата:** 2026-06-05
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-CLEANUP-01-remove-stories-from-identity`](../tasks/backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) vs фактический код. Исполнена под **EPIC-IDS-08-cleanup** (pkg-000011), 7 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): EPIC-IDS-08, task queue t01–t07.

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| `grep story_drafts\|StoryDraft` по `src/` | **0** ✅ |
| story-роуты в `asgi_app.py` | **0** ✅ |
| `_REQUIRED_TABLES` | 3 таблицы (без story_drafts) — [`db_supabase.py:287-291`](../../src/core/infrastructure/db_supabase.py) |
| `PROTECTED_OPTIONS_PATHS` | только `/me`,`/auth/eid/start`,`/oauth/*` — [`asgi_app.py:26-32`](../../src/core/api/asgi_app.py) |
| story_drafts в contracts/factory/DI | **0** ✅ |
| req-15 / миграция | DEPRECATED-шапки проставлены |
| **Offline-сюита** | **199 passed, 10 deselected** ✅ (было 200 → −1 удалённый story-тест) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду, не по индексу.

| Таск (EPIC-IDS-08, pkg-000011) | Факт | Статус |
|--------------------------------|------|--------|
| t01 remove story_drafts required tables | `_REQUIRED_TABLES` = 3 таблицы ([`db_supabase.py:287-291`](../../src/core/infrastructure/db_supabase.py)) | 🟢 |
| t02 remove story http routes | 0 story-роутов; `PROTECTED_OPTIONS_PATHS` очищен ([`asgi_app.py:26-32`](../../src/core/api/asgi_app.py)) | 🟢 |
| t03 remove storydraft domain and repos | `StoryDraft`/`StoryDraftRepository`/InMemory/Supabase + DI-слот удалены (grep=0) | 🟢 |
| t04 remove core stories package | `__init__.py` удалён, но пустой каталог `src/core/stories/` остался (F3) | 🟢 c оговоркой |
| t05 migration fate + req15 deprecated | миграция + req-15 помечены DEPRECATED; runbook не выровнен (F1) | 🟢 c оговоркой |
| t06 story related tests cleanup | offline зелёный, но 2 теста всё ещё проверяют story_drafts-миграцию/runbook (F2) | 🟢 c оговоркой |
| t07 story acceptance verification | AC1/AC4 ✅; AC2/AC3 — остаток (F1/F2) | 🟢 c оговоркой |
| **STORY-IDS-CLEANUP-01** | ядро вынесено, `/ready` починен; doc/test-остаток | **🟢 Done** (с findings) |

Индекс ([`bullrun-launch-index.md:43`](../tasks/bullrun-launch-index.md)) держит эпик `🟡 In Progress — CLEANUP-01 🟢 Done; CLEANUP-02/03 backlog only` — корректно.

---

## 2. Сверка Acceptance Criteria story

| AC | Факт | Вердикт |
|----|------|---------|
| AC1 `/ready`=200 на bootstrap-базе (`schema:true`) | `_REQUIRED_TABLES` = ровно 3 таблицы, все в [`bootstrap/000_full_init.sql`](../../supabase/bootstrap/000_full_init.sql); причина 503 устранена | ✅ (на уровне кода; полная проверка — live) |
| AC2 нет ссылок на story в коде (кроме исторической миграции) | `src/` чист (grep=0); миграция оставлена как историческая с DEPRECATED-шапкой | ✅ для `src/`; ⚠️ остаток в тестах/runbook (F1/F2) |
| AC3 story-тесты удалены/переписаны; offline зелёный | offline **199 passed** ✅; но `test_supabase_migrations_sql.py`/`test_supabase_runbook_docs.py` всё ещё завязаны на story_drafts | ⚠️ частично (F2) |
| AC4 req-15 deprecated | [`15-story-authorization.md:3`](../requirements/15-story-authorization.md) DEPRECATED | ✅ |

**Вывод:** приоритетная цель (убрать story из `src/`, починить `/ready`) **достигнута**; остаток — в документации/тестах (не в рантайме).

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| F1 | **MEDIUM** | Doc-drift / contract | runbook §3 предписывает применять миграцию #5 `story_drafts`, тогда как сама миграция помечена «do not apply on new deployments», а bootstrap её исключает | [`runbook/supabase-project-setup.md:62`](../runbook/supabase-project-setup.md) vs [`миграция:1-2`](../../supabase/migrations/20260527000001_create_story_drafts.sql) |
| F2 | MEDIUM | Test-residual (AC3) | 2 теста закрепляют story_drafts: `EXPECTED_MIGRATION_FILES` включает story_drafts ([`test_supabase_runbook_docs.py:17`](../../tests/test_supabase_runbook_docs.py)); SQL-контент проверяется ([`test_supabase_migrations_sql.py:45,47,52,87`](../../tests/test_supabase_migrations_sql.py)) — фактически тесты **энфорсят** F1 | tests |
| F3 | LOW | Residual | пустой каталог `src/core/stories/` остался после удаления `__init__.py` (пакета уже нет, но директория-мусор есть) | `src/core/stories/` |
| F4 | LOW | Doc-stale (self) | backlog-story помечена `⚪ Todo` / эпик `EPIC-IDS-CLEANUP`; реально 🟢 Done под `EPIC-IDS-08`; «точки в коде» ссылаются на устаревшие строки (`db_supabase.py:315-320`→287; `asgi_app.py:258-310` — роуты удалены) | [`STORY-IDS-CLEANUP-01...md:6,25-27`](../tasks/backlog-stories/cleanup/STORY-IDS-CLEANUP-01-remove-stories-from-identity.md) |

### F1 — пояснение (приоритет)
Три источника о судьбе `story_drafts`-миграции рассогласованы:
- миграция: «Historical migration only; **do not apply** on new identity deployments» ([`:1-2`](../../supabase/migrations/20260527000001_create_story_drafts.sql));
- bootstrap: story_drafts **исключён** ([`bootstrap/000_full_init.sql`](../../supabase/bootstrap/000_full_init.sql));
- runbook §3: story_drafts **в обязательном** списке «выполните по порядку» ([`:62`](../runbook/supabase-project-setup.md)).
Оператор по runbook применит deprecated-миграцию → пересоздаст `story_drafts` (на `/ready` уже не влияет, т.к. healthcheck её не требует, но прямо противоречит решению о выносе). **Как закрыть:** выровнять runbook §3 с deprecation (убрать #5 или пометить историческим/optional).

### F2 — пояснение
AC3 требовал «тесты, завязанные на story, удалены/переписаны». `test_supabase_runbook_docs.py` ожидает story_drafts в списке миграций runbook, `test_supabase_migrations_sql.py` валидирует её SQL. Тесты зелёные **только потому**, что миграция и runbook-строка сохранены → тесты фиксируют рассогласование F1. **Как закрыть:** согласовать со стратегией «историческая миграция» (тесты пометить/перевести на historical-набор, рассинхрон с runbook убрать).

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **199 passed** (было 200) — падение счётчика из-за удалённого story-теста, **ожидаемо**, не регресс |
| `/ready` healthcheck | теперь 3 таблицы, все в bootstrap — story_drafts-503 устранён |
| Падающих тестов | нет |
| Сломанные импорты после удаления StoryDraft | нет (grep по `src/` = 0; сюита зелёная) |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-CLEANUP-01 — 🟢 исполнена по сути:** story-домен вынесен из `src/`, `_REQUIRED_TABLES` починен, req-15/миграция помечены deprecated, offline зелёный. Приоритетный HIGH-gap (SB-1, `/ready`=503) **закрыт**.
- **Остаток (не в рантайме):** F1 (runbook ↔ deprecation рассинхрон, MEDIUM) и завязанный на него F2 (story-тесты не вычищены, MEDIUM); F3 (пустой каталог), F4 (устаревшая backlog-story) — LOW.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; статусы тасков сверены по коду.
- [x] Регрессий нет; счётчик 200→199 объяснён.
- [x] Severity проставлена; «как закрыть» — направление, без кода.
- [x] Рассинхрон runbook/миграция/bootstrap (change-propagation gap) зафиксирован, не скрыт.
