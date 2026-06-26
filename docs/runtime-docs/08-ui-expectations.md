# 08. Что identity ждёт от UI (spa-app)

## О чём этот документ

В этом репозитории **нет кода интерфейса** — identity отдаёт только HTTP API. Но чтобы всё работало, веб-приложение (spa-app) должно вести себя определённым образом: ходить с разрешённого адреса, присылать токен, правильно возвращать пользователя после проверки. Здесь собрано, **что именно identity ожидает/проверяет со стороны UI** — по фактам конфига и кода, а не по фантазиям.

Контекст: UI — это **spa-app (React/Vite)**, основной интерфейс. Сам он к Supabase напрямую не подключён (проверено в [separation-audit](../analysis/supabase-project-separation-audit-2026-06-03.md)); вход делает через Supabase Auth и работает с identity по токену.

## Контракт «identity ← UI» по пунктам

### 1. Ходить с разрешённого адреса (CORS)
Браузер пускает запросы только с origin'ов из `CORS_ALLOWED_ORIGINS` ([`asgi_app.py:75-80`](../../src/core/api/asgi_app.py), пример в [`.env.example:85-86`](../../.env.example)). В проде это конкретные домены (например `https://dogestonia.ee`), не `*`. Если UI на другом адресе — браузер заблокирует. ✅ применяется.

### 2. Прислать токен пользователя
UI логинит человека через **Supabase Auth** (email/пароль или magic link) и в каждый защищённый запрос кладёт `Authorization: Bearer <supabase_jwt>`. identity сам логин не делает — только проверяет токен ([04-security](04-security.md)). ✅ проверяется.

### 3. Активная inline-верификация телефона (без внешнего redirect)
Активный механизм проверки «реальный уникальный человек» — **телефон по SMS-OTP**, гейт `phone_verified` (eID отложен). Внешнего redirect здесь **нет** — SPA делает два API-вызова прямо из кабинета:

1. SPA → `POST /auth/phone/request` (Bearer JWT + `{phone}`) → identity шлёт SMS-OTP, отвечает `{data:{sent,expires_at}}`.
2. Пользователь вводит код в форме SPA (inline), SPA → `POST /auth/phone/confirm` (`{phone,code}`) → `{data:{status:"verified"}}`.
3. После успеха `phone_verified=true` в профиле (`GET /me`); никаких 303-редиректов и `return_url`.

Ограничения и ошибки (см. [04-security](04-security.md) и [19-phone-verification-flow](../requirements/19-phone-verification-flow.md)): только эстонские номера **+372**; один номер = один аккаунт (конфликт → `409 profile_conflict`); иностранный номер → `COUNTRY_NOT_ALLOWED`. ✅ применяется.

### 3b. Ленивый гейт: verify-экран по защищённому действию

> **Источник:** [DOC-IDS-ONB-01](../tasks/backlog-stories/identity-onboarding/DOC-IDS-ONB-01-lazy-phone-gate-contract.md) · [`09-gateway-expectations`](09-gateway-expectations.md) §«Ленивый гейт телефона».

При **web signup** телефон **не** обязателен сразу после регистрации. SPA **не** показывает verify-экран «на всякий случай» — только когда пользователь инициирует **защищённое действие**, требующее подтверждённый телефон.

**Ожидание к spa-app:**

1. Перед защищённым действием (напр. «создать/опубликовать стори») SPA вызывает `GET /me` и читает `phone_verified` ([`me_response.py:42`](../../src/core/api/me_response.py)).
2. Если `phone_verified === false` → **не** вызывать backend действия; показать **verify-экран** (inline, без внешнего redirect).
3. На verify-экране — PV-05: `POST /auth/phone/request` → пользователь вводит OTP → `POST /auth/phone/confirm` (см. §3 выше).
4. После `{data:{status:"verified"}}` и `phone_verified=true` в `/me` → вернуть пользователя к прерванному действию и выполнить его.

**Sequence (словами):** регистрация/email-only → обычное использование UI → защищённое действие → `phone_verified=false` → verify-экран → успех → действие разрешено.

**SSOT:** [STORY-IDS-PV-05](../tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-05-verification-flow-api/STORY-IDS-PV-05-verification-flow-api.md) · [onboarding-phone-verification-api.md](../runbook/onboarding-phone-verification-api.md) · gateway-side контракт — [`09-gateway-expectations`](09-gateway-expectations.md).

**Enforce на потребителе:** identity не перехватывает «создать стори» — только отдаёт флаг и API verify.

### 3a. ⏸️ deferred (eID): сказать, куда вернуть после eID
> ⏸️ **deferred (eID)** — этот redirect-флоу относится к eID-модели; реальный провайдер отложен (2026-06-10). Активна inline-верификация телефона из пункта 3.

UI передаёт `return_url` (и опционально `return_context`) в `POST /auth/eid/start`. Identity проверяет URL по белому списку `ALLOWED_RETURN_URLS` ([`handlers.py:124-141`](../../src/core/api/handlers.py), [`return_url.py`](../../src/core/security/return_url.py)) и сохраняет в сессии. После callback identity редиректит браузер **303** на этот URL с query-маркерами `eid_status` / `eid_error` ([`eid_callback.py`](../../src/core/api/eid_callback.py)). ⏸️ deferred (eID).

### 4. ⏸️ deferred (eID): SPA-first redirect-модель
> ⏸️ **deferred (eID)** — redirect-модель ниже относится к eID; активный путь — inline-верификация телефона (пункт 3).

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
| Inline phone-verify: `request` → `confirm` (без redirect) | `POST /auth/phone/request` + `POST /auth/phone/confirm`, гейт `phone_verified` | ✅ активно |
| Lazy gate: verify-экран при `phone_verified=false` на защищённом действии | §3b — `GET /me` перед действием | ✅ контракт (spa-app) |
| `return_url`/`return_context` при старте eID | поля сессии + `validate_return_url` на start | ⏸️ deferred (eID) |
| Белый список возвратных URL | `ALLOWED_RETURN_URLS` + redirect только на сохранённый URL | ⏸️ deferred (eID) |
| SPA-first callback → 303 back | `eid_status` / `eid_error` query markers | ⏸️ deferred (eID) |
| Экран входа/верификации | — | ❌ ответственность UI |

## Главное
Всё «ожидаемое от UI» — это **контракт**, а не код в этом репозитории. SPA-first redirect-модель (start → provider → callback → 303 back) зафиксирована в [`06-eid-providers`](06-eid-providers.md) и [`eid_callback.py`](../../src/core/api/eid_callback.py).
