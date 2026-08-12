## Task workspace — `task-ids-10-01-t03-sms-registry-builder-guard`

- Story: [`../STORY-IDS-PV-01-phone-provider-backbone.md`](../STORY-IDS-PV-01-phone-provider-backbone.md)
- Prerequisite: t02 (`SmsProviderDescriptor`, `SmsProviderRuntime`)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000022`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md); [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §6  
---

## Task: implement — `SmsSenderRegistry`, `build_sms_registry`, registry guard

### Цель
Реализовать lazy-реестр SMS-провайдеров из набора дескрипторов с guard вместо `KeyError`; `build_sms_registry(runtime)` регистрирует active + `mock` — Story Scope bullet 4, AC #1 (registry), AC #3, AC #4.

### Почему это важно
Story AC #3: незарегистрированный провайдер → `SmsProviderNotRegisteredError` с перечислением доступных. AC #4: новый провайдер = +1 дескриптор в tuple, без правок тела `registry.py`.

### Факты из кода
1. Образец реестра: [`registry.py:8-25`](../../../../../../../src/core/providers/registry.py) — `get`, `get_active`, `registered_names`.
2. Образец builder: [`registry_builder.py:10-40`](../../../../../../../src/core/providers/registry_builder.py) — `ALL_EID_PROVIDER_DESCRIPTORS`, `build_registry`.
3. eID guard message pattern: [`registry.py:19-21`](../../../../../../../src/core/providers/registry.py).
4. **PV-01 / PV-02 boundary:** `get_active(config)` принимает объект с атрибутом `sms_provider` (тесты — `SimpleNamespace`); полная `AppConfig` + `SMS_PROVIDER` env — PV-02.

### Gap / Проблема
Нет SMS registry/builder; нет extensible descriptor list.

### AC/DoD
- [x] (P0) `SmsSenderRegistry` с `get(name)`, `get_active(config_like)`, `registered_names`.
- [x] (P0) `get` бросает `SmsProviderNotRegisteredError` с текстом «доступны: …», не `KeyError` (Story AC #3).
- [x] (P0) `build_sms_registry(runtime)` строит active provider + всегда `mock` (lazy — только нужные инстансы).
- [x] (P0) `ALL_SMS_PROVIDER_DESCRIPTORS` tuple + `registered_sms_provider_names()`; добавление провайдера = append descriptor (Story AC #4).
- [x] (P1) `get_active` читает `config.sms_provider` (duck-typed until PV-02 wires `AppConfig`).

### Где менять код
- `doge-identity-service/src/core/phone/registry.py` (new)
- `doge-identity-service/src/core/phone/registry_builder.py` (new)
- `doge-identity-service/src/core/phone/__init__.py`

### Out of scope
- `MockSmsSender` + `MOCK_SMS_DESCRIPTOR` registration — t04
- Offline tests — t05
- `AppConfig.sms_provider` field + env validation — PV-02
- Service factory wiring — PV-05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.phone.registry_builder import build_sms_registry, registered_sms_provider_names; print(registered_sms_provider_names())"
```
