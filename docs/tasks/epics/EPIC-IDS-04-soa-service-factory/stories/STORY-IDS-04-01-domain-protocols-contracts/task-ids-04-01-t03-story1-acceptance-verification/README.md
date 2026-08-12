## Task workspace — `task-ids-04-01-t03-story1-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 1  
**Story:** [`../STORY-IDS-04-01-domain-protocols-contracts.md`](../STORY-IDS-04-01-domain-protocols-contracts.md)  
---

## Task: tests — Story 1 acceptance verification

### Цель
Добавить pytest-покрытие всех AC Story 1 (epic L134–138): импорты contracts/models, `@runtime_checkable` на всех Protocols, отсутствие запрещённых импортов в `core/domain/*`.

### Почему это важно
Domain — фундамент SOA; без автоматической проверки AC регрессии (отсутствие `@runtime_checkable`, leak fastapi в domain) останутся незамеченными до EPIC-IDS-06.

### Факты из кода
1. Story 1 AC — [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) L134–138.
2. [`src/core/domain/`](../../../../../../../src/core/domain/) — **отсутствует** (реализуется в t01–t02).
3. [`tests/`](../../../../../../../tests/) — нет `test_domain_contracts.py` / аналога для Story 1.
4. [`src/core/api/dependencies.py:12-22`](../../../../../../../src/core/api/dependencies.py) — hooks EPIC-IDS-04; domain-тесты не трогают DI.

### Gap
Нет тестового файла с verbatim AC Story 1 L134–138.

### AC/DoD
- [ ] (P0) `from core.domain.contracts import ProfileRepository, VerificationSessionStore, ...` — без ошибок (тест импорта).
- [ ] (P0) Все Protocols имеют `@runtime_checkable`.
- [ ] (P0) `from core.domain.models import ProfileRecord, VerificationSession, EIDAuditEvent` — без ошибок.
- [ ] (P0) Domain-слой (`core/domain/*`) не импортирует ничего из `core.infrastructure.*`, `httpx`, `fastapi`, `joserfc` (static scan или importlib smoke).

### Где менять код
- `doge-identity-service/tests/test_domain_contracts.py` (новый)

### Out of scope
- Реализация contracts/models — t01, t02
- InMemory `isinstance` checks — Story 2 t03
- `tests/test_di_service_factory.py` — EPIC-IDS-06

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_domain_contracts.py -v
```
