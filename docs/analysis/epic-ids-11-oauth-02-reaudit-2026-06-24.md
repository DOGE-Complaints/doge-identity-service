# Re-audit закрытия gap-листа STORY-IDS-OAUTH-02 (F1/F2/F3/F4)

> **Дата:** 2026-06-24
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — закрытие каждого gap проверено по фактическому файлу/коду (`file:line`); «NO ignoring discrepancies».
> **Источник gap-листа:** [`epic-ids-11-oauth-02-audit-2026-06-24.md`](./epic-ids-11-oauth-02-audit-2026-06-24.md) §3 (F4 security MEDIUM, F1/F2/F3 doc MEDIUM).
> **Итог:** **1/4 закрыт (F1).** F2, F3, F4 — **остаются открытыми** (по факту кода/файлов правки не внесены). Регрессий нет (350 passed).

## Сводка

| ID | Severity | Тип | Проверка по факту | Вердикт |
|----|----------|-----|-------------------|---------|
| F1 | MEDIUM | doc-stale (backlog-story) | Status 🟢, AC `[x]`, точки «построен» | 🟢 **Закрыт** |
| F2 | MEDIUM | doc-stale (пакет-индекс) | состав OAUTH-02 = ⚪ Todo; статус-строка «не построены» | 🔴 **НЕ закрыт** |
| F3 | MEDIUM | cross-doc drift (04/09) | «introspection отсутствует», «нет SERVICE_API_TOKEN» | 🔴 **НЕ закрыт** |
| F4 | MEDIUM | security (pilot fail-fast) | `SERVICE_API_TOKEN` нет в `pilot_required`; гейт no-op | 🔴 **НЕ закрыт** |

> ⚠️ Заявление «правки по gap-листу выполнены» подтверждается **только для F1**. F2/F3/F4 в фактических файлах/коде не изменены — см. доказательства ниже.

---

## F1 — backlog-story doc-stale → 🟢 ЗАКРЫТ

[`STORY-IDS-OAUTH-02...md`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md):
- **Status:** `🟢 Done` (стр.6) ✅.
- **AC:** 4×`[x]` (стр.31-34) ✅.
- **«Точки в коде»:** «`/oauth/introspect` — **построен**» (стр.25), «`/me` построен» (стр.26), «`SERVICE_API_TOKEN` — **в** `AppConfig.service_api_token`» (стр.27) ✅.

Соответствует коду. Закрыт.

---

## F2 — пакет-индекс → 🔴 НЕ ЗАКРЫТ

[`oauth/EPIC-IDS-OAUTH.md`](../tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md) — стале́ость осталась:
- **Состав (стр.18):** `STORY-IDS-OAUTH-02 … | ⚪ Todo` — а по факту **🟢 Done** (pkg-000030). ❌
- **Статус-строка (стр.22):** «OAUTH-02..04 — **⚪ Todo** (introspection, durable store, verify-gate **не построены**)» — introspection построен. ❌
- **Назначение (стр.8):** «introspection и durable store — OAUTH-02/03» (как невыполненные). ❌
- **Порядок (стр.29):** «…→ **OAUTH-02** (introspection + сервисный токен…)» как предстоящий. ❌

**Как закрыть:** OAUTH-02 → 🟢 в составе (стр.18) и статус-строке (стр.22); снять «introspection не построены»; в «Порядке» пометить OAUTH-02 ✅.

---

## F3 — cross-doc drift (04-security / 09) → 🔴 НЕ ЗАКРЫТ

Обе живые SSOT-доки всё ещё описывают introspection и сервисный токен как **отсутствующие** (после билда OAUTH-02 это неверно):

| Док:строка | Текущий (stale) текст | Факт |
|------------|------------------------|------|
| [`04-security:68`](../runtime-docs/04-security.md) as-is врезка | «introspection-endpoint **отсутствует** (OAUTH-02)» | `/oauth/introspect` построен |
| [`04-security:92`](../runtime-docs/04-security.md) таблица | «introspection-endpoint … ❌ **отсутствует** (OAUTH-02)» | построен ([introspection.py](../../src/core/oauth/introspection.py)) |
| [`04-security:93`](../runtime-docs/04-security.md) таблица | «Проверка сервисного токена … ❌ **нет** `SERVICE_API_TOKEN` в конфиге» | `service_api_token` в `AppConfig` ([schema.py:70,238](../../src/core/config/schema.py)) |
| [`04-security:95`](../runtime-docs/04-security.md) вывод | «пока нет **introspection-endpoint** и **проверки сервисного токена**» | оба построены |
| [`09-gateway-expectations:32`](../runtime-docs/09-gateway-expectations.md) | «`/oauth/introspect` — **отсутствует** (OAUTH-02) … 🟡» | построен |
| [`09-gateway-expectations:34`](../runtime-docs/09-gateway-expectations.md) | «в identity-конфиге **нет** `SERVICE_API_TOKEN` … ❌» | **фактически неверно** — есть |
| [`09-gateway-expectations:47`](../runtime-docs/09-gateway-expectations.md) Итог | «нет introspection-endpoint, нет проверки сервисного токена» | оба построены |

