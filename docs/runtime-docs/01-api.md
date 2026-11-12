# 01. HTTP API

> Актуализировано 2026-09-21 (REQ21 / EPIC-IDS-15: `identity_verified` на `/me`). Ранее: 2026-08-21 (SMSPM webhook); 2026-06-24.

## О чём этот документ

Сервис общается с внешним миром по HTTP. Здесь — честный список того, **какие двери (маршруты) у сервиса есть**, кто в них может войти и что за ними сейчас реально происходит. Рукописный контракт + machine-readable [`api-reference/openapi.yaml`](api-reference/openapi.yaml). FastAPI отдаёт `/docs` только когда сервис запущен.

Источник истины: [`asgi_app.py`](../../src/core/api/asgi_app.py), [`handlers.py`](../../src/core/api/handlers.py), [`envelope.py`](../../src/core/api/envelope.py), [`security.py`](../../src/core/api/security.py).

## Как выглядит любой ответ (envelope)

Чтобы клиентам было предсказуемо, **все** ответы завёрнуты в единый «конверт» ([`envelope.py:6-20`](../../src/core/api/envelope.py)):

- успех: `{"data": { ... }}`
- ошибка: `{"error": {"code": "...", "message": "...", "trace_id": "..."}}`

`trace_id` — это сквозной идентификатор запроса для трассировки в логах: берётся из заголовка `x-trace-id`, а если его нет — генерируется ([`envelope.py:23-26`](../../src/core/api/envelope.py)). Коды ошибок: `AUTHENTICATION_REQUIRED` (нет/битый токен, 401), `NOT_IMPLEMENTED` (ещё заглушка, 501), `CONFIG_ERROR` (500), `INTERNAL_ERROR` (500).

## Маршруты, относящиеся к identity

| Метод | Путь | Кто может войти | Что сейчас | Где в коде |
|-------|------|------------------|------------|-----------|
| GET | `/health` | все | ✅ `{status: ok}` — «я жив» | [`asgi_app.py:288-293`](../../src/core/api/asgi_app.py) |
| GET | `/ready` | все | ✅ «готов ли к работе» + статус БД | [`asgi_app.py:295-300`](../../src/core/api/asgi_app.py) |
| GET | `/me` | по Supabase JWT | ✅ 200 — профиль + method-opaque **`identity_verified`** (REQ21) + legacy `phone_verified`/`eid_verified` + `role` | [`asgi_app.py:302-312`](../../src/core/api/asgi_app.py), [`me_response.py`](../../src/core/api/me_response.py) |
| POST | `/auth/eid/start` | по Supabase JWT | ⏸️ старт eID-проверки (сессия + redirect URL); реальный провайдер DEFERRED | [`asgi_app.py:314-332`](../../src/core/api/asgi_app.py), [`handlers.py`](../../src/core/api/handlers.py) |
| GET | `/auth/{provider}/callback` | внешний редирект | ✅ mock работает; браузер → 303 на `return_url`; `Accept: application/json` → JSON | [`asgi_app.py:334-358`](../../src/core/api/asgi_app.py), [`eid_callback.py`](../../src/core/api/eid_callback.py) |
| POST | `/auth/phone/request` | по Supabase JWT | ✅ запрос SMS-OTP `{phone}` → `{data:{sent,expires_at}}` (PV-01) | [`asgi_app.py:360-376`](../../src/core/api/asgi_app.py), [`handlers.py`](../../src/core/api/handlers.py) |
| POST | `/auth/phone/confirm` | по Supabase JWT | ✅ подтверждение `{phone,code}` → `{data:{status:"verified"}}` (PV-01) | [`asgi_app.py:378-394`](../../src/core/api/asgi_app.py), [`handlers.py`](../../src/core/api/handlers.py) |
| POST | `/webhooks/telnyx/messaging` | провайдер (Ed25519) | ✅ delivery-статусы Telnyx (PV-07) | [`asgi_app.py:396-409`](../../src/core/api/asgi_app.py), [`handlers.py`](../../src/core/api/handlers.py) |
| GET | `/webhooks/smspm/delivery/{shared_secret}` | провайдер (path-secret) | ✅ delivery-статусы SMSPM; тело `OK`; на confirm не влияет | [`asgi_app.py:411-423`](../../src/core/api/asgi_app.py), [`handlers.py:759-837`](../../src/core/api/handlers.py) |
| GET | `/oauth/authorize` | публичный (старт OAuth для GPT) | ✅ построен (OAUTH-01) | [`asgi_app.py:425-435`](../../src/core/api/asgi_app.py), [`oauth/handlers.py`](../../src/core/oauth/handlers.py) |
| POST | `/oauth/authorize/complete` | по Supabase JWT | ✅ построен — подтверждение авторизации (OAUTH-02) | [`asgi_app.py:437-452`](../../src/core/api/asgi_app.py), [`oauth/handlers.py`](../../src/core/oauth/handlers.py) |
| POST | `/oauth/token` | OAuth client (form) | ✅ построен — обмен кода на токен (OAUTH-04) | [`asgi_app.py:454-460`](../../src/core/api/asgi_app.py), [`oauth/handlers.py`](../../src/core/oauth/handlers.py) |
| POST | `/oauth/introspect` | service-token | ✅ построен — `{active, sub, phone_verified}` (OAUTH-02) | [`asgi_app.py:462-471`](../../src/core/api/asgi_app.py), [`oauth/introspection.py`](../../src/core/oauth/introspection.py) |
| OPTIONS | защищённые пути | все | ✅ 200 (CORS preflight) | [`asgi_app.py:204-209`](../../src/core/api/asgi_app.py) (CORS), [`asgi_app.py:473-479`](../../src/core/api/asgi_app.py) (OPTIONS) |

