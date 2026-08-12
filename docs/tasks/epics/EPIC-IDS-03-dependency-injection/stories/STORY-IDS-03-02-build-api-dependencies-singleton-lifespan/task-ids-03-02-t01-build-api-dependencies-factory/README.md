## Task workspace — `task-ids-03-02-t01-build-api-dependencies-factory`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000004`  
**Decision Ref:** [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) §6 Story 2  
---

## Task: refactor — build_api_dependencies factory

### Цель
Привести `build_api_dependencies()` к контракту EPIC-IDS-03 Story 2: zero-arg factory, `provide_app_config()` внутри, `StubBearerTokenAuth`, `db_checks` + TODO EPIC-IDS-05.

### Почему это важно (риск)
IDS-02 stub принимает `config: AppConfig` аргументом; эпик требует env-driven factory для singleton per process.

### Факты из кода
1. [`src/core/api/dependencies.py:21-32`](../../../../../../../src/core/api/dependencies.py) — `build_api_dependencies(config: AppConfig)` с `db_ready = db_backend == "in_memory"`.
2. Epic Story 2 Outputs — [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) L116-139: `db_ready = True`, `# TODO EPIC-IDS-05`.
3. [`tests/test_asgi_transport.py`](../../../../../../../tests/test_asgi_transport.py) — `test_ready_supabase_backend_reports_degraded` ожидает 503 при supabase (IDS-02).
4. Epic §9 Open Questions — degraded ready при `db_backend=supabase` ([`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) L253-254).

### Gap
Сигнатура factory и логика `db_ready` не совпадают с epic Outputs; конфликт с IDS-02 — зафиксировать при P3, не менять формулировки AC эпика.

### AC/DoD
Зависит от Story 2 (factory — prerequisite для singleton AC):
- [x] (P0) `build_api_dependencies()` без аргумента; внутри `provide_app_config()`.
- [x] (P0) Возвращает `ApiDependencies` с `StubBearerTokenAuth`, identity-слоты `None`.
- [x] (P1) `# TODO EPIC-IDS-05: run 5-level Supabase healthchecks` над инициализацией `db_checks`.

### Acceptance
- [acceptance-verification-task-ids-03-02-t01-build-api-dependencies-factory.md](./acceptance-verification-task-ids-03-02-t01-build-api-dependencies-factory.md) — PASS
- [BULLRUN-PHASE-LOG.md](./BULLRUN-PHASE-LOG.md)

### Где менять код
- `doge-identity-service/src/core/api/dependencies.py`

### Out of scope
- `@lru_cache` / asgi wiring — t02
- TODO EPIC-IDS-04 block — Story 3 t01
- Реальный `provide_service_factory()` — EPIC-IDS-04

### Команды проверки
```bash
cd doge-identity-service && .venv/bin/python -c "
import os
os.environ.update({'APP_PROFILE': 'demo', 'API_BASE_URL': 'http://localhost:8100', 'DB_BACKEND': 'in_memory', 'EID_PROVIDER': 'mock'})
from core.api.dependencies import build_api_dependencies
d = build_api_dependencies()
print('db_backend:', d.db_backend)
print('db_ready:', d.db_ready)
print('profile_repository:', d.profile_repository)
"
```
