# Жёсткий аудит исполнения DOC-IDS-ONB-01 (контракт «ленивого гейта телефона»)

> **Дата:** 2026-06-26
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity. Не предлагаю реализацию — только findings.
> **Предмет:** [`DOC-IDS-ONB-01-lazy-phone-gate-contract`](../tasks/backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md) — **doc task** (deliverable = задокументированный контракт в 2 целевых файлах, не код). Исполнена под **EPIC-IDS-13** (pkg-000040), 5 tasks.
> **Тип проверки:** doc-task → сверка DoD c фактическими доками **+** точность процитированных code-фактов.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): pkg-000040, DOC-ONB-01 🟢 (стр.11,132,674-682,720).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| 09 целевая секция | «**Ленивый гейт телефона (web signup, enforce на потребителе)**» — [09-gateway-expectations.md:28](../runtime-docs/09-gateway-expectations.md) |
| 08-ui целевая секция | §3b «**Ленивый гейт: verify-экран по защищённому действию**» — [08-ui-expectations.md:26-43](../runtime-docs/08-ui-expectations.md) |
| Code-факт: `phone_verified` | `data["phone_verified"] = profile.phone_verified` — [me_response.py:42](../../src/core/api/me_response.py) (цитата в доках **line-accurate**) |
| Gateway-путь | introspection `{active, sub, phone_verified}` — [introspection.py](../../src/core/oauth/introspection.py), OAUTH-02 ✅ |
| PV-05 флоу | `/auth/phone/request` → `/auth/phone/confirm` — существуют (PV-05 🟢) |
| Канон «истории — в gateway» | в identity **нет** story-роутов (grep `@app.*stor` → пусто) — контракт корректен |
| SSOT-ссылки | PV-05 pipeline-стори + [`onboarding-phone-verification-api.md`](../runbook/onboarding-phone-verification-api.md) — **резолвятся** |
| **Offline-сюита** | **386 passed, 12 deselected** ✅ (docs-only волна — без изменений кода) |

---

## 1. Актуализация тасков и story (по факту)

| Таск (EPIC-IDS-13, pkg-000040) | Факт | Статус |
|--------------------------------|------|--------|
| t01 lazy gate doc gap audit | аудит разрыва (где контракт не описан) | 🟢 |
| t02 gateway lazy phone gate section | §«Ленивый гейт» в [09:28-41](../runtime-docs/09-gateway-expectations.md) | 🟢 |
| t03 ui lazy verify screen expectation | §3b в [08-ui:26-43](../runtime-docs/08-ui-expectations.md) | 🟢 |
| t04 pv05 runbook crosslinks sequence | ссылки на PV-05 + `onboarding-phone-verification-api.md` + sequence | 🟢 |
| t05 story acceptance verification | DoD 4/4 (см. §2) | 🟢 |
| **DOC-IDS-ONB-01** | контракт «ленивого гейта телефона» | **🟢 Done** |

**Индекс корректен:** `EPIC-IDS-13 … 🟡 In Progress — DOC-ONB-01 🟢` ([bullrun-launch-index.md:132](../tasks/bullrun-launch-index.md)); pkg-000040 Done. Backlog-story `Status: 🟢 Done`, DoD все `[x]` — **синхронно** (F1-дрейфа чекбоксов, как у SEC-стори, здесь нет).

---

## 2. Сверка Definition of Done (по факту доков + code)

| DoD | Факт | Вердикт |
|-----|------|---------|
| В `09-gateway-expectations` описан контракт: consumer читает `phone_verified`, иначе verify | [09:34-40](../runtime-docs/09-gateway-expectations.md) — «Контракт (gateway/spa перед действием)»: spa→`GET /me`, gateway→introspection; `false` → не выполнять, вести на verify | ✅ |
| В `08-ui-expectations` — ожидание verify-экрана по `phone_verified=false` | [08-ui §3b:30-39](../runtime-docs/08-ui-expectations.md) — перед защищённым действием `GET /me`, при `false` показать verify-экран (inline) | ✅ |
| Каноничный пример (создание стори) + явно enforce-на-потребителе | пример «создать/опубликовать стори» ([08-ui §3b:30](../runtime-docs/08-ui-expectations.md)); «enforce — на потребителе (spa-app / gateway)» ([09:32](../runtime-docs/09-gateway-expectations.md), [08-ui:43](../runtime-docs/08-ui-expectations.md)) | ✅ |
| Ссылка на PV-05 и `onboarding-phone-verification-api.md` | [08-ui §3b:41](../runtime-docs/08-ui-expectations.md) SSOT-блок: PV-05 pipeline + runbook + 09 | ✅ |

