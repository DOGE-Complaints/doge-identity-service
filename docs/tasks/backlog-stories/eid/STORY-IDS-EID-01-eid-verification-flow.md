# STORY-IDS-EID-01 — eID-флоу: старт, callback, orchestration

## Meta
- **Key:** `STORY-IDS-EID-01-eid-verification-flow`
- **Epic:** `EPIC-IDS-09` (alias в коде: `EPIC-IDS-EID`)
- **Status:** 🟢 Done
- **Источник:** backlog [`identity-todo-backlog-2026-06-04`](../../../analysis/identity-todo-backlog-2026-06-04.md) — A2, A3, C9, C10
- **Исполнение:** [pipeline story](../../epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-01-eid-verification-flow/STORY-IDS-EID-01-eid-verification-flow.md) + pkg-000015 (2026-06-06)
- **Зависит от:** [STORY-IDS-AUTHCORE-01](../auth-core/STORY-IDS-AUTHCORE-01-profile-and-me.md) (профиль, куда писать статус)

## Зачем простыми словами
Это сердце сервиса: превратить заглушки eID в рабочий процесс. Пользователь жмёт «верифицироваться» → identity создаёт сессию и редиректит к провайдеру → провайдер возвращает callback → identity ставит `eid_verified=true` в профиль и генерирует `verified_person_hash`. Инфраструктура (порт, сессии, mock) готова — нужно собрать оркестрацию.

## Scope
- Реализовать `POST /auth/eid/start`: создать сессию через активного провайдера, вернуть redirect.
- Реализовать callback'и (`/auth/mock/callback` как минимум): обработать возврат, выставить профиль, записать аудит.
- Прокинуть флаг «нужен eID» через `return_context`/`requested_action` (поля сессии уже есть).
- Привязка к пользователю — из записи сессии (`supabase_user_id`), а не из браузерной сессии (принцип session-binding).
- Генерация и конфликт `verified_person_hash` (HMAC уже есть).

## Вне scope
- Реальные провайдеры eideasy/authentigate — [STORY-IDS-EID-02](../eid-deferred/STORY-IDS-EID-02-real-eid-providers.md) (на mock флоу собирается полностью).

## Точки в коде (текущее состояние)
- Start: [`asgi_app.py`](../../../../src/core/api/asgi_app.py) → `handle_auth_eid_start` ([`handlers.py:114`](../../../../src/core/api/handlers.py)) → 200 + redirect.
- Mock callback: [`asgi_app.py`](../../../../src/core/api/asgi_app.py) → `handle_auth_eid_callback` ([`handlers.py:189`](../../../../src/core/api/handlers.py)).
- Тесты: [`test_eid_verification_flow.py`](../../../../tests/test_eid_verification_flow.py).
- Готово: `EIDProviderPort`/registry/mock ([`providers/`](../../../../src/core/providers/)), `VerificationSessionStore` ([`contracts.py:43-53`](../../../../src/core/domain/contracts.py)), `hash_secret` ([`hashing.py`](../../../../src/core/security/hashing.py)), таблица сессий + аудит.
- Поля флага: `return_context`/`requested_action` ([`models.py:43-59`](../../../../src/core/domain/models.py)).

## Acceptance Criteria
- [x] `POST /auth/eid/start` (валидный JWT) → создаёт сессию `started`, отдаёт redirect к провайдеру.
- [x] callback с валидным `state` → профиль становится `eid_verified=true`, заполнены `verified_person_hash`/`eid_verified_at`.
- [x] Повторный callback / просроченная сессия → корректная обработка (не перезаписывает терминальный статус).
- [x] Конфликт `verified_person_hash` (тот же человек, другой аккаунт) → ошибка `ProfileConflictError`/409.
- [x] Каждое событие пишется в `eid_audit_events` без PII.
- [x] Полный флоу проходит на `mock` офлайн-тестом.

## Парадигма-якорь
[04-security §Часть A](../../../runtime-docs/04-security.md) (шаги eID), [06-eid-providers](../../../runtime-docs/06-eid-providers.md), [05-data-model](../../../runtime-docs/05-data-model.md) (sessions/profiles).
