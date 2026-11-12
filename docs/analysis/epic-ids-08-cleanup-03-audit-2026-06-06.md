# Жёсткий аудит исполнения STORY-IDS-CLEANUP-03 (устранение doc-drift)

> **Дата:** 2026-06-06
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-CLEANUP-03-doc-drift`](../tasks/backlog-stories/cleanup/STORY-IDS-CLEANUP-03-doc-drift.md) vs фактические файлы. Исполнена под **EPIC-IDS-08-cleanup** (pkg-000014, docs-only), 6 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): EPIC-IDS-08, task queue t01–t06.
> **Характер story:** чисто документная синхронизация (Vне scope: изменения кода, кроме `.env.example`).

## Команды верификации (выполнены)

| Пункт scope | Результат |
|-------------|-----------|
| DOC-3 req-08 | «**Operational set: 4 миграции** (3 таблицы + provider abstraction)» ([req-08:19](../requirements/08-supabase-migrations.md)) + добавлена «## Migration 4: provider abstraction» (:245) |
| DOC-3 req-02 | «Supabase migrations \| **4 operational migrations**: 3 base tables + provider abstraction» ([req-02:18](../requirements/02-scope-and-boundaries.md)) |
| CFG-3 `.env.example` | `AUTHENTIGATE_REDIRECT_URI=http://localhost:8100/auth/authentigate/callback` ([:51](../../.env.example)) — существующий роут |
| DOC-1 req-15 | DEPRECATED-шапка ([req-15:3](../requirements/15-story-authorization.md)) |
| Направление req-02/03 | переписано под gateway→identity + GPT→gateway-direct (см. §3) |
| **Offline-сюита** | **206 passed, 10 deselected** ✅ (docs-only — без изменений рантайма) |

---

## 1. Актуализация тасков и story (по коду/файлам)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по файлам.

| Таск (EPIC-IDS-08, pkg-000014) | Факт | Статус |
|--------------------------------|------|--------|
| t01 req08/req02 migration count (DOC-3) | req-08 = 4 миграции + секция «Migration 4»; req-02:18 = «4 operational migrations» | 🟢 |
| t02 env authentigate redirect (CFG-3) | `.env.example:51` → `/auth/authentigate/callback` (реальный роут) | 🟢 |
| t03 req15 deprecated verify (DOC-1) | DEPRECATED-шапка на месте | 🟢 |
| t04 req02/req03 gateway direction sync | Flow B переписан: ChatGPT→gateway, gateway→introspection identity; добавлена пометка «Identity не форвардит» ([req-03:104,108,119](../requirements/03-architecture-formula.md)) | 🟢 |
| t05 requirements↔runtime-docs crosscheck (AC4) | req-03 Flow B совпадает с [09-gateway-expectations](../runtime-docs/09-gateway-expectations.md) (introspection-модель); противоречий нет | 🟢 |
| t06 story acceptance verification | все AC выполнены (см. §2) | 🟢 |
| **STORY-IDS-CLEANUP-03** | doc-drift устранён, согласованность восстановлена | **🟢 Done** |

Индекс ([`bullrun-launch-index.md:11`](../tasks/bullrun-launch-index.md)) фиксирует волну `pkg-000014 (CLEANUP-03 🟢, docs-only)` — корректно.

---

## 2. Сверка Acceptance Criteria story

| AC | Факт | Вердикт |
|----|------|---------|
| req-08/req-02 отражают 4 миграции | req-08:19 + Migration 4; req-02:18 «4 operational migrations» | ✅ |
| `.env.example` `AUTHENTIGATE_REDIRECT_URI` → существующий роут | `:51` `/auth/authentigate/callback` (есть в [`asgi_app.py`](../../src/core/api/asgi_app.py)) | ✅ |
| req-15 deprecated; направление req-02/03 согласовано с gateway→identity | req-15 DEPRECATED; req-02 «gateway вызывает identity»; req-03 Flow B GPT→gateway + introspection | ✅ |
| Нет противоречий требования ↔ runtime-docs | req-03 Flow B ≡ [09-gateway-expectations](../runtime-docs/09-gateway-expectations.md) | ✅ |

**Вывод:** все 4 AC выполнены.

---

## 3. Проверка ключевого риска: внутреннее противоречие req-03 (снято)

При беглом grep строка [req-03:104](../requirements/03-architecture-formula.md) `→ POST doge-complaints-gateway /intake/stories` выглядела как «identity форвардит» (старая модель) и противоречила пометке :119 «Identity не форвардит». **При чтении контекста — противоречия нет:** актор строки 104 — **ChatGPT** (`ChatGPT → POST gateway /intake/stories`, :103-105), а identity участвует только как introspection-провайдер (`gateway → introspection /me у identity`, :108). То есть Flow B полностью соответствует решённой парадигме (GPT→gateway-direct + gateway→identity-introspection). Ложная тревога, фиксирую как verified-OK.

---

## 4. Findings

**Материальных findings нет.** Doc-drift по всем трём пунктам (DOC-3/CFG-3/DOC-1) устранён, направление синхронизировано, противоречий требования↔runtime-docs не выявлено.

Тривиальные наблюдения (не gap, severity none):
| ID | Тип | Суть | Где |
|----|-----|------|-----|
| O1 | trivial | story Meta: `Epic: EPIC-IDS-CLEANUP (новый)`, исполнена под `EPIC-IDS-08-cleanup` — нет alias-пометки (в CLEANUP-01 формат был «EPIC-IDS-CLEANUP → pipeline EPIC-IDS-08»); косметика | [`STORY-IDS-CLEANUP-03...md:5`](../tasks/backlog-stories/cleanup/STORY-IDS-CLEANUP-03-doc-drift.md) |
| O2 | trivial | индекс помечает волну `2026-06-02` (имя pkg — `20260605`); дата-ярлык | [`bullrun-launch-index.md:11`](../tasks/bullrun-launch-index.md) |

---

## 5. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **206 passed** (без изменений — story docs-only) |
| Изменения кода | только `.env.example` (значение redirect); `src/` не затронут |
| Тесты, читающие req/runbook | зелёные (req-08/req-02 — requirement-доки, не assert'ятся тестами напрямую) |

Регрессий не выявлено.

---

## 6. Итог

- **STORY-IDS-CLEANUP-03 — 🟢 исполнена чисто:** все 3 пункта doc-drift (DOC-3/CFG-3/DOC-1) закрыты, направление identity↔gateway в req-02/03 синхронизировано с моделью gateway→identity и совпадает с runtime-doc 09. AC 4/4 выполнены.
- **Материальных gap'ов нет.** Только 2 косметических наблюдения (O1/O2).
- Этим закрывается последняя из трёх CLEANUP-стори; EPIC-IDS-08 CLEANUP-01/02/03 исполнены.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; статусы тасков сверены по файлам.
- [x] Потенциальное противоречие req-03 проверено чтением контекста (снято), не записано как ложный gap.
- [x] Регрессий нет (docs-only, 206 passed).
- [x] Тривиальные наблюдения отделены от material findings, не раздуты в gap.
