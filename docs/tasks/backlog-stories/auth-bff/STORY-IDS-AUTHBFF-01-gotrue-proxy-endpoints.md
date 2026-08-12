# STORY-IDS-AUTHBFF-01 — GoTrue-клиент + login/signup/logout proxy

## Meta
- **Key:** `STORY-IDS-AUTHBFF-01-gotrue-proxy-endpoints`
- **Epic:** [`EPIC-IDS-AUTHBFF`](EPIC-IDS-AUTHBFF.md)
- **Status:** 🟦 POST-MVP (см. [README.md](README.md))
- **Источник / контракт:** [`auth-bff-proxy-design-2026-06-27.md`](../../../analysis/auth-bff-proxy-design-2026-06-27.md) §3, §6
- **Зависит от:** — (фундамент BFF)

## Зачем простыми словами
identity сейчас умеет ходить в Supabase только в Postgres (`/rest/v1`, service_role). Для проксирования логина нужен **второй клиент** — к Supabase **GoTrue** (`/auth/v1`), и три эндпоинта, через которые браузер логинится/регистрируется/выходит **не касаясь Supabase напрямую**.

## Точки в коде (текущее состояние)
- HTTP-клиент только PostgREST: [`SupabaseDatabase.from_http` db_supabase.py:235-254](../../../../src/core/infrastructure/db_supabase.py) (apikey/Authorization = service_role).
- Login-эндпоинтов **нет** ([`asgi_app.py`](../../../../src/core/api/asgi_app.py)).
- В конфиге **нет** anon-ключа — только `supabase_url`/`service_role`/`jwt_secret` ([`schema.py:32-34,158-160`](../../../../src/core/config/schema.py)).

## Scope
- **Конфиг:** добавить `SUPABASE_ANON_KEY` в `AppConfig` (apikey для public GoTrue-ops). *(Альтернатива — использовать service_role как apikey, server-only; зафиксировать выбор.)*
- **GoTrue-клиент:** отдельный HTTP-клиент к `{SUPABASE_URL}/auth/v1/*` (apikey-заголовок), не путать с PostgREST-клиентом.
- **Эндпоинты:** `POST /auth/login` (`/token?grant_type=password`), `POST /auth/signup` (`/signup`), `POST /auth/logout` (`/logout`). Маппинг ошибок GoTrue → наш envelope (`401` неверные креды, и т.д.).
- Выдача сессии браузеру — **в AUTHBFF-02** (тут эндпоинты возвращают результат GoTrue во внутреннем виде, готовом для cookie-слоя).
- **Rate-limit:** `/auth/login|signup` подключить к существующему слою (SEC-01) — анти-stuffing.

## Вне scope
- Cookie/сессия/refresh/CSRF — [AUTHBFF-02](STORY-IDS-AUTHBFF-02-cookie-session-refresh-csrf.md).
- magic-link / reset / email-redirect — [AUTHBFF-03](STORY-IDS-AUTHBFF-03-magic-link-reset-email-redirect.md).
- Замена Supabase своим auth (не цель — Supabase остаётся движком).

## Acceptance Criteria
- [ ] `SUPABASE_ANON_KEY` (или решение про service_role-apikey) в конфиге; pilot-fail-fast при `DB_BACKEND=supabase` если нужно.
- [ ] GoTrue-клиент шлёт в `/auth/v1/*` с корректным apikey; не использует PostgREST-клиент.
- [ ] `POST /auth/login|signup|logout` работают (offline-тесты с mock GoTrue): успех/401/ошибки замаплены в envelope.
- [ ] `/auth/login|signup` под rate-limit (SEC-01).

## Парадигма-якорь
[`design-doc §3,§6,§7`](../../../analysis/auth-bff-proxy-design-2026-06-27.md), [04-security](../../../runtime-docs/04-security.md).
