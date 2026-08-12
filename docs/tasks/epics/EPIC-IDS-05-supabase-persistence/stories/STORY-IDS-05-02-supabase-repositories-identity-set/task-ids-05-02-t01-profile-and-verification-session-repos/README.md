## Task workspace — `task-ids-05-02-t01-profile-and-verification-session-repos`

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 2  
**Story:** [`../STORY-IDS-05-02-supabase-repositories-identity-set.md`](../STORY-IDS-05-02-supabase-repositories-identity-set.md)  
---

## Task: implement — SupabaseProfileRepository and SupabaseVerificationSessionStore

### Цель
Добавить в `db_supabase.py` `SupabaseProfileRepository` и `SupabaseVerificationSessionStore` по epic §6 Story 2 Outputs L83–93.

### Почему это важно
Profile и eID session state — core identity persistence; без них `provide_service_factory` supabase branch неполон.

### Факты из кода
1. [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py) — `ProfileRepository`, `VerificationSessionStore` Protocols (EPIC-IDS-04).
2. [`src/core/infrastructure/repositories.py`](../../../../../../../src/core/infrastructure/repositories.py) — InMemory reference implementations для поведения.
3. [`src/core/domain/models.py`](../../../../../../../src/core/domain/models.py) — `ProfileRecord`, `VerificationSession` dataclasses.
4. Epic Outputs L83–93 — PostgREST paths для `profiles` и `eid_verification_sessions`.

### Gap
Supabase-реализации Profile и VerificationSession отсутствуют в `db_supabase.py`.

### AC/DoD
- [x] (P0) `SupabaseProfileRepository.get_by_supabase_user_id` → GET `/rest/v1/profiles?supabase_user_id=eq.{id}&limit=1`; `[]` → `None`.
- [x] (P0) `SupabaseProfileRepository.upsert` → POST + `Prefer: resolution=merge-duplicates`.
- [x] (P0) `SupabaseProfileRepository.attach_eid_verification` → PATCH; HTTP 409 → `ProfileConflictError`.
- [x] (P0) `SupabaseVerificationSessionStore.create` → POST с `provider`, `provider_session_data`.
- [x] (P0) Session store: `get_by_state`, `mark_consumed`, `mark_failed`, `expire_pending` per epic L88–93.

### Где менять код
- `doge-identity-service/src/core/infrastructure/db_supabase.py`

### Out of scope
- Audit/OAuth/Draft/Health repos — [`task-ids-05-02-t02-audit-oauth-story-health-repos`](../task-ids-05-02-t02-audit-oauth-story-health-repos/README.md)
- Story 2 pytest — [`task-ids-05-02-t03-story2-acceptance-verification`](../task-ids-05-02-t03-story2-acceptance-verification/README.md)

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.infrastructure.db_supabase import SupabaseDatabase, SupabaseProfileRepository, SupabaseVerificationSessionStore
db = SupabaseDatabase.from_http('https://x.co', 'key')
assert SupabaseProfileRepository(db) and SupabaseVerificationSessionStore(db)
print('profile/session repos OK')
"
```
