# Жёсткий аудит исполнения STORY-IDS-EID-06 (браузерный callback: redirect + динамический роут)

> **Дата:** 2026-06-08
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-EID-06-browser-callback-redirect`](../tasks/backlog-stories/eid/STORY-IDS-EID-06-browser-callback-redirect.md) vs фактический код. Исполнена под **EPIC-IDS-09-eid-verification** (pkg-000019), 6 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): EPIC-IDS-09, task queue t01–t06 (pkg-000019).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| `EidCallbackOutcome` | dataclass (outcome/return_url/error_code/json_status) + `build_callback_json_envelope`/`append_eid_redirect_query`/`has_safe_redirect_target` ([eid_callback.py](../../src/core/api/eid_callback.py)) |
| Хендлер возвращает исход | `handle_auth_eid_callback(...) -> EidCallbackOutcome` ([handlers.py:191-197](../../src/core/api/handlers.py)) |
| Динамический роут | один `GET /auth/{provider}/callback` ([asgi_app.py:242-261](../../src/core/api/asgi_app.py)); старые литеральные mock/eideasy/authentigate-роуты **удалены** |
| Render + negotiate | `_render_eid_callback_outcome`: JSON по `Accept: application/json`, иначе 303 при safe target, иначе JSON-fallback ([asgi_app.py:77-97](../../src/core/api/asgi_app.py)) |
| Тесты | [test_eid_callback_redirect.py](../../tests/test_eid_callback_redirect.py) — 7 |
| **Offline-сюита** | **232 passed, 10 deselected** ✅ (было 225 → +7) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-09, pkg-000019) | Факт | Статус |
|--------------------------------|------|--------|
| t01 eid callback outcome dataclass | `EidCallbackOutcome` + хелперы рендера ([eid_callback.py](../../src/core/api/eid_callback.py)); хендлер возвращает его | 🟢 |
| t02 dynamic callback route + registry guard | `GET /auth/{provider}/callback`; `registry.get(provider)` → `ProviderNotRegisteredError`/`ConfigError` для незарегистрированного ([asgi_app.py:242-254](../../src/core/api/asgi_app.py)) | 🟢 |
| t03 callback redirect render + accept negotiate | 303 на `return_url` с `eid_status`/`eid_error`; JSON по `Accept` ([asgi_app.py:77-97](../../src/core/api/asgi_app.py), [eid_callback.py append/has_safe](../../src/core/api/eid_callback.py)) | 🟢 |
| t04 offline redirect + json regression tests | [test_eid_callback_redirect.py](../../tests/test_eid_callback_redirect.py) (7); EID-01/EID-05 тесты обновлены на `Accept: application/json` | 🟢 |
| t05 SPA-first runtime docs | [06-eid-providers §Браузерный callback и SPA-first redirect](../runtime-docs/06-eid-providers.md), [08-ui §SPA-first](../runtime-docs/08-ui-expectations.md) | 🟢 |
| t06 story acceptance verification | AC 6/6 (см. §2) | 🟢 |
| **STORY-IDS-EID-06** | callback-redirect + динамический роут | **🟢 Done** |

Индекс ([`bullrun-launch-index.md:64`](../tasks/bullrun-launch-index.md)) держит эпик `🟡 In Progress — EID-01/03/04/05/06 🟢` — корректно.

---

## 2. Сверка Acceptance Criteria story (по коду + тестам)

| AC | Факт | Вердикт |
|----|------|---------|
| `handle_auth_eid_callback` → `EidCallbackOutcome` | handlers.py:197; тест `test_handle_auth_eid_callback_returns_outcome_type` | ✅ |
| Браузер: успех → 303 `?eid_status=verified`; ошибка → `?eid_status=error&eid_error=<код>` | `_render_eid_callback_outcome` + `append_eid_redirect_query`; тесты `..._browser_redirects_with_verified_marker`, `..._provider_error_redirects_with_canonical_marker` | ✅ |
| Неизвестная сессия/return_url → безопасный 400, без open-redirect | `has_safe_redirect_target` False → JSON-fallback; тест `test_unknown_session_callback_returns_400_without_redirect` | ✅ |
| Один `/auth/{provider}/callback`; +провайдер без нового роута; незарегистр. → `ConfigError` | старые 3 роута удалены; `registry.get` guard; тесты `..._unregistered_provider..._raises_config_error`, `..._dynamic..._resolves_mock_provider` | ✅ |
| Mock-флоу EID-01 проходит (JSON-вариант сохранён) | EID-01 тесты добавили `Accept: application/json` → JSON-исход; тест `..._json_variant_returns_verified_envelope`; 232 passed | ✅ |
| Доки отражают SPA-first; offline зелёный | 06/08 обновлены; 232 passed | ✅ |

**Вывод:** все 6 AC выполнены и покрыты тестами (7 dedicated). F1🔴/F6/F11 Authentigate-аудита закрыты.

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| F1 | MEDIUM | Doc-stale | backlog-story помечена `⚪ Todo` (стр.6), реально 🟢 Done под `EPIC-IDS-09` (pkg-000019); «Точки в коде» описывают старое состояние (JSON-исход `handlers.py:327-330`, захардкоженные роуты `asgi_app.py:214-248`) | [`STORY-IDS-EID-06...md:6,25-29`](../tasks/backlog-stories/eid/STORY-IDS-EID-06-browser-callback-redirect.md) |

Иных материальных findings нет. Наблюдение (severity none): роут вызывает `registry.get(provider)` (guard) и затем оркестратор внутри снова резолвит провайдера — двойной dict-lookup, безвредно.

### Положительно: закрыт carry-over из EID-05-аудита
Прошлый аудит EID-05 отметил F2 — устаревшую секцию реестра в [06-eid-providers](../runtime-docs/06-eid-providers.md) («KeyError ловушка, только mock»). В EID-06 (правка 06 под F11) она **реконсилирована**: стр.41 теперь «`get` … бросает `ProviderNotRegisteredError` (`ConfigError`, не `KeyError`)», стр.45 — про stub без голого KeyError. Внутреннее противоречие 06 устранено.

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **232 passed** (было 225 → +7 callback-redirect тестов), **ожидаемо** |
| Callback JSON→redirect | поведенческая смена: по умолчанию (браузерный Accept) теперь 303; JSON только по `Accept: application/json` |
| EID-01/EID-05 тесты | обновлены `Accept: application/json` → JSON-исход сохранён, не сломаны (часть 232 passed) |
| 3 захардкоженных callback-роута | удалены, заменены одним `/auth/{provider}/callback` — не регресс (mock redirect_url `/auth/mock/callback?...` матчит `{provider}=mock`) |
| Безопасность open-redirect | redirect только на сохранённый (allowlisted на старте) `return_url`; нет return_url → JSON 400 |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-EID-06 — 🟢 исполнена полно:** `EidCallbackOutcome` (transport-agnostic), 303-redirect в SPA с `eid_status`/`eid_error`, безопасный fallback без open-redirect, один параметризованный `/auth/{provider}/callback` с registry-guard, JSON-вариант для тестов сохранён. AC 6/6, 7 тестов. F1🔴/F6/F11 Authentigate-аудита закрыты.
- **Единственный finding — F1 (doc-stale backlog-story)**, рекуррентный паттерн.
- Бонус: попутно закрыт carry-over F2 из EID-05-аудита (06-doc реестр приведён к факту).

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; статусы тасков сверены по коду.
- [x] AC сверены по коду **и** тестам; критичный AC5 (EID-01 не сломан) проверен — тесты получили `Accept: application/json`, 232 passed.
- [x] Старые роуты подтверждены удалёнными; open-redirect-защита прослежена (redirect только на allowlisted return_url).
- [x] Регрессий нет; 225→232 объяснён; carry-over из EID-05 отмечен как закрытый.
