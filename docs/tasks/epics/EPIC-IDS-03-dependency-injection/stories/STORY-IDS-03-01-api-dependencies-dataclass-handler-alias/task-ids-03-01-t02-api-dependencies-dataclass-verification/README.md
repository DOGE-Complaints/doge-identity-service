## Task workspace — `task-ids-03-01-t02-api-dependencies-dataclass-verification`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000004`  
**Decision Ref:** [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) §6 Story 1, §8 steps 1, 4  
---

## Task: tests — ApiDependencies dataclass acceptance

### Цель
Добавить pytest-покрытие всех AC Story 1: imports, alias, default `None` для identity-слотов, `FrozenInstanceError`.

### Факты из кода
1. Story 1 AC — [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) L104-108.
2. Epic §8 step 4 (frozen) — [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) L234-245.
3. [`tests/test_di_singleton.py`](../../../../../../../tests/test_di_singleton.py) — **не создавать** (target EPIC-IDS-06, epic §5 L68).

### Gap
Нет `tests/test_api_dependencies.py` с dataclass AC.

### AC/DoD
- [x] (P0) `from core.api.dependencies import ApiDependencies, HandlerDependencies`.
- [x] (P0) `HandlerDependencies is ApiDependencies` — True.
- [x] (P0) `ApiDependencies(config=..., bearer_token_auth=..., db_backend="in_memory", db_ready=True)` — конструируется; все identity-сервисы дефолтятся в `None`.
- [x] (P0) Попытка `deps.config = new_config` → `FrozenInstanceError`.

### Acceptance
- [acceptance-verification-task-ids-03-01-t02-api-dependencies-dataclass-verification.md](./acceptance-verification-task-ids-03-01-t02-api-dependencies-dataclass-verification.md) — PASS
- [BULLRUN-PHASE-LOG.md](./BULLRUN-PHASE-LOG.md)

### Где менять код
- `doge-identity-service/tests/test_api_dependencies.py` (новый)

### Out of scope
- Singleton / lifespan tests — Story 2 t03
- `tests/test_di_singleton.py` — EPIC-IDS-06

### Команды проверки
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_api_dependencies.py -q
python3.11 -c "
from dataclasses import FrozenInstanceError
from core.api.asgi_app import get_api_dependencies, _clear_api_dependencies_cache
_clear_api_dependencies_cache()
d = get_api_dependencies()
try:
    d.db_backend = 'x'
    assert False
except FrozenInstanceError:
    print('frozen OK')
"
```
