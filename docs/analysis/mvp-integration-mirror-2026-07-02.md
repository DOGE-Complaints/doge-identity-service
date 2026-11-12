# MVP-зеркало: сквозная интеграция gateway ↔ identity ↔ GPT ↔ spa-app (2026-07-02)

> **Цель зеркала:** синхронная карта **фактического** состояния кода для полного MVP-цикла на railway.com:
> (1) создание истории через онбординг с верификацией телефона (пока mock SMS), (2) отдельная авторизация в веб-приложении по ссылке, (3) просмотр issues **без авторизации**, (4) заглушки кабинета.
> **Метод:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — только claims с `file:line`; неподтверждённое помечено ⚠️.
> **Статус:** шаг **A (зеркало)**. План и выполнение — отдельно (см. §7).

---

## 1. Карта системы (что есть по факту)

| Часть | Что это | Точки входа / артефакты |
|-------|---------|-------------------------|
| **doge-complaints-gateway** | Python/FastAPI сервис: приём историй + публичные issues Таллина | [`asgi_app.py`](../../../doge-complaints-gateway/src/core/api/asgi_app.py) (роуты), порт **8000** |
| **doge-identity-service** | Python/FastAPI: auth (Supabase-JWT), phone-верификация, OAuth для GPT, introspection | [`asgi_app.py`](../../src/core/api/asgi_app.py), порт **8100** |
| **GPT UI/** | Отдельный git-репо с `instructions/` + `docs/` — **промпты Custom GPT, не сервис** | [`GPT UI/instructions/api-orchestrator.md`](../../../GPT%20UI/instructions/api-orchestrator.md), `story-interview-flow.md`, `ingest-validation.md` |
| **spa-app** | React SPA (Vite, HashRouter) — доска issues + верификация + логин | [`App.jsx`](../../../spa-app/src/App.jsx), [`sessionRoutePolicy.js`](../../../spa-app/src/router/sessionRoutePolicy.js) |

**Деплой:** пока только identity+gateway на railway.com; **spa-app ещё НЕ выгружен**. identity [`railway.json`](../../railway.json) — только healthcheck `/health`, без `startCommand`/Volume.

---

## 2. Поток 1 — создание истории через онбординг (GPT → gateway → identity)

**Цепочка (по коду gateway):** `POST /intake/stories` защищён двумя зависимостями `_PUBLIC_CONTENT_WRITE_DEPS` ([`asgi_app.py:332-334,475`](../../../doge-complaints-gateway/src/core/api/asgi_app.py)):
1. **`require_public_content_service_auth`** ([`:291-295`](../../../doge-complaints-gateway/src/core/api/asgi_app.py)) — обязательный **service-token** (`service_auth.require(..., mandatory=True)`). Это креденшл самого GPT-оркестратора.
2. **`require_user_token`** ([`:298-330`](../../../doge-complaints-gateway/src/core/api/asgi_app.py)) — берёт user-token, **интроспектит его в identity** (`deps.identity_introspection.introspect`), и **гейтит по phone_verified**:
   - `VerificationGateOutcome.VERIFICATION_REQUIRED` → ошибка с `verify_url` ([`build_verify_url`](../../../doge-complaints-gateway/src/core/api/asgi_app.py)) → фронт ведёт на `/verify`.
   - `UNAUTHORIZED` → отказ.

**Вывод:** гейт «сначала верифицируй телефон, потом публикуй историю» реализован **на gateway** и опирается на **introspection endpoint identity**. Это ключевой интеграционный шов gateway→identity.

**Верификация телефона (identity, mock SMS):** `POST /auth/phone/request` → код → `POST /auth/phone/confirm` → `GET /me` (`phone_verified:true`). Правила: 6 цифр / TTL 5м / 5 попыток / cooldown 60с. При `SMS_PROVIDER=file` код пишется в `var/sms-outbox/<номер>.log` (`tail -f`); `mock` — только в память. Runbook: [`sms-mock-testing.md`](../runbook/sms-mock-testing.md).

**⚠️ Подтвердить при выполнении:**
- Какой именно endpoint дёргает GPT из [`api-orchestrator.md`](../../../GPT%20UI/instructions/api-orchestrator.md) и как получает user-token (OAuth-флоу identity).
- Формат тела `POST /intake/stories` (контракт story) — сверить GPT-инструкции ↔ gateway-хендлер [`handlers.py`](../../../doge-complaints-gateway/src/core/api/handlers.py).
- Что identity возвращает в introspection (поля, влияющие на `evaluate_verification_gate`).

---

## 3. Поток 2 — авторизация в веб-приложении по ссылке (spa → Supabase → identity)

**По коду spa:** логин-страница `/login` ([`App.jsx:16`](../../../spa-app/src/App.jsx), `LoginPage`) вне `AppShellLayout`. После Supabase-login сессия ведёт на защищённые роуты; `useSessionShellState` дёргает identity `GET /me`.

**Критичный известный блокер (из прошлой сессии, подтверждён):** Supabase **Cloud** (проект `ydocxoquirltrrfmvpqz`, [`spa-app/.env:23`](../../../spa-app/.env)) подписывает JWT алгоритмом **ES256**; identity-валидатор изначально знал только HS256 → `GET /me` 401 → spa показывал «Session Expired» на `#/verify`. Фикс ES256/JWKS **на диске, не закоммичен, с костылями** → оформлен в [`STORY-IDS-SEC-06`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md) (🔴 HIGH). Детали: [`identity-build-session-pv10-jwt-2026-06-28.md §10`](./identity-build-session-pv10-jwt-2026-06-28.md).

**Вывод:** для рабочего веб-логина против Cloud ES256-фикс должен быть **закоммичен и задеплоен** на identity (railway). Это блокер потока 2.

**⚠️ Подтвердить:** точная цепочка `LoginPage` → `supabase.auth` → сохранение токена → `fetchMe` → `sessionShellState`.

---

## 4. Поток 3 — публичные issues (БЕЗ авторизации) — ✅ ПОДТВЕРЖДЕНО

**Gateway (read-роуты без `dependencies`):**
- `GET /tallinn/issues` ([`asgi_app.py:403`](../../../doge-complaints-gateway/src/core/api/asgi_app.py)) — **публичный**.
- `GET /tallinn/issues/{issue_id}` ([`:445`](../../../doge-complaints-gateway/src/core/api/asgi_app.py)) — **публичный**.
- (Только write-роуты `POST /tallinn/issues`, `/intake/stories` требуют auth.)

**SPA (политика роутов):** [`sessionRoutePolicy.js:1-16`](../../../spa-app/src/router/sessionRoutePolicy.js):
- **PUBLIC:** `/`, `/board`, `/login`, `/issue/:id` → доска и деталь issue **не требуют логина**.
- PROTECTED: `/dashboard`, `/profile`, `/story/compose`, `/verify`.
- Репозиторий issues: [`GatewayIssueRepository.js:73-84`](../../../spa-app/src/repositories/GatewayIssueRepository.js) — `GET {VITE_GATEWAY_BASE_URL}/tallinn/issues` **без Authorization**.

**Вывод:** требование «issues видны без авторизации» **выполнено и на gateway, и на spa**. Регресса нет.

---

## 5. Поток 4 — заглушки кабинета (частично есть)

- **`/profile`** = `ProtectedProfilePage` → `ProtectedPlaceholder title="Profile"` ([`AppShellLayout.jsx:12-16,44-45`](../../../spa-app/src/layout/AppShellLayout.jsx)) — **заглушка уже есть** («Protected area — session shell guard applies»), защищена гейтом сессии.
- **`/dashboard`** = `DashboardPage` ([`App.jsx:21`](../../../spa-app/src/App.jsx), [`DashboardPage.jsx`](../../../spa-app/src/pages/DashboardPage.jsx)) — ⚠️ содержимое подтвердить (stub или реальная доска).
- Контракт `GET /me` в identity уже отдаёт профиль-поля (`phone_verified`, `role`, `display_name`, …) — данные для кабинета есть.

**Вывод:** каркас кабинета (protected placeholder + guard) присутствует; «состыковать» = довести содержимое заглушек и связать с `/me`. ⚠️ Подтвердить состояние `DashboardPage`.

---

## 6. Интеграционные контракты и env/URL

| Вызов | Откуда | Куда | Auth |
|-------|--------|------|------|
| `GET /tallinn/issues` | spa (public board) | gateway :8000 | нет |
| `POST /intake/stories` | GPT-оркестратор | gateway :8000 | service-token + user-token(phone-verified via identity) |
| introspection user-token | gateway | identity :8100 | — (internal) |
| `POST /auth/phone/request|confirm`, `GET /me` | spa | identity :8100 | Supabase Bearer |
| OAuth (авторизация GPT) | GPT | identity :8100 | OAuth 2.0 |

**SPA `.env` (факт, [`spa-app/.env`](../../../spa-app/.env)):** `VITE_LIFE_REALITY_MODE=GFL-DRIVEN` (реальный gateway, не mock), `VITE_GATEWAY_BASE_URL=http://127.0.0.1:8000`, `VITE_IDENTITY_SERVICE_URL=http://127.0.0.1:8100`, `VITE_IDENTITY_MOCK_MODE=false`, `VITE_SUPABASE_URL=https://ydocxoquirltrrfmvpqz.supabase.co`.

**⚠️ Railway-разрыв:** все URL — `127.0.0.1` (локальные). Для railway spa-сборка должна указывать на **публичные** URL gateway/identity; localhost не сработает из браузера пользователя.

---

## 7. Предварительный gap-лист (сид для плана — уточнить при выполнении)

| ID | Severity | Разрыв | Где |
|----|----------|--------|-----|
| **M-1** | 🔴 HIGH | ES256/JWKS-фикс identity не закоммичен и с костылями → веб-логин против Cloud падает 401 | [`SEC-06`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md), [`build-session §10`](./identity-build-session-pv10-jwt-2026-06-28.md) |
| **M-2** | 🟠 MED | spa не задеплоен + `.env` URLs=127.0.0.1 → на railway фронт не достучится до gateway/identity | [`spa-app/.env`](../../../spa-app/.env) |
| **M-3** | 🟠 MED | Онбординг-гейт story-intake зависит от introspection identity — сверить сквозной контракт GPT→gateway→identity (поля, phone_verified) | gateway [`:298-330`](../../../doge-complaints-gateway/src/core/api/asgi_app.py) |
| **M-4** | 🟡 LOW-MED | Кабинет — только placeholder; довести заглушки и связать с `/me` | [`AppShellLayout.jsx:44`](../../../spa-app/src/layout/AppShellLayout.jsx), [`DashboardPage.jsx`](../../../spa-app/src/pages/DashboardPage.jsx) |
| **M-5** | 🟢 подтверждено | Issues публичны (gateway + spa) — **не разрыв**, зафиксировать как гарантию (регресс-тест) | §4 |
| **M-6** | ⚠️ verify | Mock SMS: для ручного онбординга включить `SMS_PROVIDER=file`; на railway чтение файла неудобно (эфемерная ФС) | [`sms-mock-testing.md`](../runbook/sms-mock-testing.md) |

**Открытые вопросы для выполнения:** точный endpoint/контракт вызова GPT→gateway; цепочка spa login→Supabase→`/me`; состояние `DashboardPage`; как identity introspection отдаёт `phone_verified`; публичные URL для railway-сборки spa.

---

## 8. Связанные документы
- Identity состояние: [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md), [`identity-backend-full-audit-2026-06-24.md`](./identity-backend-full-audit-2026-06-24.md)
- JWT/session: [`identity-build-session-pv10-jwt-2026-06-28.md`](./identity-build-session-pv10-jwt-2026-06-28.md), [`SEC-06`](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-06-supabase-jwks-es256-hardening.md)
- Mock SMS: [`runbook/sms-mock-testing.md`](../runbook/sms-mock-testing.md), phone API [`runbook/onboarding-phone-verification-api.md`](../runbook/onboarding-phone-verification-api.md)
- SPA↔Supabase граница: [`spa-app/.../identity-supabase-frontend-split-2026-06-16.md`](../../../spa-app/docs/analysis/identity-supabase-frontend-split-2026-06-16.md); онбординг-стори [`spa-app/.../identity-auth/`](../../../spa-app/docs/tasks/backlog-stories/identity-auth/)
- Gateway: [`high-level-description.md`](../../../doge-complaints-gateway/docs/high-level-description.md), [`04-security-audit.md`](../../../doge-complaints-gateway/docs/04-security-audit.md)
