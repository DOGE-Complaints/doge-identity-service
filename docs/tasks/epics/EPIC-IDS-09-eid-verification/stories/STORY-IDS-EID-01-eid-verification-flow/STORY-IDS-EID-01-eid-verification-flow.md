# STORY-IDS-EID-01 — eID-флоу: старт, callback, orchestration

## Meta
- **Key:** `STORY-IDS-EID-01-eid-verification-flow`
- **Parent Epic:** [`../../../../EPIC-IDS-09-eid-verification.md`](../../../../EPIC-IDS-09-eid-verification.md)
- **Epic alias (код/backlog):** `EPIC-IDS-EID`
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/STORY-IDS-EID-01-eid-verification-flow.md`](../../../../backlog-stories/eid/STORY-IDS-EID-01-eid-verification-flow.md)
- **Decision Ref:** [`../../../../backlog-stories/STORY-IDS-EID-01-eid-verification-flow.md`](../../../../backlog-stories/eid/STORY-IDS-EID-01-eid-verification-flow.md); [`identity-todo-backlog-2026-06-04`](../../../../../analysis/identity-todo-backlog-2026-06-04.md) — A2, A3, C9, C10; paradigm anchors — [04-security §Часть A](../../../../../runtime-docs/04-security.md), [06-eid-providers](../../../../../runtime-docs/06-eid-providers.md), [05-data-model](../../../../../runtime-docs/05-data-model.md)
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../../../analysis/identity-todo-backlog-2026-06-04.md) — A2, A3, C9, C10
- **Зависит от:** [STORY-IDS-AUTHCORE-01-profile-and-me](../../../EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-01-profile-and-me/STORY-IDS-AUTHCORE-01-profile-and-me.md) (профиль, куда писать статус)

## Зачем простыми словами
Это сердце сервиса: превратить заглушки eID в рабочий процесс. Пользователь жмёт «верифицироваться» → identity создаёт сессию и редиректит к провайдеру → провайдер возвращает callback → identity ставит `eid_verified=true` в профиль и генерирует `verified_person_hash`. Инфраструктура (порт, сессии, mock) готова — нужно собрать оркестрацию.

## Scope
- Реализовать `POST /auth/eid/start`: создать сессию через активного провайдера, вернуть redirect.
- Реализовать callback'и (`/auth/mock/callback` как минимум): обработать возврат, выставить профиль, записать аудит.
- Прокинуть флаг «нужен eID» через `return_context`/`requested_action` (поля сессии уже есть).
- Привязка к пользователю — из записи сессии (`supabase_user_id`), а не из браузерной сессии (принцип session-binding).
- Генерация и конфликт `verified_person_hash` (HMAC уже есть).

## Вне scope
- Реальные провайдеры eideasy/authentigate — [STORY-IDS-EID-02](../../../../backlog-stories/STORY-IDS-EID-02-real-eid-providers.md) (на mock флоу собирается полностью).

## Точки в коде (текущее состояние)
- Заглушки: `/auth/eid/start` ([`asgi_app.py:181-195`](../../../../../../src/core/api/asgi_app.py)), callback'и ([`asgi_app.py:197-231`](../../../../../../src/core/api/asgi_app.py)).
- Готово: `EIDProviderPort`/registry/mock ([`providers/`](../../../../../../src/core/providers/)), `VerificationSessionStore` ([`contracts.py:43-53`](../../../../../../src/core/domain/contracts.py)), `hash_secret` ([`hashing.py`](../../../../../../src/core/security/hashing.py)), таблица сессий + аудит.
- Поля флага: `return_context`/`requested_action` ([`models.py:43-59`](../../../../../../src/core/domain/models.py)).

## Acceptance Criteria
- [x] `POST /auth/eid/start` (валидный JWT) → создаёт сессию `started`, отдаёт redirect к провайдеру.
- [x] callback с валидным `state` → профиль становится `eid_verified=true`, заполнены `verified_person_hash`/`eid_verified_at`.
- [x] Повторный callback / просроченная сессия → корректная обработка (не перезаписывает терминальный статус).
- [x] Конфликт `verified_person_hash` (тот же человек, другой аккаунт) → ошибка `ProfileConflictError`/409.
- [x] Каждое событие пишется в `eid_audit_events` без PII.
- [x] Полный флоу проходит на `mock` офлайн-тестом.

## Парадигма-якорь
[04-security §Часть A](../../../../../runtime-docs/04-security.md) (шаги eID), [06-eid-providers](../../../../../runtime-docs/06-eid-providers.md), [05-data-model](../../../../../runtime-docs/05-data-model.md) (sessions/profiles).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-09-01-t01-handle-auth-eid-start-orchestration`](./task-ids-09-01-t01-handle-auth-eid-start-orchestration/README.md) | pkg-000015 |
| 2 | [`task-ids-09-01-t02-asgi-eid-start-wire-body`](./task-ids-09-01-t02-asgi-eid-start-wire-body/README.md) | pkg-000015 |
| 3 | [`task-ids-09-01-t03-mock-callback-orchestration`](./task-ids-09-01-t03-mock-callback-orchestration/README.md) | pkg-000015 |
| 4 | [`task-ids-09-01-t04-session-lifecycle-audit-events`](./task-ids-09-01-t04-session-lifecycle-audit-events/README.md) | pkg-000015 |
| 5 | [`task-ids-09-01-t05-mock-eid-flow-offline-tests`](./task-ids-09-01-t05-mock-eid-flow-offline-tests/README.md) | pkg-000015 |
| 6 | [`task-ids-09-01-t06-story-acceptance-verification`](./task-ids-09-01-t06-story-acceptance-verification/README.md) | pkg-000015 |
| 7 | [`task-ids-09-01-t07-audit-f1-backlog-story-status-sync`](./task-ids-09-01-t07-audit-f1-backlog-story-status-sync/README.md) | override epic_ids_09_eid_01_audit_2026_06_06 |
