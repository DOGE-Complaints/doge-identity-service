# Жёсткий аудит исполнения STORY-IDS-OAUTH-01 (OAuth 2.0 сервер наружу)

> **Дата:** 2026-06-24
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только проверяемые claims с `file:line`, регрессии, gaps с severity.
> **Предмет:** [`STORY-IDS-OAUTH-01-oauth-server-endpoints`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) vs фактический код. Исполнена под **EPIC-IDS-11-oauth-server** (pkg-000029), 7 tasks.
> **Выбор из** [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md): Текущая волна pkg-000029, STORY-IDS-OAUTH-01 🟢 (стр.11,52,569-575).

## Команды верификации (выполнены)

| Проверка | Результат |
|----------|-----------|
| Роуты подключены (не 501) | `/oauth/authorize` → `handle_oauth_authorize`, `/oauth/authorize/complete` → `handle_oauth_authorize_complete`, `/oauth/token` → `handle_oauth_token` ([asgi_app.py:369-403](../../src/core/api/asgi_app.py)) |
| Хендлеры | новый модуль [`core/oauth/handlers.py`](../../src/core/oauth/handlers.py) (3 функции) |
| authorization_request-store | `AuthorizationRequest` ([models.py:138](../../src/core/domain/models.py)), `AuthorizationRequestStore` Protocol ([contracts.py:122-128](../../src/core/domain/contracts.py)), `InMemoryAuthorizationRequestStore` (save/get/consume + TTL + single-use, [repositories.py:431-450](../../src/core/infrastructure/repositories.py)) |
| client_secret enforcement | `verify_client_secret(...)` против `client.client_secret_hash` → `OAuthClientError("invalid_client")` ([repositories.py issue_access_token](../../src/core/infrastructure/repositories.py), [`core/oauth/client_secret.py`](../../src/core/oauth/client_secret.py)) — **SEC-1 закрыт** |
| RFC 6749 ошибки | `oauth_error_body → {error, error_description}` ([`core/oauth/errors.py`](../../src/core/oauth/errors.py)); `OAuthClientError`→401, `OAuthGrantError`→400 |
| scope-модель | [`core/oauth/scope.py`](../../src/core/oauth/scope.py) (`parse_scope_param`/`validate_requested_scopes`) |
| Приём OAuth-токена эндпоинтами | `get_current_user` «Accept Supabase JWT **or** OAuth access tokens» ([security.py:35,54-57](../../src/core/api/security.py)) |
| Тесты | [test_oauth_server_flow.py](../../tests/test_oauth_server_flow.py) — 11; [test_oauth_authorization_request_store.py](../../tests/test_oauth_authorization_request_store.py) — 2 |
| **Offline-сюита** | **341 passed, 11 deselected** ✅ (совпадает с индексом) |

---

## 1. Актуализация тасков и story (по коду)

Коды: 🟢 Done · 🟡 In Progress · ⚪ Todo. Сверено по коду.

| Таск (EPIC-IDS-11, pkg-000029) | Факт | Статус |
|--------------------------------|------|--------|
| t01 authorization request store + contracts | `AuthorizationRequest` + Protocol + `InMemoryAuthorizationRequestStore` (TTL, single-use consume) | 🟢 |
| t02 rfc6749 errors + scope validation + client_secret | `errors.py` (`{error,error_description}`), `scope.py`, `client_secret.py` (`verify_client_secret`) | 🟢 |
| t03 oauth authorize handler + route | `handle_oauth_authorize`: валидации client/redirect/scope/state/PKCE → save request → 302 spa-login | 🟢 |
| t04 complete + token handlers + routes | `handle_oauth_authorize_complete` (Bearer → consume → code → 302 ChatGPT), `handle_oauth_token` (code→token) | 🟢 |
| t05 oauth access-token bearer dependency | `get_current_user` принимает OAuth-токен ([security.py:54-57](../../src/core/api/security.py)) | 🟢 |
| t06 offline oauth server tests | 13 тестов (flow + store) | 🟢 |
| t07 story acceptance verification | AC 8/8 (см. §2) | 🟢 |
| **STORY-IDS-OAUTH-01** | OAuth-сервер наружу | **🟢 Done** |

