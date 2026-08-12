## Task workspace — `task-ids-06-03-t01-supabase-connectivity-health-tests`

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** done  
**Wave:** `pkg-000008`  
**Decision Ref:** [`../../../../EPIC-IDS-06-testing-architecture.md`](../../../../EPIC-IDS-06-testing-architecture.md) §6 Story 3  
**Story:** [`../STORY-IDS-06-03-live-supabase-integration.md`](../STORY-IDS-06-03-live-supabase-integration.md)  
---

## Task: tests — live Supabase connectivity and health probes

### Цель
Реализовать `tests/integration/supabase/__init__.py`, helper `_require_supabase_creds_from_dotenv()`, `test_supabase_dotenv_connectivity.py` per epic §6 Story 3 Outputs L205–212.

### Почему это важно
Live integration проверяет реальный тестовый Supabase; без creds — skip, не fail (epic Story 3 Why L200).

### Факты из кода
1. [`tests/integration/supabase/.gitkeep`](../../../../../../../tests/integration/supabase/.gitkeep) — нет `.py` тестов.
2. [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) — `healthcheck`, `required_tables_ready`, `required_columns_ready`, `provider_state_ready`, `service_role_policy_probe`.
3. [`tests/test_db_supabase_healthcheck.py`](../../../../../../../tests/test_db_supabase_healthcheck.py) — unit/mocked; **не** live dotenv path.
4. [`docs/runbook/supabase-project-setup.md`](../../../../../../../docs/runbook/supabase-project-setup.md) — test project setup (IDS-05).

### Gap
Epic Outputs L205–212 не реализованы под `tests/integration/supabase/`.

### AC/DoD
- [x] (P0) `_require_supabase_creds_from_dotenv()` парсит `.env` напрямую (минуя `_block_dotenv_leakage`).
- [x] (P0) `test_supabase_connectivity` — `db.healthcheck() is True`.
- [x] (P0) `test_supabase_identity_tables_ready` — `profiles`, `eid_verification_sessions`, `eid_audit_events`, `story_drafts`.
- [x] (P0) `test_supabase_identity_columns_ready`.
- [x] (P0) `test_supabase_provider_state_ready`.
- [x] (P0) `test_supabase_service_role_policy`.

### Где менять код
- `doge-identity-service/tests/integration/supabase/__init__.py`
- `doge-identity-service/tests/integration/supabase/test_supabase_dotenv_connectivity.py` (новый; helper в том же модуле или `conftest.py` в каталоге)

### Out of scope
- Roundtrip repository tests — [`task-ids-06-03-t02-supabase-identity-roundtrip-tests`](../task-ids-06-03-t02-supabase-identity-roundtrip-tests/README.md)
- Story 3 acceptance — t03

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/integration/supabase/test_supabase_dotenv_connectivity.py -m live_integration -v
```
