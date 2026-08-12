## Task workspace — `task-ids-03-02-t02-asgi-singleton-lifespan-integration`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000004`  
**Decision Ref:** [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) §6 Story 2 Outputs L141-147  
---

## Task: refactor — asgi singleton cache + lifespan warmup

### Цель
Интегрировать zero-arg `build_api_dependencies()` в `asgi_app.py`: `_cached_dependencies()` → `build_api_dependencies()`, убрать `_config_for_dependencies` hook, сохранить lifespan warmup + logging.

### Факты из кода
1. [`src/core/api/asgi_app.py:48-59`](../../../../../../../src/core/api/asgi_app.py) — `@lru_cache`, `get_api_dependencies`, `_clear_api_dependencies_cache` уже есть.
2. [`src/core/api/asgi_app.py:25,50,63-65`](../../../../../../../src/core/api/asgi_app.py) — `_config_for_dependencies` передаёт config в factory (IDS-02 test pattern).
3. [`src/core/api/asgi_app.py:85-90`](../../../../../../../src/core/api/asgi_app.py) — `_lifespan` вызывает `get_api_dependencies()` + `configure_logging`.
4. Epic: CORS в `create_app(config)`, не в lifespan — [`../../../../EPIC-IDS-03-dependency-injection.md`](../../../../EPIC-IDS-03-dependency-injection.md) L146.

### Gap
`_cached_dependencies` вызывает `build_api_dependencies(config)` вместо zero-arg factory из эпика.

### AC/DoD
Prerequisite для Story 2 AC (singleton/lifespan):
- [x] (P0) `@lru_cache(maxsize=1) def _cached_dependencies() -> ApiDependencies: return build_api_dependencies()`.
- [x] (P0) `_clear_api_dependencies_cache()` → `_cached_dependencies.cache_clear()`.
- [x] (P0) `_lifespan`: `deps = get_api_dependencies(); configure_logging(...)` — без CORS.
- [x] (P0) Экспорт `build_api_dependencies` из `core.api.__init__`.

### Acceptance
- [acceptance-verification-task-ids-03-02-t02-asgi-singleton-lifespan-integration.md](./acceptance-verification-task-ids-03-02-t02-asgi-singleton-lifespan-integration.md) — PASS
- [BULLRUN-PHASE-LOG.md](./BULLRUN-PHASE-LOG.md)

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py`
- `doge-identity-service/src/core/api/__init__.py`

### Out of scope
- Factory body — t01
- Singleton pytest — t03
- `tests/test_di_singleton.py` — EPIC-IDS-06

### Команды проверки
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.api.asgi_app import get_api_dependencies, _clear_api_dependencies_cache
_clear_api_dependencies_cache()
d1 = get_api_dependencies()
d2 = get_api_dependencies()
assert d1 is d2, 'must be singleton'
print('singleton OK')
"
```
