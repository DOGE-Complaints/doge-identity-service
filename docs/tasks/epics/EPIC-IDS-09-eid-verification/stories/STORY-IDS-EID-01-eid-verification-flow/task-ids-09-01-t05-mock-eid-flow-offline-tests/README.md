## Task workspace — `task-ids-09-01-t05-mock-eid-flow-offline-tests`

- Story: [`../STORY-IDS-EID-01-eid-verification-flow.md`](../STORY-IDS-EID-01-eid-verification-flow.md)
- Prerequisite: [`../task-ids-09-01-t04-session-lifecycle-audit-events/README.md`](../task-ids-09-01-t04-session-lifecycle-audit-events/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000015`  
**Skill declared:** python-pro  
---

## Task: tests — mock eID flow offline e2e

### Цель
Новый `tests/test_eid_verification_flow.py` (или расширение `test_asgi_transport.py`): start → mock callback → `GET /me` с `eid_verified=true`; conflict 409; replay/expired scenarios.

### Почему это важно
Story AC #3, #4, #6; epic §7 offline e2e.

### Факты из кода
1. [`tests/test_asgi_transport.py:77-107`](../../../../../../../tests/test_asgi_transport.py) — start transport (501 today).
2. [`tests/test_eid_providers.py`](../../../../../../../tests/test_eid_providers.py) — mock provider unit tests.
3. [`tests/conftest.py`](../../../../../../../tests/conftest.py) — `test_client`, `DB_BACKEND=in_memory`.
4. [`tests/test_me_profile.py`](../../../../../../../tests/test_me_profile.py) — `/me` assertions pattern.

### Gap / Проблема
Нет offline e2e полного mock flow; AC #6 не покрыт.

### AC/DoD
- [x] (P0) E2E: JWT → start → mock callback → `/me` shows `eid_verified=true` (AC #6).
- [x] (P0) Hash conflict scenario → 409 (AC #4).
- [x] (P0) Replay callback / expired session → no profile overwrite (AC #3).
- [x] (P0) All tests `pytest -m "not live_integration"`, in_memory backend.
- [x] (P1) Update `test_asgi_transport.py` start expectations (501 → 200).

### Где менять код
- `doge-identity-service/tests/test_eid_verification_flow.py` (new)
- `doge-identity-service/tests/test_asgi_transport.py` (optional update)

### Out of scope
- Live Supabase e2e
- Real provider callbacks — EID-02

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q tests/test_eid_verification_flow.py
```
