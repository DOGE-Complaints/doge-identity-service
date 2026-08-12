## Task workspace — `task-ids-05-01-t01-supabase-database-http-client`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 1  
**Story:** [`../STORY-IDS-05-01-supabase-database-http-client.md`](../STORY-IDS-05-01-supabase-database-http-client.md)  
---

## Task: implement — SupabaseDatabase HTTP client

### Цель
Создать `src/core/infrastructure/db_supabase.py` с `@dataclass(frozen=True) class SupabaseDatabase`: `from_http`, `_headers`, `_request`, PostgREST filter cheat sheet в docstring модуля (epic §6 Story 1 Outputs L63–68).

### Почему это важно
Все Supabase-репозитории и healthchecks зависят от единого PostgREST-клиента; без него EPIC-IDS-05 не может заменить InMemory fallback.

### Факты из кода
1. [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) — **отсутствует** (glob 0 files).
2. [`src/core/infrastructure/providers.py:60-72`](../../../../../../../src/core/infrastructure/providers.py) — `DB_BACKEND=supabase` fallback на InMemory + warning `(EPIC-IDS-05)`.
3. [`src/core/domain/contracts.py`](../../../../../../../src/core/domain/contracts.py) — Protocols готовы (EPIC-IDS-04); реализации ждут этот модуль.
4. Паттерн — [`docs/tech-requirements/impl-epic-05-supabase-persistence.md`](../../../../../../../docs/tech-requirements/impl-epic-05-supabase-persistence.md) §Story 1 Task 1.1.

### Gap
Epic §6 Story 1 Outputs L63–68 не реализованы; `SupabaseDatabase` отсутствует.

### AC/DoD
- [x] (P0) `SupabaseDatabase.from_http("", "key")` → `ValueError`.
- [x] (P0) `from_http` нормализует `base_url` (без trailing slash).
- [x] (P0) `_headers()`: `apikey` + `Authorization: Bearer` + `Content-Type: application/json` + опциональный `Prefer`.
- [x] (P0) `_request`: `httpx.Client`, `raise_for_status()`, JSON или `None` при пустом теле; при 5xx — `logger.error` + `httpx.HTTPError`.
- [x] (P1) Docstring модуля содержит PostgREST filter cheat sheet (`eq.`, `in.()`, `is.null`, `gt.`, `lt.`).

### Где менять код
- `doge-identity-service/src/core/infrastructure/db_supabase.py` (новый)

### Out of scope
- Репозитории — [`task-ids-05-02-t01-profile-and-verification-session-repos`](../../STORY-IDS-05-02-supabase-repositories-identity-set/task-ids-05-02-t01-profile-and-verification-session-repos/README.md)
- pytest AC Story 1 — [`task-ids-05-01-t02-story1-acceptance-verification`](../task-ids-05-01-t02-story1-acceptance-verification/README.md)

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.infrastructure.db_supabase import SupabaseDatabase
db = SupabaseDatabase.from_http('https://x.co/', 'key')
assert db.base_url == 'https://x.co'
print('SupabaseDatabase import OK')
"
```
