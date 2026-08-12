# STORY-IDS-OAUTH-02 — Межсервисная валидация: introspection + сервисный токен

## Meta
- **Key:** `STORY-IDS-OAUTH-02-introspection-and-service-token`
- **Epic:** `EPIC-IDS-ONBOARDING` (продуктовый зонтик — [`identity-onboarding/`](../identity-onboarding/EPIC-IDS-ONBOARDING.md)); код-алиас `EPIC-IDS-OAUTH` (`next_epic` в `asgi_app.py`)
- **Status:** 🟢 Done
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../analysis/identity-todo-backlog-2026-06-04.md) — B5, B6; gap API-1, CFG-1
- **Зависит от:** [STORY-IDS-AUTHCORE-01](../auth-core/STORY-IDS-AUTHCORE-01-profile-and-me.md) (`/me`/профиль — **построен**), [STORY-IDS-OAUTH-01](STORY-IDS-OAUTH-01-oauth-server-endpoints.md) (выдаёт токен — **🟢 построен**, pkg-000029), [PV-05](../phone-verification/STORY-IDS-PV-05-verification-flow-api.md) ✅ (источник `phone_verified` — **активный гейт**); eID-источник — DEFERRED

> **Phone-pivot (2026-06):** активный гейт — `phone_verified`, не `eid_verified`. Introspection отдаёт **`phone_verified`** (eID — отложен). `/me` уже построен (не 501).

## Зачем простыми словами
Это «склейка» с gateway по согласованной модели (решение 2026-06-04): **gateway сам спрашивает identity**, валиден ли пользовательский токен и пройдена ли верификация (телефон). Introspection (`POST /oauth/introspect`) и сервисный gate (`SERVICE_API_TOKEN`) **построены** (pkg-000030).

## Scope
- Endpoint introspection: по пользовательскому токену вернуть `{active, sub, phone_verified}` (eID — опц./DEFERRED), либо формализовать построенный `/me` как этот источник.
- Проверка входящего **сервисного токена** (`SERVICE_API_TOKEN`): добавить в конфиг + middleware/зависимость.
- Модель: eID-статус **не в токене** (решение) — отдаётся introspection'ом из профиля.

## Вне scope
- Изменение алгоритма подписи OAuth-токена (HS256 остаётся — gateway не валидирует подпись, а спрашивает introspection).
- Код на стороне gateway (это его репозиторий).

## Точки в коде (текущее состояние)
- `/oauth/introspect` — **построен** ([`asgi_app.py`](../../../../src/core/api/asgi_app.py), [`core/oauth/introspection.py`](../../../../src/core/oauth/introspection.py)).
- `/me` — **построен** (AUTHCORE-01; phone-поля в [`me_response.py`](../../../../src/core/api/me_response.py)).
- `SERVICE_API_TOKEN` — **в** `AppConfig.service_api_token` ([`config/schema.py`](../../../../src/core/config/schema.py)).
- Валидатор пользовательского токена: `OAuthTokenService.validate_access_token` ([`repositories.py:536-545`](../../../../src/core/infrastructure/repositories.py)).

## Acceptance Criteria
- [x] introspection с валидным токеном → `{active:true, sub, phone_verified}`; с просроченным/битым → `{active:false}`.
- [x] Запрос без валидного сервисного токена → 401/403 (даже с валидным пользовательским токеном).
- [x] `phone_verified` берётся из профиля, не из тела токена.
- [x] Покрыто тестами (offline) + зафиксирован контракт ответа для gateway.

## Парадигма-якорь
[04-security §Часть A «два слоя»](../../../runtime-docs/04-security.md), [09-gateway-expectations §Модель аутентификации](../../../runtime-docs/09-gateway-expectations.md).
