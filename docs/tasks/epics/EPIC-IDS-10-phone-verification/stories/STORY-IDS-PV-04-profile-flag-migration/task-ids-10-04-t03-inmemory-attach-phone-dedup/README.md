## Task workspace — `task-ids-10-04-t03-inmemory-attach-phone-dedup`

- Story: [`../STORY-IDS-PV-04-profile-flag-migration.md`](../STORY-IDS-PV-04-profile-flag-migration.md)
- Prerequisite: t02 `ProfileRecord` + contract

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000025`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md) Scope bullets 2–3; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §10.1 (P1)  
---

## Task: implement — `InMemoryProfileRepository` phone attach + dedup

### Цель
Реализовать `get_by_verified_phone_hash` и `attach_phone_verification` в in-memory repo с gated dedup — Story Scope bullets 2–3.

### Почему это важно
Story AC #2 (attach sets flags) и AC #3 (dedup → `ProfileConflictError`); offline-first тесты без Supabase. Зеркало [`attach_eid_verification`](../../../../../../../src/core/infrastructure/repositories.py:85-139).

### Факты из кода
1. InMemory eID dedup: `_by_verified_hash` dict + conflict in `attach_eid_verification` ([`repositories.py:57-139`](../../../../../../../src/core/infrastructure/repositories.py)).
2. eID dedup test: [`test_attach_eid_verification_enforces_unique_verified_person_hash`](../../../../../../../tests/test_inmemory_repositories.py:114).
3. `ProfileConflictError`: [`models.py:11`](../../../../../../../src/core/domain/models.py).
4. `one_account_per_number` — когда `False`, dedup skip (story: «при `PHONE_ONE_ACCOUNT_PER_NUMBER=true`»).

### Gap / Проблема
InMemory repo не умеет attach phone verification и lookup по `verified_phone_hash`.

### AC/DoD
- [ ] (P0) `_by_verified_phone_hash: dict[str, str]` (hash → supabase_user_id), maintained on upsert/attach.
- [ ] (P0) `get_by_verified_phone_hash` — зеркало `get_by_verified_person_hash`.
- [ ] (P0) `attach_phone_verification` sets `phone_verified=True`, `verified_phone_hash`, `phone_provider`, `phone_dial_prefix`, `phone_verified_at`, `updated_at` — Story AC #2.
- [ ] (P0) При `one_account_per_number=True` и hash bound to other user → `ProfileConflictError` — Story AC #3.
- [ ] (P0) При `one_account_per_number=False` — повтор hash на другом user **разрешён** (no conflict).
- [ ] (P1) Tests: success attach + dedup conflict in `test_inmemory_repositories.py`.

### Где менять код
- `doge-identity-service/src/core/infrastructure/repositories.py` (`InMemoryProfileRepository`)
- `doge-identity-service/tests/test_inmemory_repositories.py`

### Out of scope
- Supabase repo — t04
- `/me` — t05
- HTTP 409 mapping — PV-05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_inmemory_repositories.py -q -k phone
```
