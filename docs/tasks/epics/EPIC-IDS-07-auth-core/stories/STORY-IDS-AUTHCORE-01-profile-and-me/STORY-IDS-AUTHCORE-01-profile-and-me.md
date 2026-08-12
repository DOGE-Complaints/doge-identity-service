# STORY-IDS-AUTHCORE-01 — Профиль пользователя и `GET /me`

## Meta
- **Key:** `STORY-IDS-AUTHCORE-01-profile-and-me`
- **Parent Epic:** [`../../../../EPIC-IDS-07-auth-core.md`](../../../../EPIC-IDS-07-auth-core.md)
- **Epic alias (код):** `EPIC-IDS-AUTH-CORE`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md`](../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-01-profile-and-me.md)
- **Decision Ref:** [`../../../../backlog-stories/STORY-IDS-AUTHCORE-01-profile-and-me.md`](../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-01-profile-and-me.md); [`identity-todo-backlog-2026-06-04`](../../../../../analysis/identity-todo-backlog-2026-06-04.md) A1; runtime-doc [01-api](../../../../../runtime-docs/01-api.md), [05-data-model](../../../../../runtime-docs/05-data-model.md), [04-security](../../../../../runtime-docs/04-security.md)
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../../../analysis/identity-todo-backlog-2026-06-04.md) — A1; runtime-doc [01-api](../../../../../runtime-docs/01-api.md), [05-data-model](../../../../../runtime-docs/05-data-model.md)
- **Зависит от:** — (базовая; инфраструктура AUTH уже готова в EPIC-IDS-04)

## Зачем простыми словами
Сейчас `GET /me` — заглушка, отдаёт 501. Это первый «настоящий» защищённый маршрут: по токену пользователя он должен вернуть его профиль и ключевой признак — пройдена ли eID-верификация. Этот же ответ потом переиспользуется как источник правды для gateway (см. [STORY-IDS-OAUTH-02](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md)).

## Scope
- Реализовать `handle_me` ([`handlers.py`](../../../../../../src/core/api/handlers.py)) — Done (stub удалён t09).
- Достать профиль из `ProfileRepository` по `supabase_user_id` из `UserClaims`.
- Вернуть профиль + `eid_verified` + базовые права.
- Если профиля ещё нет — определить поведение (создать пустой / вернуть «не верифицирован»).

## Вне scope
- eID-флоу (отдельно — [STORY-IDS-EID-01](../../../../backlog-stories/eid/STORY-IDS-EID-01-eid-verification-flow.md)).
- OAuth-сервер.

## Точки в коде (текущее состояние)
- Маршрут: [`asgi_app.py`](../../../../../../src/core/api/asgi_app.py) → `handle_me` → 200.
- Готово к использованию: `ProfileRepository` ([`contracts.py:23-40`](../../../../../../src/core/domain/contracts.py)), реализации InMemory/Supabase, `get_current_user` ([`security.py:65-70`](../../../../../../src/core/api/security.py)).

## Acceptance Criteria
- [x] `GET /me` без токена → 401 `AUTHENTICATION_REQUIRED`.
- [x] `GET /me` с валидным Supabase JWT → 200, `data` содержит как минимум `supabase_user_id`, `eid_verified`, и (если есть) поля профиля.
- [x] Если профиля нет — поведение детерминировано и покрыто тестом.
- [x] Ответ в envelope-формате `{"data": {...}}`.
- [x] Покрыто тестами (offline, без сети) на оба backend'а (`in_memory`).

## Парадигма-якорь
[04-security §Часть A](../../../../../runtime-docs/04-security.md) — `/me`/introspection как точка, где gateway узнаёт `eid_verified`.

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-07-01-t01-missing-profile-behavior-decision`](./task-ids-07-01-t01-missing-profile-behavior-decision/README.md) | pkg-000009 |
| 2 | [`task-ids-07-01-t02-handle-me-handler`](./task-ids-07-01-t02-handle-me-handler/README.md) | pkg-000009 |
| 3 | [`task-ids-07-01-t03-me-response-payload`](./task-ids-07-01-t03-me-response-payload/README.md) | pkg-000009 |
| 4 | [`task-ids-07-01-t04-asgi-route-wire-handle-me`](./task-ids-07-01-t04-asgi-route-wire-handle-me/README.md) | pkg-000009 |
| 5 | [`task-ids-07-01-t05-me-offline-tests`](./task-ids-07-01-t05-me-offline-tests/README.md) | pkg-000009 |
| 6 | [`task-ids-07-01-t06-story-acceptance-verification`](./task-ids-07-01-t06-story-acceptance-verification/README.md) | pkg-000009 |
| 7 | [`task-ids-07-01-t07-audit-f1-dotenv-cwd-test-isolation`](./task-ids-07-01-t07-audit-f1-dotenv-cwd-test-isolation/README.md) | pkg-000010 |
| 8 | [`task-ids-07-01-t08-audit-f2-backlog-story-status-sync`](./task-ids-07-01-t08-audit-f2-backlog-story-status-sync/README.md) | pkg-000010 |
| 9 | [`task-ids-07-01-t09-audit-f3-remove-handle-me-stub`](./task-ids-07-01-t09-audit-f3-remove-handle-me-stub/README.md) | pkg-000010 |
| 10 | [`task-ids-07-01-t10-audit-f4-basic-rights-doc-align`](./task-ids-07-01-t10-audit-f4-basic-rights-doc-align/README.md) | pkg-000010 |
| 11 | [`task-ids-07-01-t11-audit-f5-bullrun-index-factual-sync`](./task-ids-07-01-t11-audit-f5-bullrun-index-factual-sync/README.md) | pkg-000010 |
| 12 | [`task-ids-07-01-t12-audit-f6-gitignore-env`](./task-ids-07-01-t12-audit-f6-gitignore-env/README.md) | pkg-000010 |
