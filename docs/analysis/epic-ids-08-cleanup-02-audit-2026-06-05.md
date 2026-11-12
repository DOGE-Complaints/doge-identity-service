# Жёсткий аудит исполнения STORY-IDS-CLEANUP-02 (чистка заготовок и хардненинг)

> **Дата:** 2026-06-05
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-CLEANUP-02-placeholders-hardening`](../tasks/backlog-stories/cleanup/STORY-IDS-CLEANUP-02-placeholders-hardening.md) vs фактический код. Исполнена под **EPIC-IDS-08-cleanup** (pkg-000013), 7 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): EPIC-IDS-08, task queue t01–t07.

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| E17 `ALLOWED_RETURN_URLS` | оставлен + новый валидатор [`security/return_url.py`](../../src/core/security/return_url.py); тест [`test_return_url_validation.py`](../../tests/test_return_url_validation.py) |
| E18 `StubBearerTokenAuth` | grep `src/`/`tests/` = **0** ✅ удалён |
| E20 `CODE_VERIFIER_ENCRYPTION_KEY` | grep `src/` = 0; в `.env.example` нет ✅ удалён |
| E21 `idempotency.py` | файл удалён; grep в `src/` = 0 ✅ |
| E22 `core.audit/oauth/profiles` | `__init__.py` удалён, но **пустые каталоги остались** (F2) |
| **Offline-сюита** | **204 passed, 10 deselected** ✅ (было 200 → +4 теста return_url) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-08, pkg-000013) | Факт | Статус |
|--------------------------------|------|--------|
| t01 owner decisions placeholders e17 e22 | решения зафиксированы (E17 оставить+валидировать; E18/E20/E21 убрать; E22 — пакеты убраны) | 🟢 |
| t02 allowed return urls e17 | валидатор `validate_return_url`/`normalize_return_url`/`parse_allowed_return_urls` + 6 тестов; **но не подключён ни к одному маршруту** (F1) | 🟢 c оговоркой |
| t03 remove stub bearer token auth e18 | класс удалён (grep=0) | 🟢 |
| t04 code verifier encryption key e20 | удалён из схемы и `.env.example` (grep=0) | 🟢 |
| t05 idempotency resolver e21 | `idempotency.py` удалён; но [01-api.md:50](../runtime-docs/01-api.md) всё ещё ссылается на файл (F3) | 🟢 c оговоркой |
| t06 empty layer packages e22 | `__init__.py` удалены; пустые каталоги `core.audit/oauth/profiles` остались + 03-soa.md:64 утверждает «удалены» (F2) | 🟢 c оговоркой |
| t07 story acceptance verification | AC выполнены формально; F1 (валидатор не подключён) | 🟢 c оговоркой |
| **STORY-IDS-CLEANUP-02** | заготовки вычищены; security-валидатор готов, но не enforced | **🟢 Done** (с findings) |

Индекс ([`bullrun-launch-index.md:11`](../tasks/bullrun-launch-index.md)) фиксирует волну `pkg-000013 (CLEANUP-02 🟢, 204 pytest offline)` — корректно по счётчику.

---

## 2. Сверка Acceptance Criteria story

| AC | Факт | Вердикт |
|----|------|---------|
| По каждому пункту зафиксировано решение и выполнено | E17 оставить+валидировать, E18/E20/E21 убрать, E22 пакеты убрать — выполнено | ✅ (E22/E17 — с оговорками F1/F2) |
| Если `ALLOWED_RETURN_URLS` остаётся → `return_url` **валидируется**, есть тест на чужой домен | валидатор + тест `test_validate_return_url_rejects_foreign_domain` ([`:25-28`](../../tests/test_return_url_validation.py)) есть; ⚠️ но `validate_return_url` **никто не вызывает** в `src/` (0 callers) | ⚠️ частично (F1) |
| Удалённые заготовки: grep = 0 | E18/E20/E21 = 0 в `src/` ✅ | ✅ |
| Offline зелёный | 204 passed | ✅ |

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| F1 | **MEDIUM** | Security-not-enforced | `validate_return_url` реализован и покрыт тестами, но **не вызывается ни из одного маршрута** (0 callers в `src/`). Единственный потенциальный потребитель — `POST /auth/eid/start` — это 501-заглушка. Значит open-redirect, ради которого вводился E17, **в рантайме не закрыт** — защита подготовлена, но не enforced | [`security/return_url.py`](../../src/core/security/return_url.py); 0 callers (grep) |
| F2 | LOW | Residual + doc | `core.audit`/`core.oauth`/`core.profiles` — **пустые каталоги без `__init__.py`** (содержимое удалено, директории остались); при этом [03-soa-roles.md:64](../runtime-docs/03-soa-roles.md) утверждает, что они «**удалены**» — неточно | `src/core/{audit,oauth,profiles}/` |
| F3 | LOW | Doc-drift | [01-api.md:50](../runtime-docs/01-api.md) описывает «Idempotency-key резолвер (`idempotency.py`) … готов» со ссылкой на **удалённый** файл — битая ссылка + ложное утверждение | runtime-doc |
| F4 | trivial | Дата | индекс/пакет помечены `2026-06-02` для волны CLEANUP-02, фактически работа после CLEANUP-01 (2026-06-05) | `bullrun-launch-index.md:11`, имя pkg-000013 |

### F1 — пояснение (приоритет)
E17 заявлен как «закрыть open-redirect». Реализация: модуль [`return_url.py`](../../src/core/security/return_url.py) (`parse_allowed_return_urls`/`normalize_return_url`/`validate_return_url`/`InvalidReturnUrlError`), конфиг `allowed_return_urls` ([`schema.py:56,166`](../../src/core/config/schema.py)), 6 юнит-тестов. Однако `grep validate_return_url src/` (кроме самого модуля) = **0** — функция нигде не вызывается. Поскольку `return_url` приходит в `/auth/eid/start` (🟡 501), точки интеграции пока нет, и валидатор остаётся «готовой библиотекой без потребителя». **Как закрыть:** подключить `validate_return_url` к реальному обработчику при реализации eID-флоу (EPIC-IDS-EID) ИЛИ зафиксировать в AC, что E17 — подготовка, а enforcement — в eID-эпике. Решение — за владельцем.

### F2 — пояснение
Тот же класс остатка, что F3 в [CLEANUP-01 аудите](epic-ids-08-cleanup-01-audit-2026-06-05.md) (пустой `core.stories` — там был удалён полностью). Здесь `core.stories` удалён, а `core.audit/oauth/profiles` оставлены пустыми каталогами. Если решение — «оставить под будущие эпики», то корректнее держать их пакетами с `__init__.py` (а doc не должен говорить «удалены»); если «убрать» — удалить директории. Сейчас — промежуточное «ни пакет, ни удалено» + неверный doc.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **204 passed** (было 200) — +4 теста return_url, **ожидаемо** |
| Падающих тестов | нет |
| Сломанные импорты после удаления (Stub/idempotency/AES-ключ) | нет (grep=0, сюита зелёная) |
| Удаление `code_verifier_encryption_key` из pilot-required | сюита зелёная, конфиг грузится |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-CLEANUP-02 — 🟢 исполнена по сути:** E18/E20/E21 убраны чисто, E17-валидатор реализован и покрыт тестами, offline зелёный (204).
- **Главное к вниманию — F1 (MEDIUM):** open-redirect-защита (E17) **подготовлена, но не подключена** — `validate_return_url` без вызовов, потребитель `/auth/eid/start` ещё заглушка. Формально AC выполнен (валидатор+тест), фактически в рантайме `return_url` не проверяется.
- **Остатки (LOW):** F2 (пустые каталоги `core.audit/oauth/profiles` + неверный 03-soa.md), F3 (01-api.md ссылается на удалённый `idempotency.py`).

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; статусы тасков сверены по коду.
- [x] Регрессий нет; счётчик 200→204 объяснён (тесты return_url).
- [x] Severity проставлена; «как закрыть» — направление, без кода.
- [x] Расхождение «E17 валидатор без потребителя» и doc-vs-code (F2/F3) зафиксированы, не скрыты.
