# 08. Что identity ждёт от UI (spa-app)

## О чём этот документ

В этом репозитории **нет кода интерфейса** — identity отдаёт только HTTP API. Но чтобы всё работало, веб-приложение (spa-app) должно вести себя определённым образом: ходить с разрешённого адреса, присылать токен, правильно возвращать пользователя после проверки. Здесь собрано, **что именно identity ожидает/проверяет со стороны UI** — по фактам конфига и кода, а не по фантазиям.

Контекст: UI — это **spa-app (React/Vite)**, основной интерфейс. Сам он к Supabase напрямую не подключён (проверено в [separation-audit](../analysis/supabase-project-separation-audit-2026-06-03.md)); вход делает через Supabase Auth и работает с identity по токену.

## Контракт «identity ← UI» по пунктам

### 1. Ходить с разрешённого адреса (CORS)
Браузер пускает запросы только с origin'ов из `CORS_ALLOWED_ORIGINS` ([`asgi_app.py:203-208`](../../src/core/api/asgi_app.py), runbook [`cors-allowed-origins.md`](../runbook/cors-allowed-origins.md)). В проде это конкретные домены (например публичный URL spa на Railway), не `*`. Если UI на другом адресе — браузер заблокирует. ✅ применяется.

### 2. Прислать токен пользователя
UI логинит человека через **Supabase Auth** (email/пароль или magic link) и в каждый защищённый запрос кладёт `Authorization: Bearer <supabase_jwt>`. identity сам логин не делает — только проверяет токен ([04-security](04-security.md)). ✅ проверяется.

### 3. Активная inline-верификация телефона (без внешнего redirect)
Активный механизм проверки «реальный уникальный человек» — **телефон по SMS-OTP**, гейт `phone_verified` (eID отложен). Внешнего redirect здесь **нет** — SPA делает два API-вызова прямо из кабинета:

1. SPA → `POST /auth/phone/request` (Bearer JWT + `{phone}`) → identity шлёт SMS-OTP, отвечает `{data:{sent,expires_at}}`.
2. Пользователь вводит код в форме SPA (inline), SPA → `POST /auth/phone/confirm` (`{phone,code}`) → `{data:{status:"verified"}}`.
3. После успеха `phone_verified=true` в профиле (`GET /me`); никаких 303-редиректов и `return_url`.

Ограничения и ошибки (см. [04-security](04-security.md) и [19-phone-verification-flow](../requirements/19-phone-verification-flow.md)): только эстонские номера **+372**; один номер = один аккаунт (конфликт → `409 profile_conflict`); иностранный номер → `COUNTRY_NOT_ALLOWED` (waitlist-механизм — [`onboarding-waitlist.md`](../runbook/onboarding-waitlist.md)). ✅ применяется.

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

**Disclosure + boundary copy (EN SSOT):** на verify-экране (перед вводом номера) и для `COUNTRY_NOT_ALLOWED` / 409 `profile_conflict` — [`onboarding-copy.md`](../runbook/onboarding-copy.md) ([DOC-IDS-ONB-02](../tasks/backlog-stories/identity-onboarding/DOC-IDS-ONB-02-disclosure-copy.md)). Рендер — spa-app; канон текста — identity runbook.

**Enforce на потребителе:** identity не перехватывает «создать стори» — только отдаёт флаг и API verify.

### 3c. GPT verify landing: web-страница `/verify` + возврат в GPT

> **Источник:** [DOC-IDS-ONB-03](../tasks/backlog-stories/identity-onboarding/DOC-IDS-ONB-03-gpt-verify-landing-contract.md) · UX вход #2 — [`identity-onboarding-ux-2026-06-12.md`](../analysis/identity-onboarding-ux-2026-06-12.md) §2–3.  
> **OAuth as-built:** [OAUTH-01](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md)…[OAUTH-04](../tasks/backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) — **Done** (не 501). Премиса «OAuth = блокер end-to-end» устарела.

В GPT-ветке номер и OTP вводятся **только на нашем web** (не в чате). Identity отдаёт URL verify-экрана и замыкает возврат через OAuth callback; рендер страницы — spa-app.

**Sequence (словами):**

