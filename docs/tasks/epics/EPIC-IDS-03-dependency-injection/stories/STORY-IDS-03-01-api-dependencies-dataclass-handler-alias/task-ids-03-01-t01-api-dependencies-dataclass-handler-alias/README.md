## Task workspace — `task-ids-03-01-t01-api-dependencies-dataclass-handler-alias`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000004`  
**Decision Ref:** [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) §6 Story 1  
---

## Task: implement — ApiDependencies dataclass + HandlerDependencies alias

### Цель
Расширить `ApiDependencies` до полной frozen-структуры из EPIC-IDS-03 Story 1: обязательные поля, nine identity-слотов `object | None`, алиас `HandlerDependencies = ApiDependencies`.

### Почему это важно (риск)
Без зарезервированных слотов EPIC-IDS-04 придётся менять контракт dataclass; frozen singleton shared state требует immutable container.

### Факты из кода
1. [`src/core/api/dependencies.py:12-18`](../../../../../../../src/core/api/dependencies.py) — только `config`, `bearer_token_auth`, `db_backend`, `db_ready`, `db_checks`; нет optional identity-слотов.
2. [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py) — `HandlerDependencies` alias отсутствует.
3. [`src/core/api/__init__.py:3-6`](../../../../../../../src/core/api/__init__.py) — экспортирует `ApiDependencies`, не `HandlerDependencies`.

### Gap
Dataclass не соответствует Outputs EPIC-IDS-03 §6 Story 1 L78-101.

### AC/DoD
- [x] (P0) `from core.api.dependencies import ApiDependencies, HandlerDependencies`.
- [x] (P0) `HandlerDependencies is ApiDependencies` — True.
- [x] (P0) `ApiDependencies(config=..., bearer_token_auth=..., db_backend="in_memory", db_ready=True)` — конструируется; все identity-сервисы дефолтятся в `None`.
- [x] (P0) Попытка `deps.config = new_config` → `FrozenInstanceError`.

### Acceptance
- [acceptance-verification-task-ids-03-01-t01-api-dependencies-dataclass-handler-alias.md](./acceptance-verification-task-ids-03-01-t01-api-dependencies-dataclass-handler-alias.md) — PASS
- [BULLRUN-PHASE-LOG.md](./BULLRUN-PHASE-LOG.md)

### Где менять код
- `doge-identity-service/src/core/api/dependencies.py`
- `doge-identity-service/src/core/api/__init__.py`

### Out of scope
- `build_api_dependencies()` refactor — Story 2 t01
- `provide_service_factory()` — EPIC-IDS-04
- `tests/test_di_singleton.py` — EPIC-IDS-06

### Команды проверки
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.api.dependencies import ApiDependencies, HandlerDependencies
assert HandlerDependencies is ApiDependencies
print('imports OK')
"
```
