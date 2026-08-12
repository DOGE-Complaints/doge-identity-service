## Task workspace — `task-ids-10-01-t02-sms-descriptor-provider-runtime`

- Story: [`../STORY-IDS-PV-01-phone-provider-backbone.md`](../STORY-IDS-PV-01-phone-provider-backbone.md)
- Prerequisite: t01 (`SmsSenderPort` types)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000022`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md) Scope; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §6  
---

## Task: implement — `SmsProviderDescriptor`, `SmsProviderRuntime`, `SmsProviderNotRegisteredError`

### Цель
Ввести декларативный `SmsProviderDescriptor` (`name`, `config_spec`, `build(runtime) -> SmsSenderPort`), DI-bundle `SmsProviderRuntime` (`config`, `http_client`, `settings`), и guard exception — Story Scope bullet 4 (partial), AC #1.

### Почему это важно
Дескриптор + runtime — фундамент plugin-платформы; без них нельзя собрать реестр (t03) и mock-эталон (t04).

### Факты из кода
1. Образец дескриптора: [`descriptor.py:12-24`](../../../../../../../src/core/providers/descriptor.py) — `EIDProviderDescriptor`, `ProviderNotRegisteredError`.
2. Образец runtime: [`runtime.py`](../../../../../../../src/core/providers/runtime.py) — `ProviderRuntime` dataclass (eID DI-bundle).
3. `ConfigError` базовый: [`config/errors.py:1-2`](../../../../../../../src/core/config/errors.py).
4. `config_spec` stub допустим (наполнение — PV-02); образец: [`config_spec.py`](../../../../../../../src/core/providers/config_spec.py).
5. t01 создаёт `SmsSenderPort` в `core/phone/base.py`.

### Gap / Проблема
Нет SMS descriptor/runtime types; guard exception не определён.

### AC/DoD
- [x] (P0) `SmsProviderDescriptor` frozen dataclass: `name`, `config_spec`, `build(runtime) -> SmsSenderPort`.
- [x] (P0) `SmsProviderRuntime` dataclass: `config`, `http_client: httpx.Client | None`, `settings` (provider settings dict or typed stub).
- [x] (P0) `SmsProviderNotRegisteredError` — подкласс `ConfigError`.
- [x] (P1) Экспорт типов из `core.phone` package.
- [x] (P1) Story AC #1 traceability (descriptor + runtime).

### Где менять код
- `doge-identity-service/src/core/phone/descriptor.py` (new)
- `doge-identity-service/src/core/phone/runtime.py` (new)
- `doge-identity-service/src/core/phone/__init__.py`

### Out of scope
- `build_sms_registry` — t03
- `config_spec` validation / `SMS_PROVIDER` env — PV-02
- Mock sender impl — t04

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.phone.descriptor import SmsProviderDescriptor, SmsProviderNotRegisteredError; from core.phone.runtime import SmsProviderRuntime; print(SmsProviderDescriptor, SmsProviderRuntime)"
```
