## Task workspace — `task-ids-04-04-t02-eid-registry-and-mock-provider`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 4  
**Story:** [`../STORY-IDS-04-04-eid-provider-registry-mock.md`](../STORY-IDS-04-04-eid-provider-registry-mock.md)  
---

## Task: implement — EIDProviderRegistry + MockEIDProvider

### Цель
Создать `src/core/providers/registry.py` и `src/core/providers/mock/mock_provider.py` (+ `mock/__init__.py`) по epic L253–263.

### Почему это важно
Локальная разработка и тесты требуют mock-провайдера без EIDEASY_*/AUTHENTIGATE_* credentials. Registry выбирает активный провайдер по `config.eid_provider` per-request (не `@lru_cache`).

### Факты из кода
1. [`src/core/providers/registry.py`](../../../../../../../src/core/providers/registry.py) — **отсутствует**.
2. [`src/core/providers/mock/`](../../../../../../../src/core/providers/mock/) — **отсутствует**.
3. [`src/core/providers/base.py`](../../../../../../../src/core/providers/base.py) — создаётся в t01.
4. Epic L268: `MockEIDProvider` использует `verification_session_store` через DI, не хранит state в себе.

### Gap
Нет registry с `get` / `get_active` и mock flow (`/auth/mock/callback`).

### AC/DoD
- [ ] (P0) `EIDProviderRegistry({"mock": MockEIDProvider(...)}).get("mock").provider_name == "mock"`.
- [ ] (P0) `MockEIDProvider`: `provider_name == "mock"`, `callback_path == "/auth/mock/callback"`.
- [ ] (P0) `start_flow` создаёт session в store; `handle_callback` возвращает `EIDVerificationResult` с `provider="mock"`.
- [ ] (P0) Registry **не** использует `@lru_cache` (epic §7 pitfall).

### Где менять код
- `doge-identity-service/src/core/providers/registry.py` (новый)
- `doge-identity-service/src/core/providers/mock/__init__.py` (новый)
- `doge-identity-service/src/core/providers/mock/mock_provider.py` (новый)

### Out of scope
- eideasy / authentigate registration — TODO functional epic
- Story 4 full AC pytest — t03
- `provide_service_factory` wiring — Story 6

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.providers.registry import EIDProviderRegistry
from core.providers.mock.mock_provider import MockEIDProvider
from core.infrastructure.repositories import InMemoryVerificationSessionStore
store = InMemoryVerificationSessionStore()
r = EIDProviderRegistry({'mock': MockEIDProvider(store)})
assert r.get('mock').provider_name == 'mock'
print('registry + mock OK')
"
```
