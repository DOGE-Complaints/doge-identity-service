# 01. HTTP API

## О чём этот документ

Сервис общается с внешним миром по HTTP. Здесь — честный список того, **какие двери (маршруты) у сервиса есть**, кто в них может войти и что за ними сейчас реально происходит. Это рукописный «контракт», потому что отдельного OpenAPI-файла в репозитории нет — FastAPI отдаёт авто-документацию по адресу `/docs` только когда сервис запущен.

Источник истины: [`asgi_app.py`](../../src/core/api/asgi_app.py), [`handlers.py`](../../src/core/api/handlers.py), [`envelope.py`](../../src/core/api/envelope.py), [`security.py`](../../src/core/api/security.py).

## Как выглядит любой ответ (envelope)

Чтобы клиентам было предсказуемо, **все** ответы завёрнуты в единый «конверт» ([`envelope.py:6-20`](../../src/core/api/envelope.py)):

- успех: `{"data": { ... }}`
- ошибка: `{"error": {"code": "...", "message": "...", "trace_id": "..."}}`

`trace_id` — это сквозной идентификатор запроса для трассировки в логах: берётся из заголовка `x-trace-id`, а если его нет — генерируется ([`envelope.py:23-26`](../../src/core/api/envelope.py)). Коды ошибок: `AUTHENTICATION_REQUIRED` (нет/битый токен, 401), `NOT_IMPLEMENTED` (ещё заглушка, 501), `CONFIG_ERROR` (500), `INTERNAL_ERROR` (500).

## Маршруты, относящиеся к identity

| Метод | Путь | Кто может войти | Что сейчас | Где в коде |
|-------|------|------------------|------------|-----------|
| GET | `/health` | все | ✅ `{status: ok}` — «я жив» | [`asgi_app.py:145-150`](../../src/core/api/asgi_app.py) |
| GET | `/ready` | все | ✅ «готов ли к работе» + статус БД | [`asgi_app.py:152-157`](../../src/core/api/asgi_app.py) |
| GET | `/me` | по Supabase JWT | ✅ 200 — профиль + `eid_verified` + `role` (базовые права = JWT role, без RBAC) | [`asgi_app.py`](../../src/core/api/asgi_app.py), [`me_response.py`](../../src/core/api/me_response.py) |
| POST | `/auth/eid/start` | по Supabase JWT | 🟡 501 (старт eID-проверки) | [`asgi_app.py:171-181`](../../src/core/api/asgi_app.py) |
| GET | `/auth/eideasy/callback` | внешний редирект | 🟡 501 (возврат от eID Easy) | [`asgi_app.py:183-193`](../../src/core/api/asgi_app.py) |
| GET | `/auth/authentigate/callback` | внешний редирект | 🟡 501 (возврат от Authentigate) | [`asgi_app.py:195-205`](../../src/core/api/asgi_app.py) |
| GET | `/auth/mock/callback` | внешний редирект | 🟡 501 (возврат от mock-провайдера) | [`asgi_app.py:207-217`](../../src/core/api/asgi_app.py) |
| GET | `/oauth/authorize` | по Supabase JWT | 🟡 501 (старт OAuth для GPT) | [`asgi_app.py:219-230`](../../src/core/api/asgi_app.py) |
| POST | `/oauth/authorize/complete` | по Supabase JWT | 🟡 501 (подтверждение авторизации) | [`asgi_app.py:232-243`](../../src/core/api/asgi_app.py) |
| POST | `/oauth/token` | по Supabase JWT | 🟡 501 (обмен кода на токен) | [`asgi_app.py:245-256`](../../src/core/api/asgi_app.py) |
| OPTIONS | защищённые пути | все | ✅ 200 (CORS preflight) | [`asgi_app.py:26-36,312-322`](../../src/core/api/asgi_app.py) |

**Коротко:** рабочие маршруты — `/health`, `/ready`, **`GET /me`** (профиль + `eid_verified`). Остальное — каркас с заглушками `501`, под который уже готова инфраструктура (валидация токена, DI, контракты).

> Story-маршруты (`/story-drafts`, `/stories`, `/gpt/actions/submit-story`) **удалены** из identity в EPIC-IDS-08 CLEANUP-01; создание историй — домен gateway ([09-gateway-expectations](09-gateway-expectations.md)).

> ⚠️ Чего здесь не хватает под целевую модель (см. [04-security](04-security.md), [09-gateway-expectations](09-gateway-expectations.md)): **нет** маршрута `/oauth/introspect` для service-token сценария; **`GET /me`** уже отдаёт профиль и `eid_verified` по user JWT (базовые права — поле `role` из токена, без permission-матрицы).

## Кто пускается внутрь (аутентификация)

Защищённые маршруты используют зависимость `get_current_user` ([`security.py:65-70`](../../src/core/api/security.py)), которая проверяет заголовок `Authorization: Bearer <токен>`. Рабочий проверяющий — `SupabaseJwtBearerTokenAuth` ([`security.py:34-45`](../../src/core/api/security.py)). Нет токена или он битый → 401 `AUTHENTICATION_REQUIRED`. Подробно про токены — в [04-security](04-security.md).

## Что ещё есть под капотом

- **CORS** ([`asgi_app.py:75-80`](../../src/core/api/asgi_app.py)) — разрешённые origin'ы берутся из `CORS_ALLOWED_ORIGINS`; методы GET/POST/OPTIONS.
- **Перехват ошибок** ([`asgi_app.py:123-141`](../../src/core/api/asgi_app.py)) — любое необработанное исключение превращается в аккуратный `500 INTERNAL_ERROR` с `trace_id`, сервис не «падает голым стеком».
- **Idempotency-key** — резолвер удалён в EPIC-IDS-08 CLEANUP-02 (owner decision E21); idempotency для POST-маршрутов — в функциональных эпиках, когда появятся потребители.
