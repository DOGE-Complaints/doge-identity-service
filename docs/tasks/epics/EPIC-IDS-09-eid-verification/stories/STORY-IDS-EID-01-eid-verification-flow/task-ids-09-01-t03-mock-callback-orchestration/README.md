## Task workspace — `task-ids-09-01-t03-mock-callback-orchestration`

- Story: [`../STORY-IDS-EID-01-eid-verification-flow.md`](../STORY-IDS-EID-01-eid-verification-flow.md)
- Prerequisite: [`../task-ids-09-01-t01-handle-auth-eid-start-orchestration/README.md`](../task-ids-09-01-t01-handle-auth-eid-start-orchestration/README.md)

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** done  
**Wave:** `pkg-000015`  
**Skill declared:** python-pro  
---

## Task: implement — mock callback orchestration (session-binding, hash, profile)

### Цель
Реализовать обработку `GET /auth/mock/callback`: resolve session by `state`, `handle_callback` mock provider, `hash_secret` + `profile_repository.attach_eid_verification`; session-binding по `supabase_user_id` из сессии (не из JWT); `ProfileConflictError` → 409.

### Почему это важно
Story Scope: callback mock, session-binding, hash; AC #2, #4.

### Факты из кода
1. [`asgi_app.py:221-231`](../../../../../../../src/core/api/asgi_app.py) — mock callback → `handle_public_stub` 501.
2. [`providers/mock/mock_provider.py`](../../../../../../../src/core/providers/mock/mock_provider.py) — `handle_callback` возвращает verified identity payload.
3. [`contracts.py:43-52`](../../../../../../../src/core/domain/contracts.py) — `VerificationSessionStore` get/update lifecycle.
4. [`repositories.py:83-97`](../../../../../../../src/core/infrastructure/repositories.py) — `attach_eid_verification`; conflict → `ProfileConflictError`.
5. [`db_supabase.py:416`](../../../../../../../src/core/infrastructure/db_supabase.py) — Supabase unique constraint → `ProfileConflictError`.
6. [`hashing.py:9-11`](../../../../../../../src/core/security/hashing.py) — `hash_secret(value, deps.config.eid_secret)`.
7. [`tests/test_eid_providers.py`](../../../../../../../tests/test_eid_providers.py), [`tests/test_inmemory_repositories.py`](../../../../../../../tests/test_inmemory_repositories.py) — unit coverage mock + attach hash.

### Gap / Проблема
Нет callback handler; profile не обновляется после mock return.

### AC/DoD
- [x] (P0) Handler resolve session по callback `state` или `session_id`; user из session record (session-binding).
- [x] (P0) Успешный callback → `eid_verified=true`, `verified_person_hash`, `eid_verified_at` (AC #2).
- [x] (P0) `ProfileConflictError` → HTTP 409 с envelope error (AC #4).
- [x] (P0) HMAC через `hash_secret` + `config.eid_secret` (story Scope).
- [x] (P1) Inline в `handlers.py` — `handle_auth_eid_callback`.

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`
- `doge-identity-service/src/core/api/asgi_app.py` (wire mock callback route)

### Out of scope
- Session terminal states / replay / expired — t04
- Audit events полного lifecycle — t04
- eideasy/authentigate callbacks — [STORY-IDS-EID-02](../../../../../../backlog-stories/STORY-IDS-EID-02-real-eid-providers.md)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q tests/test_eid_providers.py tests/test_inmemory_repositories.py
```
