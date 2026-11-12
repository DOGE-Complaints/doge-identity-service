# Auth-BFF: identity проксирует коробочный Supabase-Auth (контракт + решения)

> **Дата:** 2026-06-27
> **Методология:** [`analysis.mdc`](../../../.cursor/rules/analysis.mdc) — текущее состояние сверено с кодом (`file:line`); целевое — проектируется как контракт для сборки.
> **Решение оператора (2026-06-27):** перенести **весь коробочный Supabase-Auth юзера с фронта в identity** (браузер без Supabase-кредов). Модель сессии — **httpOnly cookie** (refresh только на сервере). Supabase **остаётся** движком за identity (proxy), не заменяется.
> **Контекст:** реализует **вариант B** из [SEC-05](../tasks/backlog-stories/security-hardening/STORY-IDS-SEC-05-auth-credential-model-adr.md) / [SPA-SEC-02](../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-02-supabase-credential-boundary.md). Карта «что было на фронте» — [`identity-supabase-frontend-split`](../../../spa-app/docs/analysis/identity-supabase-frontend-split-2026-06-16.md).

## 1. Важная поправка (по факту кода)

`service_role`, лежавший в `spa-app/.env`, фронтом **не использовался** (клиент на `anon` — [`supabaseClient.js:4-5,23`](../../../spa-app/src/auth/supabaseClient.js); `.from/.rpc/.storage` в `src` — нет). Сборка signup работает на **anon**, не на service_role. То есть **миграция «функционала на service_role» не нужна — его не было**. Эта работа — про другое: убрать из браузера **anon-Auth-поверхность** (login/signup/session), перенеся её в identity-proxy.

## 2. Что переносим (коробочный Supabase-Auth с фронта)

Сейчас браузер вызывает напрямую ([`LoginPage.jsx`](../../../spa-app/src/pages/LoginPage.jsx), [`useAuthSession.js`](../../../spa-app/src/auth/useAuthSession.js)):
`signUp`, `signInWithPassword`, `signInWithOtp` (magic link), `resetPasswordForEmail`, `getSession`, `onAuthStateChange`, `signOut`.

## 3. Целевой контракт (identity-эндпоинты → GoTrue за ними)

Браузер ходит **только в identity** (`fetch`, `credentials: 'include'`); identity ходит в Supabase GoTrue (`{SUPABASE_URL}/auth/v1/*`) server-side.

| identity-эндпоинт | Тело | GoTrue за ним | Ответ браузеру |
|-------------------|------|---------------|----------------|
| `POST /auth/signup` | `{email, password}` | `/auth/v1/signup` | 200 + **Set-Cookie** (если confirm выкл) ИЛИ 200 `{status:"confirm_email_sent"}` |
| `POST /auth/login` | `{email, password}` | `/auth/v1/token?grant_type=password` | 200 + **Set-Cookie**; 401 при неверных |
| `POST /auth/magic-link` | `{email}` | `/auth/v1/otp` | 200 `{status:"sent"}` |
| `POST /auth/reset-password` | `{email}` | `/auth/v1/recover` | 200 `{status:"sent"}` |
| `POST /auth/logout` | — (cookie) | `/auth/v1/logout` | 200 + **очистка cookie** |
| `GET /auth/session` | — (cookie) | refresh при необходимости (`grant_type=refresh_token`) | 200 `{authenticated, user}` / 401 |

`onAuthStateChange` на фронте **уходит** — SPA узнаёт статус из `GET /auth/session` (по cookie). `/me`, `/auth/phone/*`, `/oauth/*` — **без изменений контракта**, но Bearer берётся из cookie-сессии (см. §5).

## 4. Модель сессии (решение: httpOnly cookie, refresh на сервере)

- После login/signup identity получает от GoTrue `{access_token, refresh_token, expires_at}` и **ставит httpOnly cookie** (`Secure`, `SameSite=Lax|Strict`, `Path=/`, срок = refresh). **Браузер токены не видит.**
- **Где живёт refresh:** только на сервере identity. Варианты хранения cookie-содержимого:
  - **(рек.) Stateless:** cookie = зашифрованный (server-key) блоб `{access, refresh, exp}`; identity на каждом запросе расшифровывает, при истёкшем access — рефрешит у GoTrue и **пере-ставит** cookie. Нет server-store.
  - **Stateful:** cookie = opaque `session_id`; сервер-стор (Supabase Postgres, как OAuth/phone-сессии) хранит `{access, refresh}`. Durable, но это ещё одна таблица/стор.
- **Refresh:** прозрачно server-side при истечении access (GoTrue `grant_type=refresh_token`).

## 5. Совместимость с существующим (что НЕ меняется)

- Access-token остаётся **Supabase-выпущенным** → identity валидирует его **тем же** [`SupabaseJwtValidatorImpl`](../../src/core/auth/supabase_validator.py) (HS256, `iss/aud/sub/exp/role`). Ничего в валидации не меняется.
- `/me`, `/auth/phone/*`, `/oauth/*` — те же; меняется лишь **источник** Bearer: новая зависимость «достать access из cookie-сессии (refresh при нужде) → положить как текущего юзера». `get_current_user` расширяется на cookie-источник в дополнение к `Authorization: Bearer`.

