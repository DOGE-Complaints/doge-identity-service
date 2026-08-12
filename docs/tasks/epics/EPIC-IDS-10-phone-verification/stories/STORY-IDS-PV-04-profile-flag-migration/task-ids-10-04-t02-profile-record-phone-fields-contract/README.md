## Task workspace — `task-ids-10-04-t02-profile-record-phone-fields-contract`

- Story: [`../STORY-IDS-PV-04-profile-flag-migration.md`](../STORY-IDS-PV-04-profile-flag-migration.md)
- Prerequisite: t01 migration SQL (column names SSOT)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000025`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md) Scope bullet 2; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §4  
---

## Task: implement — `ProfileRecord` phone fields + `ProfileRepository` contract

### Цель
Расширить domain model и protocol: 5 phone-полей + `get_by_verified_phone_hash` + `attach_phone_verification` — Story Scope bullet 2.

### Почему это важно
t03/t04 реализуют attach/dedup; t05 `/me` читает поля из `ProfileRecord`. Зеркало eID [`ProfileRecord`](../../../../../../../src/core/domain/models.py:23-40) / [`ProfileRepository`](../../../../../../../src/core/domain/contracts.py:24-40).

### Факты из кода
1. `ProfileRecord` — только eID/wallet поля ([`models.py:23-40`](../../../../../../../src/core/domain/models.py)); phone_* **отсутствуют**.
2. `ProfileRepository` — `get_by_verified_person_hash`, `attach_eid_verification` ([`contracts.py:27-40`](../../../../../../../src/core/domain/contracts.py)); phone methods **отсутствуют**.
3. `ProfileRecord(...)` constructors в: `repositories.py`, `db_supabase.py`, `test_me_profile.py`, `test_db_supabase_repositories.py`, `test_supabase_identity_roundtrip.py` — потребуют новых defaults.
4. `PHONE_ONE_ACCOUNT_PER_NUMBER` в `AppConfig` ([`schema.py:236`](../../../../../../../src/core/config/schema.py)) — gated dedup через параметр `one_account_per_number: bool` на `attach_phone_verification` (PV-05 передаст config value).

### Gap / Проблема
Domain layer не знает о phone verification state; repository protocol не объявляет attach/lookup по phone hash.

### AC/DoD
- [ ] (P0) `ProfileRecord`: `phone_verified: bool`, `verified_phone_hash: str | None`, `phone_provider: str | None`, `phone_dial_prefix: str | None`, `phone_verified_at: datetime | None` (defaults: False/None).
- [ ] (P0) `ProfileRepository.get_by_verified_phone_hash(hash_: str) -> ProfileRecord | None`.
- [ ] (P0) `ProfileRepository.attach_phone_verification(user_id, *, provider, dial_prefix, verified_phone_hash, verified_at, one_account_per_number: bool) -> ProfileRecord`.
- [ ] (P1) Все существующие `ProfileRecord(...)` в `src/` и `tests/` компилируются (grep fix).
- [ ] (P1) `test_domain_contracts.py` — `ProfileRepository` structural check passes.

### Где менять код
- `doge-identity-service/src/core/domain/models.py`
- `doge-identity-service/src/core/domain/contracts.py`
- `doge-identity-service/src/core/infrastructure/repositories.py` (ProfileRecord stubs in attach_eid only — constructor args)
- `doge-identity-service/src/core/infrastructure/db_supabase.py` (`_profile_from_row` defaults until t04)
- `doge-identity-service/tests/test_me_profile.py`, `test_db_supabase_repositories.py`, `tests/integration/supabase/test_supabase_identity_roundtrip.py`

### Out of scope
- InMemory/Supabase attach implementation — t03, t04
- `/me` response — t05
- Migration SQL — t01

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_domain_contracts.py -q
.venv/bin/python -c "from core.domain.models import ProfileRecord; from core.domain.contracts import ProfileRepository; print(ProfileRecord, ProfileRepository)"
```
