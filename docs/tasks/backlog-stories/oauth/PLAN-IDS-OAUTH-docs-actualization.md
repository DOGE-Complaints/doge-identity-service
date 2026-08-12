# PLAN-IDS-OAUTH — Актуализация документации флоу авторизации (выполняемый план)

> **Тип:** executable doc-plan (не стори; план для исполнителя-агента).
> **Дата:** 2026-06-24 · **Эпик:** `EPIC-IDS-OAUTH` / зонтик `EPIC-IDS-ONBOARDING`.
> **Методология:** [`analysis.mdc`](../../../../../.cursor/rules/analysis.mdc) — каждое изменение со ссылкой `file:line`, до/после, сверка с кодом, без фантазий.
> **Источник:** исследование флоу «GPT → submit → авторизация» 2026-06-23/24 (центр — identity). Каноничный флоу — [`04-security §A`](../../../runtime-docs/04-security.md); стык — [`09-gateway-expectations`](../../../runtime-docs/09-gateway-expectations.md).

## Зачем
Флоу-доки identity **устарели в двух осях** и вводят в заблуждение (из-за чего и возникла путаница «куда submit и где /me»):
1. **eID → phone pivot** не отражён: диаграмма и текст говорят `eid_verified` / eID-провайдер, хотя активный механизм — **телефон** (`phone_verified`), eID отложен.
2. **`/me` помечен «501-заглушка»**, хотя он **реально построен** (AUTHCORE-01, phone-поля в [`me_response.py`](../../../../src/core/api/me_response.py)).

Цель: привести флоу-доки к факту кода + phone-модели, **не теряя** eID-знание (помечать DEFERRED), без дублирования уже сделанного (01-api/08-ui — DOC-ONB-05; overview/backend — pivot-баннеры уже добавлены).

## Объём (что трогаем / что НЕ трогаем)
- ✅ Трогаем: [`04-security.md`](../../../runtime-docs/04-security.md) §A + диаграмма, [`09-gateway-expectations.md`](../../../runtime-docs/09-gateway-expectations.md).
- ❌ Не трогаем (покрыто отдельно, чтобы не дублировать): `01-api.md`/`08-ui-expectations.md` → [DOC-IDS-ONB-05](../identity-onboarding/DOC-IDS-ONB-05-runtime-docs-refresh.md); `identity-overview.md`/`identity-backend.md` → уже получили pivot-баннеры (PIVOT 2026-06).

---

## Шаги (выполнять по порядку)

### Шаг 1 — `04-security.md` Часть A (флоу + диаграмма)
**Сверка по коду перед правкой:** `grep -nE "@app\.(get|post)" asgi_app.py` (роуты), `me_response.py` (поля `/me`), `asgi_app.py` (oauth = `_bearer_route`→501).

Правки (с до/после):
- **Таблица «что в коде» (стр.~80-90):** строка `/me` сейчас «🟡 501» → **`/me` ✅ построен** (AUTHCORE-01; phone-поля). Строка eID-старт/callback «501» → **mock готов, реальный провайдер DEFERRED**. Добавить строку **phone-флоу `/auth/phone/request|confirm` ✅ (PV-05)**.
- **Принцип «два вопроса» (стр.20-27):** «прошёл ли он eID?» → «прошёл ли он **верификацию (телефон)**?»; ввести термин `phone_verified` как активный гейт; eID — отложенный альтернативный слой.
- **Sequence-диаграмма (стр.31-65):** заменить eID-ветку на phone:
  - `ID-->>GW: {active, sub, eid_verified}` → `{active, sub, phone_verified}`.
  - `alt eID ещё не пройден … EID-провайдер … profiles.eid_verified=true` → `alt телефон не подтверждён → identity ведёт на verify (inline OTP) → POST /auth/phone/confirm → profiles.phone_verified=true`.
  - Note «если eid_verified=false → 403» → «если `phone_verified=false` → 403 → GPT ведёт на verify».
  - Добавить ремарку, что `/oauth/*` и introspection — **ещё 501/отсутствуют** (target, не as-is).
- **Текст «по шагам» (стр.67-77):** eID→phone аналогично; шаг про introspection — отметить, что endpoint ещё не построен (OAUTH-02).
- **Добавить врезку as-is vs target:** as-is = OAuth 501, introspection нет, gateway intake открыт; target = диаграмма выше.

### Шаг 2 — `09-gateway-expectations.md`
- **§Модель аутентификации (стр.18-24):** `{active, sub, eid_verified}` → `{active, sub, phone_verified}`; «пройден ли eID» → «пройдена ли верификация (телефон)».
- **Таблица «что нужно от identity» (стр.28-32):** строка introspection — `/me` «🟡 501» → **`/me` ✅ построен; `/oauth/introspect` отсутствует** (OAUTH-02).
- **Целевая парадигма (стр.9-16):** «нужна eID-верификация» → «нужна верификация (телефон)»; eID — отложено.

### Шаг 3 — Сверка консистентности
- Проверить, что после правок 04/09 согласуются с [`identity-frontend.md`](../../../../../docs/Identity/identity-frontend.md) (phone), [`identity-onboarding-ux-2026-06-12`](../../../analysis/identity-onboarding-ux-2026-06-12.md) и баннерами overview/backend.
- Проверить ссылки (`file:line`) ещё валидны.

### Шаг 4 (опц.) — Сводный объяснитель
Если нужен один человеческий документ «как идёт submit из GPT» — создать `docs/Identity/identity-submit-flow-explained-2026-06-24.md` (as-is + target, phone-диаграммы), со ссылками в оба репо. Иначе — ограничиться актуализацией 04/09.

## Definition of Done
- [ ] `04-security §A`: диаграмма и текст — **phone** (`phone_verified`), eID помечен DEFERRED; таблица статусов соответствует коду (`/me` ✅, oauth 501, phone ✅).
- [ ] `09-gateway-expectations`: introspection-ответ = `phone_verified`; `/me` не «501».
- [ ] Нет противоречий с frontend.md / onboarding-ux / баннерами overview-backend.
- [ ] Все `file:line` сверены с фактическим кодом; ссылки не битые.
- [ ] Дублирования с DOC-ONB-05 нет (01-api/08-ui не трогали).

## Связь
Питает стори [OAUTH-04](STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) (контракт verify-gate) и [OAUTH-02](STORY-IDS-OAUTH-02-introspection-and-service-token.md) (introspection под phone). Якоря: [`04-security`](../../../runtime-docs/04-security.md), [`09-gateway-expectations`](../../../runtime-docs/09-gateway-expectations.md).