1. GPT инициирует вход/защищённое действие → `GET /oauth/authorize` (с `requested_action`, опц. `return_context`).
2. Identity → **302** на spa [`build_spa_oauth_login_url`](../../src/core/oauth/spa_login.py): `{spa}/login?oauth_request_id=…`.
3. Пользователь логинится (Supabase Auth); spa держит `oauth_request_id` для complete.
4. Spa → `POST /oauth/authorize/complete` (Bearer + `oauth_request_id`).
5. Если `requested_action` требует телефон и `phone_verified=false` → **HTTP 403** flat body [`verification_required`](../../src/core/oauth/verification_required.py): `{ "error": "verification_required", "reason": "…", "verify_url": "…" }` ([`09-gateway-expectations`](09-gateway-expectations.md) §контракт).
6. `verify_url` строится [`build_spa_verify_url`](../../src/core/oauth/spa_login.py): `{spa}/verify` или `{spa}/verify?context=<return_context>` (query-имя **`context`** = OAuth `return_context`; identity **не** фиксирует enum значений — напр. spa GPT-bridge может передать `custom_gpt`).
7. На `/verify`: disclosure ([`onboarding-copy.md`](../runbook/onboarding-copy.md)) → PV-05 `POST /auth/phone/request` → OTP → `POST /auth/phone/confirm`.
8. После успеха spa снова → `POST /oauth/authorize/complete` → identity **302** на GPT `redirect_uri?code=…&state=…` (связка GPT↔Supabase user замыкается здесь). Spa следует Location в браузере.

**Контракт входа (что страница принимает):**

| Вход | Источник | Ожидание к UI |
|------|----------|---------------|
| Path `/verify` | `verify_url` из 403 | Открыть verify-экран (не chat) |
| Query `context` (опц.) | `return_context` → `build_spa_verify_url` | Сохранить/использовать как GPT-bridge маркер при необходимости |
| Bearer Supabase JWT | login-шаг | Сессия обязательна для phone API и complete |
| `oauth_request_id` | login URL / session | Нужен для повторного `authorize/complete` после verify |

**Контракт выхода / возврат:**

| Исход | Поведение UI |
|-------|----------------|
| Успех, GPT-ветка (есть `oauth_request_id`) | `POST /oauth/authorize/complete` → follow **302** Location на GPT callback |
| Успех, non-GPT | Как §3b — вернуть к прерванному UI-действию |
| `COUNTRY_NOT_ALLOWED` / 409 `profile_conflict` | Boundary copy из [`onboarding-copy.md`](../runbook/onboarding-copy.md) |
| Повторный 403 `verification_required` | Остаться на verify (не уводить в GPT) |

**Browser-submit (смежный путь):** gateway `POST /story-drafts/{id}/submit` при `phone_verified=false` отдаёт **тот же** shape `verification_required` + `verify_url` ([`09-gateway-expectations`](09-gateway-expectations.md)). §3c фокус — OAuth/GPT landing; lazy web-gate — §3b.

**Disclosure SSOT:** [`onboarding-copy.md`](../runbook/onboarding-copy.md) ([DOC-IDS-ONB-02](../tasks/backlog-stories/identity-onboarding/DOC-IDS-ONB-02-disclosure-copy.md)).

**Вне scope этого контракта:** пиксель/разметка spa; waitlist-механизм — [`onboarding-waitlist.md`](../runbook/onboarding-waitlist.md) ([DOC-IDS-ONB-04](../tasks/backlog-stories/identity-onboarding/DOC-IDS-ONB-04-non-ee-waitlist-spec.md)).

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
**Активно (phone + GPT):** login + verify landing — §3 / §3b / **§3c** (`/login?oauth_request_id=…`, `/verify?context=…`, возврат через OAuth complete). База URL spa берётся из `CORS_ALLOWED_ORIGINS[0]` ([`spa_login.py`](../../src/core/oauth/spa_login.py)).  
**⏸️ deferred (eID):** отдельный eID return_url / callback — §3a / §4; identity редиректит 303 с `eid_status` / `eid_error`.

## Сводка

| Что ждём от UI | Чем проверяется в identity | Статус |
|----------------|----------------------------|--------|
| Запросы с разрешённого origin | `CORS_ALLOWED_ORIGINS` | ✅ |
| Bearer Supabase JWT в запросах | `get_current_user` | ✅ |
| Inline phone-verify: `request` → `confirm` (без redirect) | `POST /auth/phone/request` + `POST /auth/phone/confirm`, гейт `phone_verified` | ✅ активно |
| Lazy gate: verify-экран при `phone_verified=false` на защищённом действии | §3b — `GET /me` перед действием | ✅ контракт (spa-app) |
| GPT verify landing `/verify?context=` + возврат в GPT через OAuth complete | §3c — `verify_url` / `authorize/complete` 302 | ✅ контракт (spa-app) |
| `return_url`/`return_context` при старте eID | поля сессии + `validate_return_url` на start | ⏸️ deferred (eID) |
| Белый список возвратных URL | `ALLOWED_RETURN_URLS` + redirect только на сохранённый URL | ⏸️ deferred (eID) |
| SPA-first callback → 303 back | `eid_status` / `eid_error` query markers | ⏸️ deferred (eID) |

## Главное
Всё «ожидаемое от UI» — это **контракт**, а не код в этом репозитории. Активный GPT/phone verify landing — §3c. SPA-first eID redirect-модель (start → provider → callback → 303 back) — deferred; см. [`06-eid-providers`](06-eid-providers.md) и [`eid_callback.py`](../../src/core/api/eid_callback.py).
