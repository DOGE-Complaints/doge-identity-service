## Task workspace — `task-ids-05-03-t02-build-api-dependencies-db-checks`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 3  
**Story:** [`../STORY-IDS-05-03-five-level-healthcheck.md`](../STORY-IDS-05-03-five-level-healthcheck.md)  
---

## Task: implement — build_api_dependencies db_checks integration

### Цель
Обновить `build_api_dependencies()` при `db_backend == "supabase"`: заполнить `db_checks` и `db_ready` через `SupabaseDatabase` (epic L138–149); удалить TODO EPIC-IDS-05.

### Почему это важно
`/ready` и startup logs должны отражать реальное состояние Supabase; degraded mode без crashloop — intentional (epic §7).

### Факты из кода
1. [`src/core/api/dependencies.py:57-68`](../../../../../../../src/core/api/dependencies.py) — текущий stub: `db_checks = {}`, `db_ready = db_backend == "in_memory"`.
2. Epic L140–149 — exact `db_checks` keys: connectivity, schema, columns, provider_state, policy_probe.
3. [`src/core/infrastructure/providers.py:60-72`](../../../../../../../src/core/infrastructure/providers.py) — factory still InMemory fallback until Story 6.
4. [`src/core/config/schema.py:107`](../../../../../../../src/core/config/schema.py) — fail-fast if supabase backend without URL/service_role at config load.

### Gap
`build_api_dependencies` не вызывает 5-level healthchecks для supabase backend.

### AC/DoD
- [x] (P0) При `db_backend == "supabase"`: `SupabaseDatabase.from_http(config.supabase_url, config.supabase_service_role)`.
- [x] (P0) `db_checks` dict с ключами `connectivity`, `schema`, `columns`, `provider_state`, `policy_probe`.
- [x] (P0) `db_ready = all(db_checks.values())`.
- [x] (P0) Удалён комментарий `# TODO EPIC-IDS-05: run 5-level Supabase healthchecks`.
- [x] (P1) Startup log via lifespan emits `db_checks={...}` (see Story 3 AC t03).

### Где менять код
- `doge-identity-service/src/core/api/dependencies.py`

### Out of scope
- Supabase factory branch — Story 6
- Story 3 pytest — [`task-ids-05-03-t03-story3-acceptance-verification`](../task-ids-05-03-t03-story3-acceptance-verification/README.md)

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
import inspect
from core.api.dependencies import build_api_dependencies
src = inspect.getsource(build_api_dependencies)
assert 'db_checks' in src and 'connectivity' in src
print('dependencies db_checks wiring present')
"
```
