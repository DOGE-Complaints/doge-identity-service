# STORY-IDS-EID-06 — Браузерный callback: redirect-рендеринг и динамический роут

## Meta
- **Key:** `STORY-IDS-EID-06-browser-callback-redirect`
- **Parent Epic:** [`../../../../EPIC-IDS-09-eid-verification.md`](../../../../EPIC-IDS-09-eid-verification.md)
- **Epic alias (код/backlog):** `EPIC-IDS-EID`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md`](../../../../backlog-stories/eid/STORY-IDS-EID-06-browser-callback-redirect.md)
- **Decision Ref:** [`../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md`](../../../../backlog-stories/eid/STORY-IDS-EID-06-browser-callback-redirect.md); [`authentigate-compatibility-audit-2026-06-07`](../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F1 🔴, F6, F11)
- **Источник:** аудит [`authentigate-compatibility-audit-2026-06-07`](../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F1 🔴, F6, F11)
- **Зависит от:** [STORY-IDS-EID-05-canonical-provider-contract](../STORY-IDS-EID-05-canonical-provider-contract/STORY-IDS-EID-05-canonical-provider-contract.md) (коды `EidErrorCode` для маркера), [STORY-IDS-EID-03-provider-plugin-backbone](../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md) (реестр для резолва провайдера в роуте)

## Зачем простыми словами
Реальный eID-провайдер после логина **редиректит браузер пользователя** на наш callback — а сейчас callback отдаёт **JSON**, и человек застрянет на странице с JSON вместо возврата в приложение. Это блокер живого флоу. Нужно: callback завершается HTTP-redirect'ом обратно в SPA на сохранённый `return_url` с пометкой результата. Заодно убираем хардкод отдельного роута под каждого провайдера — один параметризованный роут на всех.

## Scope
- **`EidCallbackOutcome` (новый dataclass):** `outcome: Literal["verified","already_verified","failed"]`, `return_url: str | None`, `error_code: EidErrorCode | None`, `json_status: int`. `handle_auth_eid_callback` возвращает его вместо `(dict,int)`.
- **Redirect-рендер на уровне роута:** callback завершается `RedirectResponse(303)` на `session.return_url` с маркером `?eid_status=verified` либо `?eid_status=error&eid_error=<canonical-code>`. `return_url` уже прошёл allowlist на старте ([`validate_return_url`](../../../../../../src/core/security/return_url.py)) и хранится в сессии.
- **Безопасный фолбэк:** если сессия/`return_url` неизвестны (нельзя безопасно редиректить — open-redirect) → JSON/HTML 400.
- **JSON-вариант для mock/тестов:** сохранить (например, по `Accept: application/json`), чтобы offline-тесты [EID-01](../STORY-IDS-EID-01-eid-verification-flow/STORY-IDS-EID-01-eid-verification-flow.md) не ломались.
- **Динамический роут (F6):** заменить три захардкоженных callback-роута ([`asgi_app.py:214-248`](../../../../../../src/core/api/asgi_app.py)) на один `GET /auth/{provider}/callback`; хендлер резолвит `provider` из пути, проверяет регистрацию в реестре (иначе `ConfigError`), делегирует в оркестратор.
- **Док (F11):** в [06-eid-providers](../../../../../runtime-docs/06-eid-providers.md)/[08-ui-expectations](../../../../../runtime-docs/08-ui-expectations.md) зафиксировать web-SPA модель (full-page redirect → callback → 303 back); мобильные user-agent рекомендации — только при появлении RN-клиента (UI = spa-app, не React Native).

## Вне scope
- Сами коды ошибок — [EID-05](../STORY-IDS-EID-05-canonical-provider-contract/STORY-IDS-EID-05-canonical-provider-contract.md).
- Реальный провайдер, который этот redirect инициирует — [EID-02](../../../../backlog-stories/STORY-IDS-EID-02-real-eid-providers.md).

## Точки в коде (реализовано)
- `EidCallbackOutcome` + JSON builder: [`eid_callback.py`](../../../../../../src/core/api/eid_callback.py).
- Оркестратор возвращает outcome: [`handlers.py:191-375`](../../../../../../src/core/api/handlers.py).
- Динамический роут + redirect render: [`asgi_app.py`](../../../../../../src/core/api/asgi_app.py) (`GET /auth/{provider}/callback`, `_render_eid_callback_outcome`).
- Allowlist return_url на старте: [`handlers.py:124-141`](../../../../../../src/core/api/handlers.py), [`return_url.py`](../../../../../../src/core/security/return_url.py).
- Offline tests: [`test_eid_callback_redirect.py`](../../../../../../tests/test_eid_callback_redirect.py).

## Acceptance Criteria
- [x] `handle_auth_eid_callback` возвращает `EidCallbackOutcome` (домен-исход), без привязки к одному представлению.
- [x] Успешный callback в браузере → `303` на `return_url` с `?eid_status=verified`; ошибка → `?eid_status=error&eid_error=<код>`.
- [x] Неизвестная сессия/return_url → безопасный 400 (без редиректа на неизвестный origin).
- [x] Один параметризованный роут `/auth/{provider}/callback`; добавление провайдера не требует нового роута; незарегистрированный `provider` → `ConfigError`.
- [x] Mock-флоу [EID-01](../STORY-IDS-EID-01-eid-verification-flow/STORY-IDS-EID-01-eid-verification-flow.md) продолжает проходить (JSON-вариант для тестов сохранён).
- [x] Доки отражают SPA-first redirect-модель. Offline-набор зелёный.

## Парадигма-якорь
[08-ui-expectations](../../../../../runtime-docs/08-ui-expectations.md) (return_url, SPA), [01-api](../../../../../runtime-docs/01-api.md) (контракты эндпоинтов), [06-eid-providers](../../../../../runtime-docs/06-eid-providers.md).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-09-06-t01-eid-callback-outcome-dataclass`](./task-ids-09-06-t01-eid-callback-outcome-dataclass/README.md) | pkg-000019 |
| 2 | [`task-ids-09-06-t02-dynamic-callback-route-registry-guard`](./task-ids-09-06-t02-dynamic-callback-route-registry-guard/README.md) | pkg-000019 |
| 3 | [`task-ids-09-06-t03-callback-redirect-render-accept-negotiate`](./task-ids-09-06-t03-callback-redirect-render-accept-negotiate/README.md) | pkg-000019 |
| 4 | [`task-ids-09-06-t04-offline-redirect-and-json-regression-tests`](./task-ids-09-06-t04-offline-redirect-and-json-regression-tests/README.md) | pkg-000019 |
| 5 | [`task-ids-09-06-t05-spa-first-runtime-docs`](./task-ids-09-06-t05-spa-first-runtime-docs/README.md) | pkg-000019 |
| 6 | [`task-ids-09-06-t06-story-acceptance-verification`](./task-ids-09-06-t06-story-acceptance-verification/README.md) | pkg-000019 |
| 7 | [`task-ids-09-06-t07-audit-f1-backlog-story-status-sync`](./task-ids-09-06-t07-audit-f1-backlog-story-status-sync/README.md) | override epic_ids_09_eid_06_audit_2026_06_08 |
