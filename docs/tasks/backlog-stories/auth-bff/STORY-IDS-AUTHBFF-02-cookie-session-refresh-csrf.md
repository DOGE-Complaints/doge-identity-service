# STORY-IDS-AUTHBFF-02 — httpOnly-cookie сессия + server-side refresh + CSRF

## Meta
- **Key:** `STORY-IDS-AUTHBFF-02-cookie-session-refresh-csrf`
- **Epic:** [`EPIC-IDS-AUTHBFF`](EPIC-IDS-AUTHBFF.md)
- **Status:** 🟦 POST-MVP (см. [README.md](README.md))
- **Источник / контракт:** [`auth-bff-proxy-design-2026-06-27.md`](../../../analysis/auth-bff-proxy-design-2026-06-27.md) §4, §5, §7
- **Зависит от:** [AUTHBFF-01](STORY-IDS-AUTHBFF-01-gotrue-proxy-endpoints.md) (эндпоинты выдают токены GoTrue)

## Зачем простыми словами
Это **ядро BFF**: после логина браузер не должен видеть токены. identity ставит **httpOnly-cookie**, держит refresh-token **на сервере** и прозрачно обновляет access. Существующие защищённые роуты (`/me`, `/auth/phone`, `/oauth`) должны брать пользователя **из cookie-сессии**, а не только из `Authorization`-заголовка.

## Точки в коде (текущее состояние)
- Cookie/сессия-инфры в `api/` **нет** (grep `Set-Cookie/csrf` → пусто).
- `get_current_user` берёт только `Authorization: Bearer` ([`security.py`](../../../../src/core/api/security.py)).
- JWT валидируется `SupabaseJwtValidatorImpl` ([`supabase_validator.py`](../../../../src/core/auth/supabase_validator.py)) — **переиспользуем без изменений** (access-token остаётся Supabase-выпущенным).

## Scope
- **Cookie-сессия:** после login/signup ставить httpOnly+Secure+SameSite cookie. Содержимое — по решению design §4: **stateless** (зашифрованный `{access,refresh,exp}` под server-ключом) **или** **stateful** (`session_id` → Supabase-стор). Зафиксировать выбор.
- **Server-side refresh:** при истёкшем access — рефреш у GoTrue (`grant_type=refresh_token`), пере-выставить cookie. Браузер refresh не видит.
- **`GET /auth/session`:** по cookie → `{authenticated, user}` (рефреш при нужде) / 401.
- **`get_current_user` расширить:** источник Bearer = cookie-сессия **в дополнение** к заголовку (для обратной совместимости API-клиентов).
- **CSRF:** на мутирующих запросах (cookie-режим) — double-submit-token или SameSite=Strict + обязательный кастом-заголовок. Зафиксировать.
- **CORS с credentials:** `Allow-Credentials: true` + точечные origin'ы (не `*`).
- `logout` — очистка cookie + GoTrue logout (из AUTHBFF-01).

## Вне scope
- Сами proxy-эндпоинты login/signup — [AUTHBFF-01](STORY-IDS-AUTHBFF-01-gotrue-proxy-endpoints.md).
- email-флоу — [AUTHBFF-03](STORY-IDS-AUTHBFF-03-magic-link-reset-email-redirect.md).

## Acceptance Criteria
- [ ] После login/signup — httpOnly+Secure+SameSite cookie; в ответе/браузере **нет** access/refresh-токенов.
- [ ] Истёкший access → прозрачный server-refresh → запрос проходит; refresh-token в браузер не попадает.
- [ ] `/me` (и phone/oauth) работают **по cookie** (без ручного Bearer) — тест.
- [ ] CSRF-защита на мутациях; CORS-credentials настроены; offline-тесты.
- [ ] `GET /auth/session` отражает статус; `logout` гасит сессию.

## Парадигма-якорь
[`design-doc §4,§5,§7`](../../../analysis/auth-bff-proxy-design-2026-06-27.md), [04-security](../../../runtime-docs/04-security.md).
