# 08. Что identity ждёт от UI (spa-app)

## О чём этот документ

В этом репозитории **нет кода интерфейса** — identity отдаёт только HTTP API. Но чтобы всё работало, веб-приложение (spa-app) должно вести себя определённым образом: ходить с разрешённого адреса, присылать токен, правильно возвращать пользователя после проверки. Здесь собрано, **что именно identity ожидает/проверяет со стороны UI** — по фактам конфига и кода, а не по фантазиям.

Контекст: UI — это **spa-app (React/Vite)**, основной интерфейс. Сам он к Supabase напрямую не подключён (проверено в [separation-audit](../analysis/supabase-project-separation-audit-2026-06-03.md)); вход делает через Supabase Auth и работает с identity по токену.

## Контракт «identity ← UI» по пунктам

### 1. Ходить с разрешённого адреса (CORS)
Браузер пускает запросы только с origin'ов из `CORS_ALLOWED_ORIGINS` ([`asgi_app.py:75-80`](../../src/core/api/asgi_app.py), пример в [`.env.example:85-86`](../../.env.example)). В проде это конкретные домены (например `https://dogestonia.ee`), не `*`. Если UI на другом адресе — браузер заблокирует. ✅ применяется.

### 2. Прислать токен пользователя
UI логинит человека через **Supabase Auth** (email/пароль или magic link) и в каждый защищённый запрос кладёт `Authorization: Bearer <supabase_jwt>`. identity сам логин не делает — только проверяет токен ([04-security](04-security.md)). ✅ проверяется.

### 3. Сказать, куда вернуть после eID
UI передаёт `return_url` (и опционально `return_context`) в `POST /auth/eid/start`. Identity проверяет URL по белому списку `ALLOWED_RETURN_URLS` ([`handlers.py:124-141`](../../src/core/api/handlers.py), [`return_url.py`](../../src/core/security/return_url.py)) и сохраняет в сессии. После callback identity редиректит браузер **303** на этот URL с query-маркерами `eid_status` / `eid_error` ([`eid_callback.py`](../../src/core/api/eid_callback.py)). ✅ применяется.

### 4. SPA-first redirect-модель
Типичный web-флоу (spa-app, не React Native):

1. SPA → `POST /auth/eid/start` (Bearer JWT + `return_url` на страницу возврата в SPA).
2. Full-page redirect пользователя к eID-провайдеру (redirect URL из ответа start).
3. Провайдер → `GET /auth/{provider}/callback` на identity.
4. Identity → **303** обратно в SPA на `return_url?eid_status=verified` или `?eid_status=error&eid_error=<код>`.
5. SPA читает query-параметры и показывает результат.

Мобильные user-agent рекомендации — только при появлении RN-клиента; сейчас UI = spa-app.

### 5. Дать страницу верификации/авторизации
В сценарии из [04-security](04-security.md) UI показывает страницу входа (с флагом «нужен eID») и страницу/экран, куда возвращается пользователь после проверки. Этот экран — на стороне UI; identity лишь редиректит и принимает callback. ❌ конкретный URL экрана в коде identity не зашит — это ожидание к UI.

## Сводка

| Что ждём от UI | Чем проверяется в identity | Статус |
|----------------|----------------------------|--------|
| Запросы с разрешённого origin | `CORS_ALLOWED_ORIGINS` | ✅ |
| Bearer Supabase JWT в запросах | `get_current_user` | ✅ |
| `return_url`/`return_context` при старте eID | поля сессии + `validate_return_url` на start | ✅ |
| Белый список возвратных URL | `ALLOWED_RETURN_URLS` + redirect только на сохранённый URL | ✅ |
| SPA-first callback → 303 back | `eid_status` / `eid_error` query markers | ✅ |
| Экран входа/верификации | — | ❌ ответственность UI |

## Главное
Всё «ожидаемое от UI» — это **контракт**, а не код в этом репозитории. SPA-first redirect-модель (start → provider → callback → 303 back) зафиксирована в [`06-eid-providers`](06-eid-providers.md) и [`eid_callback.py`](../../src/core/api/eid_callback.py).
