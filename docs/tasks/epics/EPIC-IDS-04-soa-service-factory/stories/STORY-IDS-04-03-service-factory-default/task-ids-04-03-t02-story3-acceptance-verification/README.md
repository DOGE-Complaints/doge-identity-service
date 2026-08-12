## Task workspace — `task-ids-04-03-t02-story3-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 3  
**Story:** [`../STORY-IDS-04-03-service-factory-default.md`](../STORY-IDS-04-03-service-factory-default.md)  
---

## Task: tests — Story 3 acceptance verification

### Цель
Добавить pytest-покрытие verbatim AC Story 3 (epic L234–238): config accessor, identity of `get_*()` returns, `FrozenInstanceError`, Protocol structural typing.

### Почему это важно
Shared state InMemory репозиториев ломается, если factory пересоздаёт объекты на каждый `get_*()`; frozen guard предотвращает случайную мутацию DI-контейнера.

### Факты из кода
1. Story 3 AC — [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) L234–238.
2. [`src/core/infrastructure/service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py) — **отсутствует** (t01).
3. [`src/core/api/dependencies.py`](../../../../../../../src/core/api/dependencies.py) — EPIC-IDS-04 hooks; factory tests не требуют `build_api_dependencies` пока Story 6 не закрыт.

### Gap
Нет `tests/test_service_factory.py` с AC L234–238.

### AC/DoD
- [ ] (P0) `DefaultServiceFactory(...).config` — возвращает переданный `AppConfig`.
- [ ] (P0) `factory.get_profile_repository() is factory.get_profile_repository()` — True (same instance, factory не плодит копии).
- [ ] (P0) `factory.something = "x"` → `FrozenInstanceError`.
- [ ] (P0) `ServiceFactory` — `Protocol`, не базовый класс; `DefaultServiceFactory` его удовлетворяет.

### Где менять код
- `doge-identity-service/tests/test_service_factory.py` (новый)

### Out of scope
- `provide_service_factory` — Story 6
- `tests/test_di_service_factory.py` — EPIC-IDS-06

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_service_factory.py -v
```
