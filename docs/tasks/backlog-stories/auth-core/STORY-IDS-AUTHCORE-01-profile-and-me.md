# STORY-IDS-AUTHCORE-01 — Профиль пользователя и `GET /me`

## Meta
- **Key:** `STORY-IDS-AUTHCORE-01-profile-and-me`
- **Epic:** `EPIC-IDS-07` (alias в коде: `EPIC-IDS-AUTH-CORE`)
- **Status:** 🟢 Done
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../analysis/identity-todo-backlog-2026-06-04.md) — A1; runtime-doc [01-api](../../../runtime-docs/01-api.md), [05-data-model](../../../runtime-docs/05-data-model.md)
- **Исполнение:** pipeline story + pkg-000009 (2026-06-04)
- **Зависит от:** — (базовая; инфраструктура AUTH уже готова в EPIC-IDS-04)

## Зачем простыми словами
`GET /me` — первый «настоящий» защищённый маршрут identity: по токену пользователя возвращает профиль и ключевой признак — пройдена ли eID-верификация. Ответ переиспользуется как источник правды для gateway (см. [STORY-IDS-OAUTH-02](../oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md)).

## Scope
- Реализовать `handle_me` вместо заглушки `handle_me_stub` ([`handlers.py`](../../../../src/core/api/handlers.py)).
- Достать профиль из `ProfileRepository` по `supabase_user_id` из `UserClaims`.
- Вернуть профиль + `eid_verified` + базовые права.
- Если профиля ещё нет — определить поведение (создать пустой / вернуть «не верифицирован»).

## Вне scope
- eID-флоу (отдельно — [STORY-IDS-EID-01](../eid/STORY-IDS-EID-01-eid-verification-flow.md)).
- OAuth-сервер.

## Точки в коде (текущее состояние)
- Маршрут: [`asgi_app.py`](../../../../src/core/api/asgi_app.py) → `handle_me` → 200 + envelope `data`.
- Payload: [`me_response.py`](../../../../src/core/api/me_response.py) — `build_me_data`.
- Тесты: [`test_me_profile.py`](../../../../tests/test_me_profile.py).

## Acceptance Criteria
- [x] `GET /me` без токена → 401 `AUTHENTICATION_REQUIRED`.
- [x] `GET /me` с валидным Supabase JWT → 200, `data` содержит как минимум `supabase_user_id`, `eid_verified`, и (если есть) поля профиля.
- [x] Если профиля нет — поведение детерминировано и покрыто тестом.
- [x] Ответ в envelope-формате `{"data": {...}}`.
- [x] Покрыто тестами (offline, без сети) на оба backend'а (`in_memory`).

## Парадигма-якорь
[04-security §Часть A](../../../runtime-docs/04-security.md) — `/me`/introspection как точка, где gateway узнаёт `eid_verified`.
