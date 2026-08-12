# STORY-IDS-OAUTH-02 — Межсервисная валидация: introspection + сервисный токен

## Meta
- **Key:** `STORY-IDS-OAUTH-02-introspection-and-service-token`
- **Parent Epic:** [`../../EPIC-IDS-11-oauth-server.md`](../../EPIC-IDS-11-oauth-server.md)
- **Epic alias (код/backlog):** `EPIC-IDS-OAUTH` · продуктовый зонтик [`EPIC-IDS-ONBOARDING`](../../../../backlog-stories/identity-onboarding/EPIC-IDS-ONBOARDING.md)
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md)
- **Decision Ref:** [`../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md); [`identity-todo-backlog-2026-06-04`](../../../../../analysis/identity-todo-backlog-2026-06-04.md) — B5, B6; gap API-1, CFG-1
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../../../analysis/identity-todo-backlog-2026-06-04.md) — B5, B6; gap API-1, CFG-1
- **Зависит от:** [STORY-IDS-AUTHCORE-01](../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-01-profile-and-me.md) (`/me`/профиль — **построен**), [STORY-IDS-OAUTH-01](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) (выдаёт токен — **🟢 построен**, pkg-000029), [PV-05](../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md) ✅ (источник `phone_verified` — **активный гейт**); eID-источник — DEFERRED

> **Phone-pivot (2026-06):** активный гейт — `phone_verified`, не `eid_verified`. Introspection отдаёт **`phone_verified`** (eID — отложен). `/me` уже построен (не 501).

## Зачем простыми словами
Это «склейка» с gateway по согласованной модели (решение 2026-06-04): **gateway сам спрашивает identity**, валиден ли пользовательский токен и пройден ли eID. Для этого identity нужен endpoint introspection (или рабочий `/me`), а на вход — проверка сервисного токена, чтобы дёргать его могли только доверенные сервисы. Сейчас **обоих** механизмов нет.

## Scope
- Endpoint introspection: по пользовательскому токену вернуть `{active, sub, phone_verified}` (eID — опц./DEFERRED), либо формализовать построенный `/me` как этот источник.
- Проверка входящего **сервисного токена** (`SERVICE_API_TOKEN`): добавить в конфиг + middleware/зависимость.
- Модель: eID-статус **не в токене** (решение) — отдаётся introspection'ом из профиля.

## Вне scope
- Изменение алгоритма подписи OAuth-токена (HS256 остаётся — gateway не валидирует подпись, а спрашивает introspection).
- Код на стороне gateway (это его репозиторий).

## Точки в коде (текущее состояние)
- `/oauth/introspect` — **построен** ([`asgi_app.py`](../../../../../../src/core/api/asgi_app.py), [`core/oauth/introspection.py`](../../../../../../src/core/oauth/introspection.py)).
- `/me` — **построен** (AUTHCORE-01; phone-поля в [`me_response.py`](../../../../../../src/core/api/me_response.py)).
- `SERVICE_API_TOKEN` — **в** `AppConfig.service_api_token` ([`config/schema.py`](../../../../../../src/core/config/schema.py)); gate через `ServiceTokenAuth`.
- Валидатор пользовательского токена: `OAuthTokenService.validate_access_token` ([`repositories.py:536-545`](../../../../../../src/core/infrastructure/repositories.py)).

## Acceptance Criteria
- [x] introspection с валидным токеном → `{active:true, sub, phone_verified}`; с просроченным/битым → `{active:false}`.
- [x] Запрос без валидного сервисного токена → 401/403 (даже с валидным пользовательским токеном).
- [x] `phone_verified` берётся из профиля, не из тела токена.
- [x] Покрыто тестами (offline) + зафиксирован контракт ответа для gateway.

## Парадигма-якорь
[04-security §Часть A «два слоя»](../../../../../runtime-docs/04-security.md), [09-gateway-expectations §Модель аутентификации](../../../../../runtime-docs/09-gateway-expectations.md).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-11-02-t01-service-api-token-config`](./task-ids-11-02-t01-service-api-token-config/README.md) | pkg-000030 |
| 2 | [`task-ids-11-02-t02-service-token-auth-dependency`](./task-ids-11-02-t02-service-token-auth-dependency/README.md) | pkg-000030 |
| 3 | [`task-ids-11-02-t03-oauth-introspection-handler`](./task-ids-11-02-t03-oauth-introspection-handler/README.md) | pkg-000030 |
| 4 | [`task-ids-11-02-t04-oauth-introspect-route`](./task-ids-11-02-t04-oauth-introspect-route/README.md) | pkg-000030 |
| 5 | [`task-ids-11-02-t05-offline-introspection-tests`](./task-ids-11-02-t05-offline-introspection-tests/README.md) | pkg-000030 |
| 6 | [`task-ids-11-02-t06-story-acceptance-verification`](./task-ids-11-02-t06-story-acceptance-verification/README.md) | pkg-000030 |