**Как закрыть:** заменить «отсутствует/нет» → «✅ построен (OAUTH-02)»; строку 09:34 «нет SERVICE_API_TOKEN» — на «есть (`service_api_token`)»; обновить итоги 04:95 / 09:47. ⚠️ С оговоркой F4 (гейт включается только при заданном токене — см. ниже), чтобы не записать «защищено» там, где по умолчанию open.

---

## F4 — security: сервисный гейт не enforced в pilot → 🔴 НЕ ЗАКРЫТ

Код **не изменён**:
- `pilot_required` ([schema.py:174-184](../../src/core/config/schema.py)) — **без** `SERVICE_API_TOKEN` (есть `OAUTH_ACCESS_TOKEN_SECRET`, `GPT_OAUTH_CLIENT_SECRET`, но не сервисный токен). ❌
- `ServiceTokenAuth.from_secret("")` → `disabled()`; `require()` при `is_enabled()=false` — **no-op** ([security.py:108-110](../../src/core/api/security.py)). ❌
- Роут `/oauth/introspect` ([asgi_app.py:407-416](../../src/core/api/asgi_app.py)) — без отдельного guard/503 при выключенном гейте. ❌

⇒ при незаданном `SERVICE_API_TOKEN` (вкл. **pilot**) `/oauth/introspect` остаётся **открытым** — раскрытие `{active, sub, phone_verified}` без аутентификации. Подтверждено: новых тестов на pilot-enforcement сервисного токена нет (`grep` по `tests/` — только дефолт-`""` кейсы).

**Как закрыть:** добавить `("SERVICE_API_TOKEN", _value(env, "SERVICE_API_TOKEN", ""))` в `pilot_required` **либо** default-deny на `/oauth/introspect`, когда гейт выключен; покрыть тестом «pilot без `SERVICE_API_TOKEN` → ConfigError» или «introspect без гейта → 401/503».

---

## Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **350 passed, 11 deselected** — без изменений |
| Код (`schema.py`, `security.py`, `introspection.py`, `asgi_app.py`) | по факту не менялся (F4 требует кода — не внесён) |
| F1-правка (backlog-story) | doc-only, на сюиту не влияет |

Регрессий нет (и не ожидалось — изменён только 1 doc-файл).

---

## Итог
- **Закрыт только F1** (backlog-story актуализирована: 🟢, AC `[x]`, точки «построен»).
- **F2 — НЕ закрыт:** пакет-индекс [`EPIC-IDS-OAUTH.md`](../tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md) держит OAUTH-02 ⚪ Todo + «introspection не построены» (стр.18,22,8,29).
- **F3 — НЕ закрыт:** [`04-security`](../runtime-docs/04-security.md) (стр.68,92,93,95) и [`09-gateway-expectations`](../runtime-docs/09-gateway-expectations.md) (стр.32,34,47) всё ещё пишут «introspection отсутствует / нет SERVICE_API_TOKEN» — последнее **фактически неверно**.
- **F4 — НЕ закрыт (security):** `SERVICE_API_TOKEN` не в pilot-fail-fast, гейт no-op при незаданном токене → introspect открыт в проде.

**Рекомендация:** F4 — приоритет (security/info-disclosure); F2/F3 — doc-sync под факт OAUTH-02. Реализацию не предлагаю — только «как закрыть» в каждом разделе.

## Quality gate (analysis.mdc)
- [x] Каждый gap перепроверен по фактическому файлу/коду с `file:line`, не по заявлению «выполнено».
- [x] Расхождение «заявлено выполнено vs по факту» зафиксировано честно (F2/F3/F4 открыты) — «NO ignoring discrepancies».
- [x] F4 подтверждён по `pilot_required` (нет ключа) + `ServiceTokenAuth.disabled` no-op + отсутствие теста.
- [x] F3: строка 09:34 «нет SERVICE_API_TOKEN» помечена как фактически неверная (есть в `AppConfig`).
- [x] Регрессий нет (350 unchanged; код не менялся).
