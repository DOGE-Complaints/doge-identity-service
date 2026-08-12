## Task workspace — `task-ids-04-04-t03-story4-acceptance-verification`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000005`  
**Decision Ref:** [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) §6 Story 4  
**Story:** [`../STORY-IDS-04-04-eid-provider-registry-mock.md`](../STORY-IDS-04-04-eid-provider-registry-mock.md)  
---

## Task: tests — Story 4 acceptance verification

### Цель
Добавить pytest-покрытие verbatim AC Story 4 (epic L264–268): `isinstance(MockEIDProvider, EIDProviderPort)`, registry lookup, `get_active` error path, mock flow без внешних credentials.

### Почему это важно
eID — критический путь identity-сервиса; AC фиксируют plugin-контракт до интеграции с Authentigate/eID Easy.

### Факты из кода
1. Story 4 AC — [`../../../../EPIC-IDS-04-soa-service-factory.md`](../../../../EPIC-IDS-04-soa-service-factory.md) L264–268.
2. [`src/core/providers/`](../../../../../../../src/core/providers/) — только пустой `__init__.py` (t01–t02 создают модули).
3. [`src/core/config/schema.py`](../../../../../../../src/core/config/schema.py) — `eid_provider` field для `get_active` tests.

### Gap
Нет `tests/test_eid_providers.py` с AC L264–268.

### AC/DoD
- [ ] (P0) `isinstance(MockEIDProvider(...), EIDProviderPort)` — True.
- [ ] (P0) `EIDProviderRegistry({"mock": MockEIDProvider(...)}).get("mock").provider_name == "mock"`.
- [ ] (P0) `EIDProviderRegistry({}).get_active(config_with_eid_provider_eideasy)` → `KeyError` (или `EIDProviderError` — решение фиксируется в t02).
- [ ] (P0) При `config.eid_provider == "mock"` flow проходит без EIDEASY_*/AUTHENTIGATE_* (req-17 acceptance).

### Где менять код
- `doge-identity-service/tests/test_eid_providers.py` (новый)

### Out of scope
- Реализация base/registry/mock — t01, t02
- HTTP Authentigate timeout — forward note epic L269
- `tests/test_di_service_factory.py` — EPIC-IDS-06

### Проверка
```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_eid_providers.py -v
```
