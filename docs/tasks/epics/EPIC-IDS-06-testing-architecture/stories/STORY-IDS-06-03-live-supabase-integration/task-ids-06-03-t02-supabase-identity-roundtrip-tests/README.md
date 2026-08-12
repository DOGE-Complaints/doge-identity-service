## Task workspace — `task-ids-06-03-t02-supabase-identity-roundtrip-tests`

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 3  
**Story:** [`../STORY-IDS-06-03-live-supabase-integration.md`](../STORY-IDS-06-03-live-supabase-integration.md)  
---

## Task: tests — live Supabase identity roundtrip

### Цель
Создать `tests/integration/supabase/test_supabase_identity_roundtrip.py` per epic §6 Story 3 Outputs L213–218 с UUID4 keys + teardown DELETE.

### Почему это важно
Проверяет реальные Supabase repositories и partial unique constraint на `verified_person_hash`.

### Факты из кода
1. [`tests/integration/supabase/test_supabase_identity_roundtrip.py`](../../../../../../../tests/integration/supabase/test_supabase_identity_roundtrip.py) — **отсутствует**.
2. [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) — `SupabaseProfileRepository`, session store, audit log adapters.
3. Epic L218 — все тесты UUID4 + teardown.

### Gap
Roundtrip live tests отсутствуют.

### AC/DoD
- [x] (P0) `test_profile_upsert_and_read` — upsert + `get_by_supabase_user_id`, cleanup.
- [x] (P0) `test_verification_session_create_and_consume` — `status="consumed"`.
- [x] (P0) `test_eid_audit_event_append` — `request_id=test-...`, cleanup DELETE.
- [x] (P0) `test_partial_unique_verified_person_hash` — второй attach → `ProfileConflictError` (или 409), cleanup.
- [x] (P1) UUID4-generated keys + teardown на всех тестах (epic L218).

### Где менять код
- `doge-identity-service/tests/integration/supabase/test_supabase_identity_roundtrip.py` (новый)

### Out of scope
- Connectivity module — t01
- CI wiring — Story 4

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/integration/supabase/test_supabase_identity_roundtrip.py -m live_integration -v
```
