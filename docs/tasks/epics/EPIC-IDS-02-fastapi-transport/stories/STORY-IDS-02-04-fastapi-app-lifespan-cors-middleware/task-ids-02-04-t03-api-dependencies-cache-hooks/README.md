## Task workspace — `task-ids-02-04-t03-api-dependencies-cache-hooks`

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done
**Wave:** `pkg-000003`  
---

## Task: implement — dependency cache hooks для transport слоя

### Цель
Подготовить `_cached_dependencies`, `_clear_api_dependencies_cache`, `get_api_dependencies` для минимального DI bootstrap (до EPIC-IDS-03).

### AC/DoD
- [x] Реализован `@lru_cache(maxsize=1)` кэш dependencies.
- [x] Есть hook очистки cache для тестов.
- [x] `get_api_dependencies()` используется в lifespan.

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py`
- `doge-identity-service/src/core/api/__init__.py`

### Process
- [BULLRUN-PHASE-LOG.md](./BULLRUN-PHASE-LOG.md)
