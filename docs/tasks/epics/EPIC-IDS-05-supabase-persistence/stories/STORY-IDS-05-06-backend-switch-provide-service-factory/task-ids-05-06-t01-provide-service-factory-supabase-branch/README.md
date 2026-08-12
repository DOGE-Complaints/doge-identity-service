## Task workspace — `task-ids-05-06-t01-provide-service-factory-supabase-branch`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 6  
**Story:** [`../STORY-IDS-05-06-backend-switch-provide-service-factory.md`](../STORY-IDS-05-06-backend-switch-provide-service-factory.md)  
---

## Task: implement — provide_service_factory supabase branch

### Цель
Заменить InMemory fallback в [`providers.py`](../../../../../../../src/core/infrastructure/providers.py) L60–72 на реальную композицию Supabase repos (epic L210–225).

### Почему это важно
Финальный шаг EPIC-IDS-05: `DB_BACKEND=supabase` должен использовать PostgREST repositories, не demo InMemory.

### Факты из кода
1. [`src/core/infrastructure/providers.py:60-72`](../../../../../../../src/core/infrastructure/providers.py) — текущий warning + InMemory fallback.
2. Epic L212–225 — exact composition block with `ValueError` without creds.
3. [`tests/test_epic_ids_04_integration.py:100-110`](../../../../../../../tests/test_epic_ids_04_integration.py) — expects fallback until EPIC-IDS-05 (migrate in t02).
4. Stories 1–3 — supply `SupabaseDatabase` + repository classes.

### Gap
`provide_service_factory` не инстанцирует Supabase repositories.

### AC/DoD
- [x] (P0) `elif db_backend == "supabase"`: raise `ValueError` if missing `supabase_url` or `supabase_service_role`.
- [x] (P0) `SupabaseDatabase.from_http` with `timeout_s=float(resolved_config.request_timeout_s or 15)`.
- [x] (P0) Wire: Profile, VerificationSession, Audit, Health, OAuthClient, StoryDraft repositories per epic L220–225.
- [x] (P0) `oauth_token_service`, `bearer_token_auth`, `eid_provider_registry` unchanged (backend-agnostic).

### Где менять код
- `doge-identity-service/src/core/infrastructure/providers.py`

### Out of scope
- Test migration — [`task-ids-05-06-t02-supabase-fallback-test-migration`](../task-ids-05-06-t02-supabase-fallback-test-migration/README.md)

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
import inspect
from core.infrastructure import providers
src = inspect.getsource(providers.provide_service_factory)
assert 'SupabaseProfileRepository' in src
assert 'falling back to InMemory' not in src
print('supabase branch OK')
"
```