## 6. Что net-new в identity (сейчас НЕТ — проверено)

| Нужно | Сейчас | Net-new? |
|-------|--------|----------|
| GoTrue HTTP-клиент (`/auth/v1/*`) | есть только PostgREST `/rest/v1` ([`db_supabase.py:235-254`](../../src/core/infrastructure/db_supabase.py), service_role) | **да** — отдельный клиент |
| `apikey` для GoTrue public-ops | у identity нет `anon` ([`schema.py`](../../src/core/config/schema.py) — только url/service_role/jwt_secret) | **да** — добавить `SUPABASE_ANON_KEY` (или использовать service_role как apikey, server-only) |
| Login/signup/magic/reset/logout/session эндпоинты | login-эндпоинтов нет ([`asgi_app.py`](../../src/core/api/asgi_app.py)) | **да** |
| Cookie/сессия/CSRF | нет cookie-инфры в `api/` | **да** — Set-Cookie, шифрование/стор, CSRF |
| Cookie-источник в `get_current_user` | сейчас только Bearer-header | **да** — расширение |

## 7. Острые подзадачи (не забыть)

- **CSRF:** при cookie-сессии — double-submit-token или `SameSite=Strict` + обязательный кастом-заголовок на мутирующих запросах.
- **CORS с credentials:** `CORS_ALLOWED_ORIGINS` точечные (не `*`) + `Allow-Credentials: true`; cookie-домен.
- **Email-confirm redirect:** Supabase шлёт письмо со ссылкой → `redirect_to` должен вести на **наш** маршрут (identity-callback или spa-страница, которая дёргает identity), а не на дефолт Supabase. Конфигурируется в Supabase Dashboard + `redirect_to` в `signUp`.
- **Magic-link / reset redirect:** аналогично — ссылки ведут в наш контур.
- **anon/url переезжают в identity-env:** браузер чист; identity держит `SUPABASE_URL` + `SUPABASE_ANON_KEY` (новый) + `SERVICE_ROLE` + `JWT_SECRET`.
- **Rate-limit:** новые `/auth/login|signup` — чувствительные; переиспользовать SEC-01 слой (per-IP/anti-credential-stuffing).

## 8. Что меняется на фронте (spa)

- Убрать прямой `@supabase/supabase-js` Auth ([`supabaseClient.js`](../../../spa-app/src/auth/supabaseClient.js), вызовы в [`LoginPage.jsx`](../../../spa-app/src/pages/LoginPage.jsx)); переписать на `fetch(identity, {credentials:'include'})`.
- `useAuthSession` → опрос `GET /auth/session` вместо Supabase-listener.
- Из браузерного `.env` уходят **все** `VITE_SUPABASE_*` (детали — spa [SPA-SEC-02](../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-02-supabase-credential-boundary.md)).

## 9. Размен (честно)

**+** браузер без Supabase-кредов; единый домен/контур; refresh-token недостижим для XSS; единая точка rate-limit/аудита логина.
**−** identity получает существенный новый слой (сессии/refresh/CSRF/email-redirect) — раньше его не было; +latency (лишний hop); поддержка cookie/CORS-credentials. Раньше split-doc §8 этого не требовал — оправдано целью «zero Supabase в браузере».

## 10. Стори (декомпозиция)

| Story | Что | Репо |
|-------|-----|------|
| [AUTHBFF-01](../tasks/backlog-stories/auth-bff/STORY-IDS-AUTHBFF-01-gotrue-proxy-endpoints.md) | GoTrue-клиент + `SUPABASE_ANON_KEY` + login/signup/logout proxy | identity |
| [AUTHBFF-02](../tasks/backlog-stories/auth-bff/STORY-IDS-AUTHBFF-02-cookie-session-refresh-csrf.md) | httpOnly-cookie сессия + server-side refresh + CSRF + cookie-источник в `get_current_user` | identity |
| [AUTHBFF-03](../tasks/backlog-stories/auth-bff/STORY-IDS-AUTHBFF-03-magic-link-reset-email-redirect.md) | magic-link / reset / email-confirm redirect в наш контур | identity |
| [SPA-SEC-02](../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-02-supabase-credential-boundary.md) | переписать SPA-клиент на identity (убрать прямой Supabase) | spa-app |

## Quality gate (analysis.mdc)
- [x] Текущее состояние (фронт на anon, service_role не используется, identity без login/cookie/anon) — сверено по коду с `file:line`.
- [x] Решения оператора (cookie / Supabase-behind-proxy) зафиксированы и положены в контракт.
- [x] Net-new vs reuse разведено (валидация JWT — reuse; GoTrue-клиент/cookie/эндпоинты — net-new).
- [x] Острые подзадачи (CSRF, CORS-credentials, email-redirect, anon-в-identity) перечислены.
