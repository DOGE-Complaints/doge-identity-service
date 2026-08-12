## Task workspace — `task-ids-05-02-t02-audit-oauth-story-health-repos`

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 2  
**Story:** [`../STORY-IDS-05-02-supabase-repositories-identity-set.md`](../STORY-IDS-05-02-supabase-repositories-identity-set.md)  
---

## Task: implement — audit, OAuth, story draft, health repos and JSONB helper

### Цель
Добавить в `db_supabase.py`: `SupabaseEIDAuditLogRepository`, `SupabaseOAuthClientStore`, `SupabaseStoryDraftRepository`, `SupabaseHealthRepository`, `_jsonb_normalize` (epic L94–113).

### Почему это важно
`SupabaseHealthRepository` обязателен для factory (audit C-2); без него Story 6 упадёт с `NameError`. JSONB normalize предотвращает `str` в domain models.

### Факты из кода
1. Epic L99–110 — `SupabaseHealthRepository.ping()` делегирует `db.healthcheck()` (healthcheck methods добавляются в Story 3 t01; stub или forward ref допустим до t01).
2. [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py) — `EIDAuditLogRepository`, `OAuthClientStore`, `StoryDraftRepository`, `HealthRepository`.
3. [`src/core/infrastructure/repositories.py`](../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryOAuthClientStore.from_config` MVP pattern.
4. Epic L112 — `_jsonb_normalize(row, fields)` для PostgREST JSONB-as-str.

### Gap
Оставшиеся Supabase repository classes и JSONB helper отсутствуют.

### AC/DoD
- [x] (P0) `SupabaseEIDAuditLogRepository`: `log_event` POST append-only; `list_events` GET с filters + order/limit.
- [x] (P0) `SupabaseOAuthClientStore`: read-only MVP from env (`gpt_oauth_client_id` via `fallback_config`).
- [x] (P0) `SupabaseStoryDraftRepository`: CRUD по `story_drafts` (req-15 fields).
- [x] (P0) `SupabaseHealthRepository(db).ping()` → `db.healthcheck()`; satisfies `HealthRepository` Protocol.
- [x] (P0) `_jsonb_normalize`: JSONB fields always `dict`/`list`, never bare `str`.

### Где менять код
- `doge-identity-service/src/core/infrastructure/db_supabase.py`

### Out of scope
- Profile/session repos — [`task-ids-05-02-t01-profile-and-verification-session-repos`](../task-ids-05-02-t01-profile-and-verification-session-repos/README.md)
- Dynamic `oauth_clients` table — epic Open Question L97

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.domain.contracts import HealthRepository
from core.infrastructure.db_supabase import SupabaseDatabase, SupabaseHealthRepository
db = SupabaseDatabase.from_http('https://x.co', 'key')
assert isinstance(SupabaseHealthRepository(db), HealthRepository)
print('health repo protocol OK')
"
```
