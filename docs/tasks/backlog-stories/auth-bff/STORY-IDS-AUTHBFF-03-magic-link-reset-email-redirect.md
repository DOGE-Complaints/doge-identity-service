# STORY-IDS-AUTHBFF-03 — magic-link / reset / email-confirm redirect в наш контур

## Meta
- **Key:** `STORY-IDS-AUTHBFF-03-magic-link-reset-email-redirect`
- **Epic:** [`EPIC-IDS-AUTHBFF`](EPIC-IDS-AUTHBFF.md)
- **Status:** 🟦 POST-MVP (см. [README.md](README.md))
- **Источник / контракт:** [`auth-bff-proxy-design-2026-06-27.md`](../../../analysis/auth-bff-proxy-design-2026-06-27.md) §3, §7
- **Зависит от:** [AUTHBFF-01](STORY-IDS-AUTHBFF-01-gotrue-proxy-endpoints.md), [AUTHBFF-02](STORY-IDS-AUTHBFF-02-cookie-session-refresh-csrf.md) (сессия — чтобы завершать вход после ссылки)

## Зачем простыми словами
Magic-link, сброс пароля и подтверждение email — это **письма от Supabase со ссылкой**. По умолчанию ссылка ведёт в контур Supabase. В BFF-модели ссылка должна вести **в наш контур** (identity/spa), чтобы по возврату мы поставили нашу httpOnly-cookie сессию, а не отдали токен напрямую браузеру.

## Точки в коде (текущее состояние)
- Эндпоинтов magic-link/reset нет; email-redirect нигде не настраивается ([`asgi_app.py`](../../../../src/core/api/asgi_app.py)).
- GoTrue-клиент появляется в [AUTHBFF-01](STORY-IDS-AUTHBFF-01-gotrue-proxy-endpoints.md); cookie-сессия — в [AUTHBFF-02](STORY-IDS-AUTHBFF-02-cookie-session-refresh-csrf.md).

## Scope
- **`POST /auth/magic-link`** (`/auth/v1/otp`) и **`POST /auth/reset-password`** (`/auth/v1/recover`) с `redirect_to` в **наш** маршрут.
- **Callback-завершение:** маршрут (identity или spa→identity), который принимает возврат по ссылке (magic-link/confirm/recover), обменивает у GoTrue на сессию и **ставит httpOnly-cookie** (через слой AUTHBFF-02).
- **Email-confirm:** при `signup` с включённым Confirm-email — `redirect_to` в наш контур; по подтверждению — сессия ставится у нас.
- **Конфиг Supabase Dashboard:** задокументировать (runbook) разрешённые `redirect_to`-URL.

## Вне scope
- UI-страницы (spa) для magic-link/reset/confirm — spa-сторона.
- Сам OTP-телефон (`/auth/phone/*`) — это другой механизм (PV), не email.

## Acceptance Criteria
- [ ] `/auth/magic-link` и `/auth/reset-password` шлют письма с `redirect_to` в наш контур (не дефолт Supabase).
- [ ] Возврат по ссылке → обмен у GoTrue → httpOnly-cookie сессия (не токен в браузер).
- [ ] Email-confirm (если включён) завершается нашей сессией.
- [ ] Разрешённые redirect-URL задокументированы (runbook) + проверка allowlist.
- [ ] Offline-тесты (mock GoTrue) на оба флоу.

## Парадигма-якорь
[`design-doc §3,§7`](../../../analysis/auth-bff-proxy-design-2026-06-27.md), [08-ui-expectations](../../../runtime-docs/08-ui-expectations.md).