**Коротко:** рабочие маршруты — `/health`, `/ready`, **`GET /me`** (consumer flag **`identity_verified`** для gateway/threads/spa REQ7; legacy method flags coexist), **`POST /auth/phone/request`** + **`POST /auth/phone/confirm`** (активный *метод* верификации; ставит `phone_verified` + opaque), **`GET /auth/{provider}/callback`** (mock), **`POST /webhooks/telnyx/messaging`**, **`GET /webhooks/smspm/delivery/{shared_secret}`**, и весь OAuth-набор — ✅ построен (OAUTH-01/02/04). **`POST /auth/eid/start`** — каркас, реальный eID-провайдер ⏸️ deferred. SMS — [11-sms-providers](11-sms-providers.md). Канон `/me`: [API_REFERENCE §6](api-reference/API_REFERENCE.md).

> Story-маршруты (`/story-drafts`, `/stories`, `/gpt/actions/submit-story`) **удалены** из identity в EPIC-IDS-08 CLEANUP-01; создание историй — домен gateway ([09-gateway-expectations](09-gateway-expectations.md)).

> **`POST /oauth/introspect`** — ✅ построен (OAUTH-02, service-token gate + `{active, sub, phone_verified}` — **legacy GPT path**); **`GET /me`** отдаёт **`identity_verified`** (REQ7 consumer canon) плюс legacy method flags по user JWT.

## Кто пускается внутрь (аутентификация)

Защищённые маршруты используют зависимость `get_current_user` ([`security.py:65-70`](../../src/core/api/security.py)), которая проверяет заголовок `Authorization: Bearer <токен>`. Рабочий проверяющий — `SupabaseJwtBearerTokenAuth` ([`security.py:34-45`](../../src/core/api/security.py)). Нет токена или он битый → 401 `AUTHENTICATION_REQUIRED`. Подробно про токены — в [04-security](04-security.md).

## Что ещё есть под капотом

- **CORS** ([`asgi_app.py:204-209`](../../src/core/api/asgi_app.py)) — разрешённые origin'ы берутся из `CORS_ALLOWED_ORIGINS`; методы GET/POST/OPTIONS.
- **Перехват ошибок** ([`asgi_app.py:123-141`](../../src/core/api/asgi_app.py)) — любое необработанное исключение превращается в аккуратный `500 INTERNAL_ERROR` с `trace_id`, сервис не «падает голым стеком».
- **Idempotency-key** — резолвер удалён в EPIC-IDS-08 CLEANUP-02 (owner decision E21); idempotency для POST-маршрутов — в функциональных эпиках, когда появятся потребители.