Индекс держит эпик корректно: `EPIC-IDS-11 … 🟡 In Progress — OAUTH-01 🟢` ([bullrun-launch-index.md:100](../tasks/bullrun-launch-index.md)); pkg-000029 Done, 341 offline (стр.11).

---

## 2. Сверка Acceptance Criteria story (по коду + тестам)

| AC | Факт (код + тест) | Вердикт |
|----|-------------------|---------|
| `/oauth/authorize` (валид. вход) → code привязан к `supabase_user_id` | complete: `issue_authorization_code(supabase_user_id=current_user…)` ([handlers.py:106-113](../../src/core/oauth/handlers.py)); тест `test_oauth_full_flow_with_pkce` | ✅ |
| `/oauth/token`: code→token; повтор/просрочка → `invalid_grant` | `OAuthGrantError("invalid_grant")` ([handlers.py:151](../../src/core/oauth/handlers.py)); тест `test_oauth_token_rejects_reused_code` | ✅ |
| Неверный `client_secret` → отказ | `verify_client_secret` → `OAuthClientError` 401; тест `test_oauth_token_rejects_wrong_client_secret` | ✅ |
| PKCE: `code_challenge` требует корректный `code_verifier` | движок S256; тесты `..._with_pkce`, `..._pkce_mismatch` | ✅ |
| authorize: `invalid_client`/`invalid_redirect_uri`(прямой)/`invalid_scope`/`state` | [handlers.py:41-62](../../src/core/oauth/handlers.py); тесты `..._invalid_client`, `..._invalid_redirect_uri`, `..._invalid_scope` | ✅ |
| authorization_request-store + handshake (authorize→spa-login `oauth_request_id`→complete→ChatGPT) | save→302 spa-login ([handlers.py:81-83](../../src/core/oauth/handlers.py)); complete→consume→302 `?code&state`; тест `..._happy_path_redirects_to_spa_login` | ✅ |
| Ошибки RFC 6749 + scope-модель | `oauth_error_body` `{error,error_description}`; `scope.py`; тест `test_oauth_rfc_error_shape` | ✅ |
| Offline-набор зелёный | **341 passed** | ✅ |

**Бонус (scope item «приём OAuth-токена»):** `/me` принимает OAuth-access-token — тест `test_me_accepts_oauth_access_token`. ✅

**Вывод:** все 8 AC выполнены и покрыты тестами (13). SEC-1 (`client_secret` не проверялся) — **закрыт**.

---

## 3. Findings (severity + как закрыть; без реализации)

| ID | Severity | Тип | Суть | Где |
|----|----------|-----|------|-----|
| **F1** | MEDIUM | Doc-stale | Backlog-story `Status: ⚪ Todo` (стр.6) + AC `[ ]` (стр.33-40) + секция «Точки в коде» описывает пред-состояние («Маршруты-заглушки → `handle_bearer_stub` → 501», «`client_secret` не проверяется», «`authorization_request`-стора пока нет», номера `asgi_app.py:219-256`/`repositories.py:238-346`) — реально 🟢 Done под pkg-000029, роуты подключены, SEC-1 закрыт, стор есть. **Как закрыть:** Status ⚪→🟢, AC `[ ]`→`[x]`, обновить «Точки в коде» (модуль `core/oauth/`, `InMemoryAuthorizationRequestStore`, `verify_client_secret`). Рекуррентный паттерн. | [`STORY-IDS-OAUTH-01...md:6,26-30,33-40`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) |
| **F2** | MEDIUM | Doc-stale (свежий drift) | Локальный пакет-индекс `oauth/EPIC-IDS-OAUTH.md`: строка статуса «код OAUTH-01..04 — **⚪ Todo** (роуты `/oauth/*` = 501)», состав OAUTH-01 = ⚪ Todo, «Назначение: сейчас роуты `/oauth/*` — заглушки 501» — устарело (OAUTH-01 🟢, роуты подключены). **Как закрыть:** OAUTH-01 → 🟢 в составе; снять «501» из статус-строки/назначения. | [`oauth/EPIC-IDS-OAUTH.md`](../tasks/backlog-stories/oauth/EPIC-IDS-OAUTH.md) |
| **F3** | MEDIUM | Cross-doc consistency (свежий drift) | Флоу-доки и соседние стори, **обновлённые 2026-06-24**, ещё держат «OAuth = 501» как факт: [`04-security §A`](../runtime-docs/04-security.md) (as-is врезка «OAuth-роуты `/oauth/*` = 501» + таблица «OAuth-маршруты 🟡 501»), [`09-gateway-expectations`](../runtime-docs/09-gateway-expectations.md) (зависимость от OAuth), [`OAUTH-02`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md)/[`OAUTH-03`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md)/[`OAUTH-04`](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) («роуты 501»). После реализации OAUTH-01 эти «501» неверны. **Как закрыть:** заменить «501» → «✅ построен (OAUTH-01)» в as-is/таблицах; зависимости OAUTH-02/03/04 от «501» снять. | runtime-docs + oauth-стори |

