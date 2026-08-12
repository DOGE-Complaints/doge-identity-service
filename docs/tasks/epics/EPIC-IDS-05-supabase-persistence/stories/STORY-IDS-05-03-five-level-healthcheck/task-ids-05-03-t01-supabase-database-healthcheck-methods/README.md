## Task workspace — `task-ids-05-03-t01-supabase-database-healthcheck-methods`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000006`  
**Decision Ref:** [`../../../../EPIC-IDS-05-supabase-persistence.md`](../../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 3  
**Story:** [`../STORY-IDS-05-03-five-level-healthcheck.md`](../STORY-IDS-05-03-five-level-healthcheck.md)  
---

## Task: implement — five-level SupabaseDatabase healthcheck methods

### Цель
Добавить на `SupabaseDatabase` методы: `healthcheck`, `required_tables_ready`, `required_columns_ready`, `provider_state_ready`, `service_role_policy_probe` (epic L128–137).

### Почему это важно
Readiness без crashloop: оператор видит `db_checks` через `/ready`; identity-таблицы отличаются от gateway.

### Факты из кода
1. Epic L131–133 — tables: `profiles`, `eid_verification_sessions`, `eid_audit_events`, `story_drafts` (не gateway tables).
2. [`src/core/api/dependencies.py:65-68`](../../../../../../../src/core/api/dependencies.py) — `# TODO EPIC-IDS-05: run 5-level Supabase healthchecks`; `db_checks = {}`.
3. [`tests/test_asgi_transport.py:119`](../../../../../../../tests/test_asgi_transport.py) — `test_ready_supabase_backend_reports_degraded` (503 until this story).
4. Epic L137 — `service_role_policy_probe` uses `eid_audit_events`, not `profiles`.

### Gap
5 healthcheck methods отсутствуют на `SupabaseDatabase`.

### AC/DoD
- [x] (P0) `healthcheck()` → GET `/rest/v1/?limit=1`; any error → False (no raise).
- [x] (P0) `required_tables_ready()` — all 4 identity tables GET `?limit=1` success.
- [x] (P0) `required_columns_ready()` — profiles select critical columns.
- [x] (P0) `provider_state_ready()` — sessions select `provider`, `provider_session_data`.
- [x] (P0) `service_role_policy_probe()` — POST dummy audit event + DELETE probe rows; RLS failure → False.
- [x] (P0) All methods: `try/except Exception: return False`.

### Где менять код
- `doge-identity-service/src/core/infrastructure/db_supabase.py`

### Out of scope
- `build_api_dependencies` wiring — [`task-ids-05-03-t02-build-api-dependencies-db-checks`](../task-ids-05-03-t02-build-api-dependencies-db-checks/README.md)

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.infrastructure.db_supabase import SupabaseDatabase
db = SupabaseDatabase.from_http('https://x.co', 'key')
for name in ('healthcheck', 'required_tables_ready', 'required_columns_ready', 'provider_state_ready', 'service_role_policy_probe'):
    assert hasattr(db, name)
print('healthcheck methods OK')
"
```
