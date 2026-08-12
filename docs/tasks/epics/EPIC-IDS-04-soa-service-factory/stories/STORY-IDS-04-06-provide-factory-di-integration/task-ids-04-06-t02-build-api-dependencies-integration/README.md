## Task workspace — `task-ids-04-06-t02-build-api-dependencies-integration`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** ready  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 6  
**Story:** [`../STORY-IDS-04-06-provide-factory-di-integration.md`](../STORY-IDS-04-06-provide-factory-di-integration.md)  
---

## Task: implement — build_api_dependencies factory integration

### Цель
Обновить [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py): `build_api_dependencies()` вызывает `provide_service_factory()` и заполняет все identity-поля; типы полей `ApiDependencies` — с `object | None` на конкретные Protocol-типы (epic L351–353).

### Почему это важно
Завершает DI-цепочку EPIC-IDS-03 → EPIC-IDS-04: singleton в `asgi_app` получает полный контейнер вместо `None`-слотов и `StubBearerTokenAuth`.

### Факты из кода
1. [`src/core/api/dependencies.py:50-71`](../../../../../../../src/core/api/dependencies.py) — текущая реализация: `StubBearerTokenAuth()`, identity-слоты не заполнены.
2. [`src/core/api/dependencies.py:73-90`](../../../../../../../src/core/api/dependencies.py) — готовый commented template для EPIC-IDS-04 integration.
3. [`src/core/api/dependencies.py:12-22`](../../../../../../../src/core/api/dependencies.py) — `EPIC_IDS_04_OPTIONAL_FIELDS` tuple для contract tests EPIC-IDS-03.
4. [`src/core/api/asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — **не менять** (epic L354: singleton hook без изменений).

### Gap
`build_api_dependencies().profile_repository is None`; bearer auth — stub.

### AC/DoD
- [ ] (P0) `build_api_dependencies().profile_repository is not None` (после EPIC-IDS-04 уже не `None`).
- [ ] (P0) `build_api_dependencies().eid_provider_registry.get("mock").provider_name == "mock"`.
- [ ] (P0) `build_api_dependencies().bearer_token_auth.__class__.__name__ == "SupabaseJwtBearerTokenAuth"`.
- [ ] (P0) Типы полей `ApiDependencies` уточнены до Protocol-типов (не `object | None`).
- [ ] (P0) `asgi_app.py` — без изменений.

### Где менять код
- `doge-identity-service/src/core/api/dependencies.py` (обновить)

### Out of scope
- `provide_service_factory` body — t01
- `asgi_app.py`, `get_api_dependencies`, `_clear_api_dependencies_cache` — EPIC-IDS-03 closed
- Epic §8 full smoke — t03
- `tests/test_di_service_factory.py` — EPIC-IDS-06

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
import os
os.environ.update({'APP_PROFILE': 'demo', 'API_BASE_URL': 'http://localhost:8100', 'DB_BACKEND': 'in_memory', 'EID_PROVIDER': 'mock'})
from core.api.dependencies import build_api_dependencies
d = build_api_dependencies()
assert d.profile_repository is not None
assert d.eid_provider_registry is not None
assert type(d.bearer_token_auth).__name__ == 'SupabaseJwtBearerTokenAuth'
print('DI integration OK')
"
```