Иных материальных findings нет. Наблюдения (severity none, **не gap OAUTH-01**):
- **`InMemoryOAuthTokenService` + `InMemoryAuthorizationRequestStore` — in-memory** (codes/handshake теряются на редеплое). **Вне scope OAUTH-01** — это [OAUTH-03](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) (durable Supabase-стор). Access-токен — stateless HS256 (переживает редеплой).
- **introspection-endpoint** для gateway — **вне scope OAUTH-01** ([OAUTH-02](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md)).
- Новые модули `core/oauth/` (`handlers/errors/scope/client_secret/spa_login`) — чистая декомпозиция, не в `handlers.py` (изоляция OAuth-логики).

---

## 4. Регрессионная проверка

| Аспект | Результат |
|--------|-----------|
| Offline-сюита | **341 passed, 11 deselected** (совпадает с индексом «341 pytest offline»), **ожидаемо** |
| Новый пакет `core/oauth/` | аддитивный; phone/eID/`/me` не затронуты |
| `get_current_user` | расширен на OAuth-токены — Supabase-JWT путь сохранён (тесты `/me` зелёные) |
| OAuth-роуты | были 501 (`handle_bearer_stub`) → реальные хендлеры; `handle_bearer_stub` остаётся в коде ([handlers.py:732](../../src/core/api/handlers.py)) — больше не на oauth-роутах (наблюдение, не регресс) |
| eID/phone/OAuth-движок | без изменений поведения — сюита зелёная |

Регрессий не выявлено.

---

## 5. Итог

- **STORY-IDS-OAUTH-01 — 🟢 исполнена полно:** `/oauth/authorize` (валидации client/redirect/scope/state/PKCE → `AuthorizationRequest`-store → 302 spa-login), `/oauth/authorize/complete` (Bearer → consume → code → 302 ChatGPT), `/oauth/token` (code→access-token, `client_secret` enforced, `invalid_grant`/`invalid_client`), RFC 6749-ошибки, scope-модель, приём OAuth-токена `/me`. AC 8/8, 13 тестов. SEC-1 закрыт.
- **Findings:** **F1 (MEDIUM)** — backlog-story doc-stale (⚪→🟢); **F2 (MEDIUM)** — пакет-индекс `EPIC-IDS-OAUTH.md` держит «501/⚪»; **F3 (MEDIUM)** — флоу-доки/соседние стори (`04-security`/`09`/OAUTH-02/03/04), обновлённые в тот же день, ещё пишут «OAuth 501» (свежий drift после билда).
- Наблюдения (in-memory стор → OAUTH-03; introspection → OAUTH-02) — по scope, не gaps.

## Quality gate (analysis.mdc)
- [x] Все claims с `file:line`; 7 тасков + story сверены по коду (pipeline-таски t01–t07 🟢, индекс корректен).
- [x] AC 8/8 сверены по коду **и** тестам; PKCE/invalid_grant/client_secret/RFC-shape/token-acceptance подтверждены отдельными тестами.
- [x] SEC-1 (`client_secret`) проверен закрытым (`verify_client_secret` → 401).
- [x] Регрессий нет; 341 offline совпал с индексом; in-memory/introspection отнесены к OAUTH-03/02 (не gaps OAUTH-01).
- [x] Свежий doc-drift «OAuth 501» в обновлённых 2026-06-24 доках пойман (F3) — рекомендация синхронизировать.
