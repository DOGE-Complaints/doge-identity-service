## Task workspace — `task-ids-02-04-t01-create-app-and-lifespan`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done
**Wave:** `pkg-000003`  
---

## Task: implement — create_app(config) и lifespan bootstrap

### Цель
Собрать `create_app(config)` + module-level `app` и lifespan bootstrapping DI/logging по Story 4.

### AC/DoD
- [x] `create_app(config)` создаёт `FastAPI(title="doge-identity-service")`.
- [x] Lifespan вызывает `get_api_dependencies()` и `configure_logging(...)`.
- [x] CORS middleware добавляется при сборке app (не в runtime).

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py`

### Process
- [BULLRUN-PHASE-LOG.md](./BULLRUN-PHASE-LOG.md)
