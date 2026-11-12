# Re-audit #2 закрытия gap-листа STORY-IDS-OAUTH-02 (F2/F3/F4)

> **Дата:** 2026-06-24
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — каждый gap проверен по фактическому файлу/коду (`file:line`).
> **Контекст:** в [re-audit #1](./epic-ids-11-oauth-02-reaudit-2026-06-24.md) был закрыт только F1; F2/F3/F4 оставались открыты. Эта проверка — после повторной правки.
> **Итог:** **4/4 закрыты** (F1 ранее + F2/F3/F4 теперь). Регрессий нет — **351 passed** (+1 новый pilot-тест).

## Сводка

| ID | Severity | Тип | Проверка по факту | Вердикт |
|----|----------|-----|-------------------|---------|
| F1 | MEDIUM | doc (backlog-story) | закрыт в re-audit #1 | 🟢 Закрыт |
| F2 | MEDIUM | doc (пакет-индекс) | OAUTH-02 🟢 Done в составе + статус-строке | 🟢 **Закрыт** |
| F3 | MEDIUM | cross-doc drift (04/09) | «introspection ✅ построен», «сервисный gate ✅» | 🟢 **Закрыт** |
| F4 | MEDIUM | security (pilot fail-fast) | `SERVICE_API_TOKEN` в `pilot_required` + тест | 🟢 **Закрыт** |

---

## F4 — security: сервисный гейт enforced в pilot → 🟢 ЗАКРЫТ

- **Pilot fail-fast:** `SERVICE_API_TOKEN` добавлен в `pilot_required` ([schema.py:184](../../src/core/config/schema.py)) — при пустом значении `raise ConfigError("SERVICE_API_TOKEN is required for APP_PROFILE=pilot")` ([schema.py:185-187](../../src/core/config/schema.py)). ✅
- **Тест:** `test_pilot_requires_service_api_token` ([test_config_schema.py:136-137](../../tests/test_config_schema.py)) — `pytest.raises(ConfigError, match="SERVICE_API_TOKEN")`. ✅
- **Следствие:** в `APP_PROFILE=pilot` сервис не стартует без токена ⇒ `ServiceTokenAuth` гарантированно `is_enabled()` ([security.py:105-110](../../src/core/api/security.py)) ⇒ `/oauth/introspect` ([asgi_app.py:407-416](../../src/core/api/asgi_app.py)) защищён `require_service_token`. Утечки `{active, sub, phone_verified}` в проде больше нет.

**Остаточное (observation, не gap):** в `APP_PROFILE=demo` `ServiceTokenAuth.require` остаётся no-op при незаданном токене ([security.py:109-110](../../src/core/api/security.py)) — `/oauth/introspect` открыт. Это согласованная demo-поза (как и весь demo-профиль); прод закрыт через pilot fail-fast. Severity none.

---

## F2 — пакет-индекс → 🟢 ЗАКРЫТ

[`oauth/EPIC-IDS-OAUTH.md`](../tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md):
- **Pipeline (стр.5):** «OAUTH-01 🟢, OAUTH-02 🟢 Done; pkg-000029, pkg-000030» ✅.
- **Назначение (стр.8):** «**OAUTH-01** и **OAUTH-02 построены** (… `POST /oauth/introspect` …); durable store — OAUTH-03» ✅.
- **Состав (стр.18):** `STORY-IDS-OAUTH-02 … | 🟢 Done (pipeline, pkg-000030)` ✅.
- **Статус-строка (стр.22):** «OAUTH-01 и OAUTH-02 — **🟢 Done** (… `POST /oauth/introspect`, service token gate); OAUTH-03..04 — ⚪ Todo» ✅.
- **Порядок (стр.29):** «OAUTH-01 ✅ → **OAUTH-02 ✅** → OAUTH-03 → OAUTH-04» ✅.

Стале́ость «OAUTH-02 ⚪ / introspection не построены» устранена полностью.

---

## F3 — cross-doc drift (04-security / 09) → 🟢 ЗАКРЫТ

| Док:строка | Стало | Факт-якорь |
|------------|-------|------------|
| [`04-security:68`](../runtime-docs/04-security.md) as-is врезка | «introspection-endpoint `POST /oauth/introspect` — **✅ построен** (OAUTH-02); сервисный gate — `SERVICE_API_TOKEN`/`ServiceTokenAuth` (обязателен в `APP_PROFILE=pilot`)» | ✅ |
| [`04-security:92`](../runtime-docs/04-security.md) таблица | «introspection-endpoint … `introspection.py`, `asgi_app.py:407-416` \| ✅ построен (OAUTH-02)» | ✅ |
| [`09-gateway:32`](../runtime-docs/09-gateway-expectations.md) | «`/oauth/introspect` — ✅ **построен** (`introspection.py`, OAUTH-02) \| ✅» | ✅ |
| [`09-gateway:34`](../runtime-docs/09-gateway-expectations.md) | «`AppConfig.service_api_token` + `ServiceTokenAuth` … обязателен в `APP_PROFILE=pilot` \| ✅» | ✅ |
| [`09-gateway:47`](../runtime-docs/09-gateway-expectations.md) Итог | «OAuth-выдача и **introspection+сервисный gate построены** (OAUTH-01, OAUTH-02); gateway intake — ещё не подключён» | ✅ |

Прежняя фактически неверная строка «в identity-конфиге **нет** `SERVICE_API_TOKEN`» (09:34) исправлена на «есть + обязателен в pilot». Замечание из re-audit #1 (не писать «защищено» при открытом F4) — снято: F4 закрыт, а формулировка корректно ограничена «обязателен в pilot».

---

## Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **351 passed, 11 deselected** (было 350 → **+1**: `test_pilot_requires_service_api_token`) |
| Изменение кода | `schema.py` `pilot_required` += `SERVICE_API_TOKEN` (фейл-фаст); поведение demo не изменено |
| `ServiceTokenAuth`/introspect-роут | без изменений (защита включается конфигом) |
| Прочие OAuth/phone/eID-тесты | зелёные |

Регрессий нет; прирост +1 объяснён новым тестом.

---

## Итог
- **4/4 gap закрыты:** F1 (backlog-story, ранее), **F2** (пакет-индекс: OAUTH-02 🟢), **F3** (04-security/09: «introspection+gate построены»), **F4** (security: `SERVICE_API_TOKEN` в pilot fail-fast + тест).
- **F4 — главный (security)** — закрыт правильным механизмом: фейл-фаст конфига в pilot (а не точечный guard), что согласуется с `OAUTH_ACCESS_TOKEN_SECRET`/`GPT_OAUTH_CLIENT_SECRET`.
- **Регрессий нет** (351 passed, +1 тест).
- **Остаточное (observation, не gap):** demo-профиль оставляет introspect открытым (no-op gate) — согласованная demo-поза; прод закрыт.

## Quality gate (analysis.mdc)
- [x] Каждый gap перепроверен по фактическому файлу/коду с `file:line`.
- [x] F4 подтверждён двумя независимыми точками: `pilot_required` (schema.py:184) **и** тест `test_pilot_requires_service_api_token`.
- [x] F3: строка 09:34 (ранее фактически неверная) проверена на исправление.
- [x] Регрессий нет; +1 тест объяснён; demo-остаток зафиксирован честно как observation.
