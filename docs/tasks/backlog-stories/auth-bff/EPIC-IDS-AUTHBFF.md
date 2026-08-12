# EPIC-IDS-AUTHBFF — identity как Auth-BFF (проксирование Supabase-Auth)

> **Статус:** 🟦 **POST-MVP** (решено 2026-06-28 — не берём сейчас; см. [`README.md`](README.md) §4) · **Тип:** Функциональный (auth) · **Создан:** 2026-06-27
> **📌 Сначала прочитай [`README.md`](README.md)** — записка простыми словами «зачем этот пакет» + промпт для spa-сессии.
> **Решение:** перенести коробочный Supabase-Auth юзера с фронта в identity (браузер без Supabase-кредов); сессия — **httpOnly cookie**; Supabase **остаётся** движком за proxy. Зафиксировано в [SEC-05](../security-hardening/STORY-IDS-SEC-05-auth-credential-model-adr.md) (вариант B).
> **Контракт/дизайн (SSOT):** [`auth-bff-proxy-design-2026-06-27.md`](../../../analysis/auth-bff-proxy-design-2026-06-27.md).

## Назначение
Сейчас браузер логинится напрямую в Supabase Auth (anon-ключ + URL в браузере). Цель — чтобы **браузер ходил только в identity**, а identity проксировал login/signup/magic-link/reset/logout/session в Supabase GoTrue **server-side**, выдавая браузеру **httpOnly-cookie** сессию (токены в браузер не попадают). Так из браузера уходят все Supabase-креды.

## Контекст
- Карта «что было на фронте»: [`identity-supabase-frontend-split`](../../../../../spa-app/docs/analysis/identity-supabase-frontend-split-2026-06-16.md).
- **Важно:** `service_role` фронтом не использовался — это **не** про него; это про вынос anon-Auth-поверхности.
- Net-new в identity: GoTrue-клиент, `SUPABASE_ANON_KEY`, login-эндпоинты, cookie/сессия/CSRF (сейчас всего этого нет — см. design §6).

## Состав (seed; детали — в design-doc)
| Story | Тема | Статус |
|-------|------|--------|
| [AUTHBFF-01](STORY-IDS-AUTHBFF-01-gotrue-proxy-endpoints.md) | GoTrue-клиент + `SUPABASE_ANON_KEY` + `POST /auth/login\|signup\|logout` | ⚪ Todo |
| [AUTHBFF-02](STORY-IDS-AUTHBFF-02-cookie-session-refresh-csrf.md) | httpOnly-cookie сессия + server-side refresh + CSRF + cookie-источник в `get_current_user` | ⚪ Todo |
| [AUTHBFF-03](STORY-IDS-AUTHBFF-03-magic-link-reset-email-redirect.md) | magic-link / reset / email-confirm redirect в наш контур | ⚪ Todo |

## Порядок
**AUTHBFF-01** (эндпоинты+клиент) → **AUTHBFF-02** (сессия — ядро) → **AUTHBFF-03** (email-флоу). Параллельно spa [SPA-SEC-02](../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-02-supabase-credential-boundary.md) переписывает клиент.

## Связь
[SEC-05 ADR](../security-hardening/STORY-IDS-SEC-05-auth-credential-model-adr.md) · [design-doc](../../../analysis/auth-bff-proxy-design-2026-06-27.md) · [04-security](../../../runtime-docs/04-security.md) · валидация JWT не меняется ([`supabase_validator.py`](../../../../src/core/auth/supabase_validator.py)).
