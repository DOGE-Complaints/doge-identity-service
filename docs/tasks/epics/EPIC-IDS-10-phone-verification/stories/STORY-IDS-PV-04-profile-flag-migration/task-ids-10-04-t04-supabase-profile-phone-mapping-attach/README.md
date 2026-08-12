## Task workspace — `task-ids-10-04-t04-supabase-profile-phone-mapping-attach`

- Story: [`../STORY-IDS-PV-04-profile-flag-migration.md`](../STORY-IDS-PV-04-profile-flag-migration.md)
- Prerequisite: t01 migration + t02 contract

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000025`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md) Scope bullets 2–3; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §4  
---

## Task: implement — Supabase profile row mapping + phone attach

### Цель
Расширить `_profile_to_row` / `_profile_from_row` и `SupabaseProfileRepository` phone methods — Story Scope §репозиторий (Supabase слой).

### Почему это важно
Story AC #2, #3 на persistence path; зеркало [`SupabaseProfileRepository.attach_eid_verification`](../../../../../../../src/core/infrastructure/db_supabase.py:387-419) (409 → `ProfileConflictError`).

### Факты из кода
1. Row mapping: [`_profile_to_row`](../../../../../../../src/core/infrastructure/db_supabase.py:89-108), [`_profile_from_row`](../../../../../../../src/core/infrastructure/db_supabase.py:111-132) — phone columns **отсутствуют**.
2. eID attach 409 handling: [`test_profile_attach_eid_verification_maps_409_to_profile_conflict_error`](../../../../../../../tests/test_db_supabase_repositories.py:96).
3. `get_by_verified_person_hash` REST filter pattern: [`db_supabase.py:366-373`](../../../../../../../src/core/infrastructure/db_supabase.py).

### Gap / Проблема
Supabase layer не сериализует phone fields и не реализует attach/lookup для phone hash.

### AC/DoD
- [ ] (P0) `_profile_to_row` / `_profile_from_row` include all 5 phone fields.
- [ ] (P0) `get_by_verified_phone_hash` — GET `/rest/v1/profiles?verified_phone_hash=eq.{hash}`.
- [ ] (P0) `attach_phone_verification` — PATCH body with phone fields; HTTP 409 → `ProfileConflictError`.
- [ ] (P0) Gated dedup: при `one_account_per_number=True` pre-check via `get_by_verified_phone_hash` OR rely on DB unique index + 409 (mirror eID approach).
- [ ] (P1) `test_db_supabase_repositories.py` — phone attach success + 409 conflict mock.

### Где менять код
- `doge-identity-service/src/core/infrastructure/db_supabase.py`
- `doge-identity-service/tests/test_db_supabase_repositories.py`

### Out of scope
- InMemory impl — t03
- `/me` — t05
- Live Supabase integration — `live_integration` marker

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_db_supabase_repositories.py -q -k phone
```