**Вывод:** все 4 DoD выполнены; контракт **двухсторонний** (spa-app via `/me`, gateway via introspection), enforce явно вынесен на потребителя (identity provider-agnostic — story-роутов нет), процитированные code-факты точны (`me_response.py:42`). Архитектурно корректно: identity отдаёт флаг + флоу, не перехватывает действие.

---

## 3. Findings (severity + как закрыть; без реализации)

Контракт-deliverable — без материальных дефектов. Findings — мелкая doc-консистентность.

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | LOW | Doc-stale (само-противоречие пакет-индекса) | В [`EPIC-IDS-ONBOARDING.md`](../tasks/backlog-stories/identity-onboarding/EPIC-IDS-ONBOARDING.md) §«Актуальность» (стр.42,44) написано, что DOC-ONB-01 «✅ уже покрыт … **а не отдельной волной онбординга**» — но он **материализован** отдельной волной **pkg-000040 / EPIC-IDS-13** (5 tasks). Состав-строка уже 🟢, но прозаический текст рядом противоречит. **Как закрыть:** в §«Актуальность» отметить «DOC-ONB-01 формализован под EPIC-IDS-13 (pkg-000040)». | [`EPIC-IDS-ONBOARDING.md` §Актуальность](../tasks/backlog-stories/identity-onboarding/EPIC-IDS-ONBOARDING.md) |
| **F2** | LOW | Cross-doc (eID-эра во вступлении) | [09-gateway-expectations.md:5](../runtime-docs/09-gateway-expectations.md) вступление всё ещё формулирует роль identity как «подтверждает … прошёл **eID**» — покрыто phone-pivot-баннером ([09:11](../runtime-docs/09-gateway-expectations.md)), но первая фраза читается eID-first. Не scope DOC-ONB-01. **Как закрыть:** в опционе — «прошёл верификацию (телефон)» во вступлении (или оставить на баннер). | [09-gateway-expectations.md:5](../runtime-docs/09-gateway-expectations.md) |

Наблюдения (severity none, **не gaps**):
- **O1:** DOC-ONB-01 — это **consumer-side контракт** (spa-app + gateway), а не identity-backend код; «Вне scope» story явно исключает код гейта в identity ([DOC-ONB-01:24-26](../tasks/backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md)) — соответствует факту (story-роутов в identity нет).
- **O2:** контракт ссылается на gateway-enforcement, который живёт в **репозитории gateway** (не identity) — здесь зафиксирован только identity-side контракт (флаг + флоу). Консистентно с [09](../runtime-docs/09-gateway-expectations.md).

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **386 passed, 12 deselected** — без изменений (docs-only волна pkg-000040, код не трогался) |
| Изменённые файлы | `09-gateway-expectations.md` (+§28), `08-ui-expectations.md` (+§3b) — аддитивные секции |
| Цитаты в доках vs код | `me_response.py:42` = `phone_verified` — точно; PV-05/introspection/runbook-ссылки резолвятся |

Регрессий нет (документация; код не затронут).

---

## 5. Итог

- **DOC-IDS-ONB-01 — 🟢 исполнена полно:** контракт «ленивого гейта телефона» задокументирован в обоих целевых файлах ([09 §28](../runtime-docs/09-gateway-expectations.md), [08-ui §3b](../runtime-docs/08-ui-expectations.md)) — двухсторонний (spa `/me` + gateway introspection), enforce-на-потребителе явно, канон-пример (создание стори), ссылки на PV-05/runbook. DoD 4/4, code-факты точны. Таски t01–t05 🟢; индекс корректен, backlog-story синхронна (без F1-дрейфа).
- **Findings — только мелкая doc-консистентность:** **F1 (LOW)** — прозаический текст §«Актуальность» в пакет-индексе противоречит факту материализации (pkg-000040); **F2 (LOW)** — eID-эра во вступлении 09 (покрыто баннером). Наблюдения O1/O2 — это consumer-side контракт, не identity-backend.
- **Регрессий нет** (386 passed).

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 5 тасков + story + 4 DoD сверены по фактическим докам и коду.
- [x] Doc-task проверен правильно: deliverable = контракт в 09/08-ui; обе секции существуют и полны.
- [x] Точность процитированных code-фактов проверена (`me_response.py:42` = `phone_verified`; story-роутов в identity нет).
- [x] SSOT/cross-ссылки (PV-05 pipeline, runbook) резолвятся.
- [x] Регрессий нет (docs-only; 386 = факт). F1/F2 (LOW doc-консистентность) отделены от выполненного контракта.
