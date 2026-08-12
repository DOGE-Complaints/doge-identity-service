## Task workspace — `task-ids-04-03-t01-service-factory-protocol-and-default`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 3  
**Story:** [`../STORY-IDS-04-03-service-factory-default.md`](../STORY-IDS-04-03-service-factory-default.md)  
---

## Task: implement — ServiceFactory Protocol + DefaultServiceFactory

### Цель
Создать `ServiceFactory(Protocol)` в `src/core/application/factory.py` и `@dataclass(frozen=True) class DefaultServiceFactory` в `src/core/infrastructure/service_factory.py` по epic L214–233.

### Почему это важно
Factory — единственный объект, знающий связи между сервисами. `frozen=True` + `get_*()` returning same instance гарантируют shared InMemory state и иммутабельность контейнера.

### Факты из кода
1. [`src/core/application/`](../../../../../../../src/core/application/) — **отсутствует** (нет `factory.py`).
2. [`src/core/infrastructure/service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py) — **отсутствует**.
3. [`src/core/api/dependencies.py:63-90`](../../../../../../../src/core/api/dependencies.py) — commented block ожидает `service_factory.get_*()` из EPIC-IDS-04.
4. [`src/core/domain/`](../../../../../../../src/core/domain/) и [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py) — зависимости Story 1–2.

### Gap
Epic §6 Story 3 Outputs L214–233 не реализованы; заглушки `return object()` отсутствуют, но factory-класса нет.

### AC/DoD
- [ ] (P0) `DefaultServiceFactory(...).config` — возвращает переданный `AppConfig`.
- [ ] (P0) `factory.get_profile_repository() is factory.get_profile_repository()` — True (same instance).
- [ ] (P0) `factory.something = "x"` → `FrozenInstanceError`.
- [ ] (P0) `ServiceFactory` — `Protocol`, не базовый класс; `DefaultServiceFactory` его удовлетворяет.

### Где менять код
- `doge-identity-service/src/core/application/__init__.py` (новый)
- `doge-identity-service/src/core/application/factory.py` (новый)
- `doge-identity-service/src/core/infrastructure/service_factory.py` (новый)

### Out of scope
- `provide_service_factory()` assembly — Story 6
- Story 3 pytest — t02
- eID registry / JWT — Story 4–5

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -c "
from dataclasses import FrozenInstanceError
from core.application.factory import ServiceFactory
from core.infrastructure.service_factory import DefaultServiceFactory
import typing
assert typing.runtime_checkable(ServiceFactory) or hasattr(ServiceFactory, '__protocol_attrs__')
print('ServiceFactory types OK')
"
```
