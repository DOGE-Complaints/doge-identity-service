## Task workspace — `task-ids-04-06-t01-provide-service-factory`

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** ready  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 6  
**Story:** [`../STORY-IDS-04-06-provide-factory-di-integration.md`](../STORY-IDS-04-06-provide-factory-di-integration.md)  
---

## Task: implement — provide_service_factory

### Цель
Создать `src/core/infrastructure/providers.py` с `provide_service_factory(config)` по epic L304–349: сборка InMemory repos, OAuth token service, JWT auth, eID registry с mock, `DefaultServiceFactory` return; supabase branch — fallback + warning + TODO EPIC-IDS-05.

### Почему это важно
Единственная точка выбора backend по `DB_BACKEND`. Все остальные модули не должны знать про in_memory vs supabase.

### Факты из кода
1. [`src/core/infrastructure/providers.py`](../../../../../../../src/core/infrastructure/providers.py) — **отсутствует**.
2. [`src/core/api/dependencies.py:63-90`](../../../../../../../src/core/api/dependencies.py) — TODO + commented `provide_service_factory` block с полным mapping `get_*()`.
3. [`src/core/security/hashing.py`](../../../../../../../src/core/security/hashing.py) — используется в `InMemoryOAuthClientStore.from_config`.
4. Epic §7: при `DB_BACKEND=supabase` без EPIC-IDS-05 — fallback InMemory + warning, **не raise**.

### Gap
Нет `provide_service_factory()`; factory wiring не собран.

### AC/DoD
- [ ] (P0) `provide_service_factory()` при `DB_BACKEND=in_memory` возвращает `DefaultServiceFactory` с InMemory-репозиториями.
- [ ] (P0) `provide_service_factory(config_with_supabase)` — fallback на InMemory + warning (до EPIC-IDS-05), не падает.
- [ ] (P0) OAuth token service, JWT validator, mock registry собираются по epic L323–335.
- [ ] (P0) Unsupported `db_backend` → `ValueError`.

### Где менять код
- `doge-identity-service/src/core/infrastructure/providers.py` (новый)

### Out of scope
- `build_api_dependencies()` update — t02
- Supabase repositories — EPIC-IDS-05
- `asgi_app.py` singleton hook — без изменений
- Epic §8 smoke — t03

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
import os
os.environ.update({'APP_PROFILE': 'demo', 'API_BASE_URL': 'http://localhost:8100', 'DB_BACKEND': 'in_memory', 'EID_PROVIDER': 'mock'})
from core.infrastructure.providers import provide_service_factory
f = provide_service_factory()
print('db_backend:', f.config.db_backend)
print('mock provider:', f.get_eid_provider_registry().get('mock').provider_name)
print('Factory OK')
"
```
