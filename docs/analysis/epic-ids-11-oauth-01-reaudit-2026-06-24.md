# Re-audit закрытия gap-листа STORY-IDS-OAUTH-01 (F1/F2/F3)

> **Дата:** 2026-06-24
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — закрытие каждого gap проверено по фактическому файлу/коду (`file:line`), регрессии, остаточные.
> **Источник gap-листа:** [`epic-ids-11-oauth-01-audit-2026-06-24.md`](./epic-ids-11-oauth-01-audit-2026-06-24.md) §3 (F1 MEDIUM, F2 MEDIUM, F3 MEDIUM).
> **Итог:** **3/3 закрыты.** Регрессий нет (341 passed). Остаточное: 2 мелких (LOW) — в Scope-описании и в историческом PLAN.

## Сводка

| ID | Severity | Было | Стало | Вердикт |
|----|----------|------|-------|---------|
| F1 | MEDIUM | backlog-story `⚪ Todo`, AC `[ ]`, «точки в коде» = 501/«стора нет» | Status `🟢 Done`, 8×AC `[x]`, точки → `core/oauth/`, `verify_client_secret`, SEC-1 закрыт | 🟢 Закрыт (1 LOW-остаток) |
| F2 | MEDIUM | пакет-индекс `EPIC-IDS-OAUTH.md`: «OAUTH-01 ⚪, /oauth/* 501» | OAUTH-01 🟢 Done, «построен», SEC-1 ✅, статус-строка 2026-06-24 | 🟢 Закрыт |
| F3 | MEDIUM | `04-security §A`/`09`/OAUTH-02/03/04 держат «OAuth 501» | везде «✅ построен (OAUTH-01)» | 🟢 Закрыт |

---

## F1 — backlog-story doc-stale → 🟢 ЗАКРЫТ

[`STORY-IDS-OAUTH-01...md`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md):
- **Status:** `⚪ Todo` → **`🟢 Done`** (стр.6) ✅.
- **AC:** все 8 — `[x]` (стр.36-43) ✅.
- **«Точки в коде»:** обновлены под факт — Handlers `core/oauth/handlers.py` (стр.28), `client_secret проверяется` через `verify_client_secret` ([repositories.py:495-501](../../src/core/infrastructure/repositories.py)), «SEC-1 закрыт» (стр.31) ✅.

**Остаток (LOW):** Scope стр.18 всё ещё пишет «**В движке этого стора пока нет** — добавить» про `authorization_request`-store, хотя `InMemoryAuthorizationRequestStore` уже существует ([repositories.py:431](../../src/core/infrastructure/repositories.py)). Это present-tense факт-claim в Scope-описании. **Как закрыть:** убрать «пока нет — добавить» (или переформулировать в прошедшем). Не SSOT-критично (AC/точки уже верны).

---

## F2 — пакет-индекс → 🟢 ЗАКРЫТ

[`oauth/EPIC-IDS-OAUTH.md`](../tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md):
- Эпик-статус: `🟡 In Progress`; добавлена строка `Pipeline: EPIC-IDS-11 (OAUTH-01 🟢 Done, pkg-000029)` (стр.3,5) ✅.
- Назначение: «**OAUTH-01 построен** (маршруты `/oauth/*` подключены, `core/oauth/`)» (стр.8) ✅; «gaps SEC-1 ✅» (стр.11) ✅.
- Состав: OAUTH-01 = **🟢 Done** (pipeline, pkg-000029) (стр.17); OAUTH-02/03/04 зависят от «OAUTH-01 ✅» (стр.18-20) ✅.
- Статус-строка 2026-06-24 (стр.22): OAUTH-01 🟢, 02..04 ⚪ — точно ✅.
- Порядок: «OAUTH-01 ✅ → …» (стр.29) ✅.
- В файле **не осталось** «/oauth/* = 501» как факта.

---

## F3 — cross-doc «OAuth 501» → 🟢 ЗАКРЫТ

| Док | Было | Стало |
|-----|------|-------|
| [`04-security §A`](../runtime-docs/04-security.md) as-is врезка (стр.68) | «OAuth-роуты /oauth/* = 501» | «OAuth-маршруты `/oauth/*` — **✅ построены** (OAUTH-01)» ✅ |
| `04-security §A` таблица (стр.89) | «OAuth-маршруты 🟡 501» | «`asgi_app.py:368-403`, `core/oauth/handlers.py` \| ✅ построен (OAUTH-01)» ✅ |
| `04-security §B` (стр.111) | «client_secret не проверяется; наружу не подключён» | «`client_secret` проверяется (`verify_client_secret`, SEC-1 закрыт); подключён через `core/oauth/handlers.py`» ✅ |
| [`09-gateway-expectations`](../runtime-docs/09-gateway-expectations.md) (стр.33,47) | «Выдача OAuth-токена 🟡» | «`core/oauth/handlers.py` … ✅ (OAUTH-01)»; Итог «OAuth-выдача **построена** (OAUTH-01)» ✅ |
| [`OAUTH-02`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md) (стр.8) | «OAUTH-01 выдаёт токен» (нейтрально) | «OAUTH-01 … **🟢 построен**, pkg-000029» ✅ |
| [`OAUTH-03`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) (стр.9) | «OAUTH-01 (вводит handshake)» | «OAUTH-01 **🟢 построен** … pkg-000029» ✅ |
| [`OAUTH-04`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) (стр.9,27) | «`/oauth/*` = 501» | «`/oauth/*` — **построены** (OAUTH-01 ✅)» ✅ |

Sweep по «501» в живых доках: остаточные упоминания **только** там, где они корректны:
- `OAUTH-02` «`/me` уже построен (**не** 501)» / «прежняя пометка 501 устарела» — верные утверждения.
- `PLAN-IDS-OAUTH-docs-actualization.md` — **исторический executed-план** (описывает пред-состояние, которое чинили); помечен 🟢 Выполнен. См. остаток ниже.

**Остаток (LOW):** в [`PLAN-IDS-OAUTH-docs-actualization.md`](../tasks/backlog-stories/oauth/PLAN-IDS-OAUTH-docs-actualization.md) DoD-пункт (стр.50) «таблица статусов соответствует коду (`/me` ✅, **oauth 501**, phone ✅)» теперь сам-противоречив (oauth построен). Это чек-лист в **выполненном** плане (исторический артефакт, не live-SSOT). **Как закрыть:** пометить DoD как достигнутый по факту (oauth уже не 501) либо архивировать план.

---

## Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **341 passed, 11 deselected** — **без изменений** (gap-фиксы doc-only, код не трогался) |
| Индекс vs факт | bullrun «341 pytest offline» = факт 341 ✅ |
| Код OAuth (`core/oauth/`, security, repositories) | не изменён — поведение прежнее |

Регрессий нет.

---

## Итог
- **F1/F2/F3 — закрыты** по фактическим файлам: backlog-story (🟢 + AC + точки), пакет-индекс (OAUTH-01 🟢, без «501»), флоу-доки и соседние стори (`04-security`/`09`/OAUTH-02/03/04 → «построен»).
- **Регрессий нет** (341 passed, код не трогался).
- **Остаточное (2× LOW, не SSOT-критично):** (1) Scope стр.18 backlog-story «стора пока нет — добавить» (стор уже есть); (2) PLAN DoD стр.50 «oauth 501» (исторический executed-план). Оба — косметика в не-живых секциях.

## Quality gate (analysis.mdc)
- [x] Каждый gap перепроверен по фактическому файлу с `file:line`; не по заявлению.
- [x] F3 — sweep по «501» во всех живых доках; остаточные «501» только корректные (OAUTH-02 «не 501») или исторические (PLAN).
- [x] Регрессий нет (341 unchanged; код не трогался — gap-лист был doc-only).
- [x] 2 LOW-остатка зафиксированы честно (Scope-claim + executed-PLAN DoD), не выданы за закрытые.
