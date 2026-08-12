## Task workspace — `task-ids-04-04-t01-eid-provider-port-base`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 4  
**Story:** [`../STORY-IDS-04-04-eid-provider-registry-mock.md`](../STORY-IDS-04-04-eid-provider-registry-mock.md)  
---

## Task: implement — EIDProviderPort base module

### Цель
Создать `src/core/providers/base.py` и обновить `src/core/providers/__init__.py` по epic L248–252: `EIDVerificationResult`, `EIDStartResult`, `@runtime_checkable EIDProviderPort`, `EIDProviderError`.

### Почему это важно
Plugin-архитектура eID (req-17) изолирует HTTP-слой от провайдер-специфики. `EIDProviderPort` — контракт для mock/eideasy/authentigate; registry и factory зависят от него.

### Факты из кода
1. [`src/core/providers/base.py`](../../../../../../../src/core/providers/base.py) — **отсутствует**.
2. [`src/core/providers/__init__.py`](../../../../../../../src/core/providers/__init__.py) — только docstring «Providers layer package».
3. Epic L133: `EIDProviderPort` в `providers/base.py`, не в `core/domain/contracts.py`.
4. [`src/core/api/dependencies.py:41`](../../../../../../../src/core/api/dependencies.py) — слот `eid_provider_registry: object | None`.

### Gap
Нет Port, result-dataclasses и `EIDProviderError` из epic L248–252.

### AC/DoD
- [ ] (P0) `@runtime_checkable class EIDProviderPort(Protocol)` с `provider_name`, `callback_path`, `start_flow`, `handle_callback`.
- [ ] (P0) `EIDVerificationResult` — `@dataclass(frozen=True)`; `EIDStartResult` — `@dataclass`.
- [ ] (P0) `class EIDProviderError(Exception)` с полем `code: str`.
- [ ] (P0) Пакет `core.providers` экспортирует публичные символы через `__init__.py`.

### Где менять код
- `doge-identity-service/src/core/providers/base.py` (новый)
- `doge-identity-service/src/core/providers/__init__.py` (обновить exports)

### Out of scope
- `EIDProviderRegistry`, `MockEIDProvider` — t02
- Story 4 pytest — t03
- Authentigate / eID Easy HTTP — функциональные эпики

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from core.providers.base import EIDProviderPort, EIDVerificationResult, EIDStartResult, EIDProviderError
import typing
assert typing.runtime_checkable(EIDProviderPort) or hasattr(EIDProviderPort, '__protocol_attrs__')
print('EIDProviderPort base OK')
"
```
