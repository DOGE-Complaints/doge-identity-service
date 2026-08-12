## Task workspace — `task-ids-09-03-t01-descriptor-runtime-types`

- Story: [`../STORY-IDS-EID-03-provider-plugin-backbone.md`](../STORY-IDS-EID-03-provider-plugin-backbone.md)
- Prerequisite: STORY-IDS-EID-01 Done ([`../STORY-IDS-EID-01-eid-verification-flow/STORY-IDS-EID-01-eid-verification-flow.md`](../STORY-IDS-EID-01-eid-verification-flow/STORY-IDS-EID-01-eid-verification-flow.md))

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000016`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §F5  
---

## Task: implement — `EIDProviderDescriptor` and `ProviderRuntime` types

### Цель
Ввести декларативный `EIDProviderDescriptor` (`name`, `config_spec`, `build(runtime) -> EIDProviderPort`) и dataclass `ProviderRuntime` (DI-bundle skeleton) — фундамент plugin-платформы из story Scope.

### Почему это важно
Story AC #1: «Есть `EIDProviderDescriptor` и `ProviderRuntime`». Без типов нельзя собрать lazy-реестр и mock-дескриптор (t03).

### Факты из кода
1. [`base.py:32-53`](../../../../../../../src/core/providers/base.py) — `EIDProviderPort` protocol (контракт `build` должен возвращать).
2. [`registry.py:7-17`](../../../../../../../src/core/providers/registry.py) — текущий реестр без дескрипторов.
3. [`providers.py:92`](../../../../../../../src/core/infrastructure/providers.py) — хардкод `MockEIDProvider` в фабрике.
4. [`schema.py:9`](../../../../../../../src/core/config/schema.py) — `ConfigError` базовый класс для guard (t04).
5. [`__init__.py`](../../../../../../../src/core/providers/__init__.py) — публичный реэкспорт провайдеров.

### Gap / Проблема
Нет типов дескриптора/runtime; провайдеры не подключаются декларативно.

### AC/DoD
- [x] (P0) `EIDProviderDescriptor` с полями `name`, `config_spec` (minimal/empty stub — наполнение EID-04), `build(runtime) -> EIDProviderPort`.
- [x] (P0) `ProviderRuntime` dataclass: `config`, `session_store`, optional `http_client`, optional слоты `secret_box`, `oidc`, `clock`.
- [x] (P0) `ProviderNotRegisteredError` — подкласс `ConfigError` (или alias) для registry guard (t04).
- [x] (P1) Экспорт новых типов из `core.providers` package.

### Где менять код
- `doge-identity-service/src/core/providers/descriptor.py` (new)
- `doge-identity-service/src/core/providers/runtime.py` (new)
- `doge-identity-service/src/core/providers/__init__.py`

### Out of scope
- Сборка runtime в фабрике — t02
- `build_registry`, mock descriptor — t03
- Guard в `registry.get` — t04
- Наполнение `config_spec` валидацией — EID-04

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.providers.descriptor import EIDProviderDescriptor; from core.providers.runtime import ProviderRuntime; print(EIDProviderDescriptor, ProviderRuntime)"
```
