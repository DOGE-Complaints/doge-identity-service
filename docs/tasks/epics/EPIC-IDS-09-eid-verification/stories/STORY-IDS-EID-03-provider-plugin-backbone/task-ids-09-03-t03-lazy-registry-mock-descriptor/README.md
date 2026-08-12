## Task workspace — `task-ids-09-03-t03-lazy-registry-mock-descriptor`

- Story: [`../STORY-IDS-EID-03-provider-plugin-backbone.md`](../STORY-IDS-EID-03-provider-plugin-backbone.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000016`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §F5  
---

## Task: implement — lazy `build_registry` + mock descriptor (эталон)

### Цель
Заменить хардкод [`providers.py:92`](../../../../../../../src/core/infrastructure/providers.py) на `build_registry(runtime)` из набора дескрипторов; `MockEIDProvider` — через `EIDProviderDescriptor` (эталон для будущих провайдеров).

### Почему это важно
Story AC #1 (mock via descriptor), AC #2 (реестр из дескрипторов; +провайдер = +дескриптор, не правки тела `providers.py`/`registry.py`).

### Факты из кода
1. [`providers.py:92`](../../../../../../../src/core/infrastructure/providers.py) — `EIDProviderRegistry({"mock": MockEIDProvider(...)})`.
2. [`mock/mock_provider.py`](../../../../../../../src/core/providers/mock/mock_provider.py) — `MockEIDProvider` реализация порта.
3. [`registry.py:7-17`](../../../../../../../src/core/providers/registry.py) — `EIDProviderRegistry` API.
4. [`handlers.py`](../../../../../../../src/core/api/handlers.py) — `get_active(config)` consumer at runtime.
5. [`test_eid_provider_registry.py:14-18`](../../../../../../../tests/test_eid_provider_registry.py) — smoke: mock registered by default.

### Gap / Проблема
Реестр не строится из дескрипторов; mock не является эталоном plugin registration.

### AC/DoD
- [x] (P0) `MOCK_EID_DESCRIPTOR` (или аналог) оборачивает `MockEIDProvider.build(runtime)`.
- [x] (P0) `build_registry(runtime)` регистрирует **active** provider (`config.eid_provider`) + всегда `mock` (lazy — только нужные инстансы).
- [x] (P0) Убрать inline `EIDProviderRegistry({"mock": ...})` из `providers.py`; wiring через descriptor list / registry builder module.
- [x] (P1) Добавление нового провайдера = append descriptor в registry module, без правок `registry.py` class body (AC #2).
- [x] (P1) Существующий offline eID flow (EID-01) не ломается при `EID_PROVIDER=mock`.

### Где менять код
- `doge-identity-service/src/core/providers/mock/descriptor.py` (new) или `mock/__init__.py`
- `doge-identity-service/src/core/providers/registry_builder.py` (new)
- `doge-identity-service/src/core/infrastructure/providers.py`

### Out of scope
- Authentigate/eideasy descriptors — EID-02
- `registry.get` guard — t04
- `config_spec` validation — EID-04

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_eid_provider_registry.py tests/test_eid_verification_flow.py -m "not live_integration" -q
```
