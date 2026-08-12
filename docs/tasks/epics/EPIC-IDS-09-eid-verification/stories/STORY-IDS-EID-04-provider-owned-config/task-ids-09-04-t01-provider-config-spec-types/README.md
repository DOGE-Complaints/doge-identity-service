## Task workspace — `task-ids-09-04-t01-provider-config-spec-types`

- Story: [`../STORY-IDS-EID-04-provider-owned-config.md`](../STORY-IDS-EID-04-provider-owned-config.md)
- Prerequisite: STORY-IDS-EID-03 Done ([`../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md`](../STORY-IDS-EID-03-provider-plugin-backbone/STORY-IDS-EID-03-provider-plugin-backbone.md))

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000017`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §F3  
---

## Task: implement — `ProviderConfigSpec` types and descriptor integration

### Цель
Заменить stub `config_spec: tuple[str, ...]` на `ProviderConfigSpec` с `required`, `optional_defaults`, `validate(env)` / `load(env) -> settings` — фундамент provider-owned config из story Scope.

### Почему это важно
Story AC #3: добавление провайдера не должно требовать правок `schema.py`. Без типа `ProviderConfigSpec` нельзя делегировать валидацию (t03) и Authentigate spec (t02).

### Факты из кода
1. [`descriptor.py:15-29`](../../../../../../../src/core/providers/descriptor.py) — `config_spec: tuple[str, ...]`, `empty_config_spec()` placeholder «until EID-04».
2. [`mock/descriptor.py:13-17`](../../../../../../../src/core/providers/mock/descriptor.py) — mock uses `empty_config_spec()`.
3. [`registry_builder.py:8-10`](../../../../../../../src/core/providers/registry_builder.py) — `ALL_EID_PROVIDER_DESCRIPTORS` (mock only).
4. [`__init__.py`](../../../../../../../src/core/providers/__init__.py) — public re-exports.

### Gap / Проблема
`config_spec` — пустой tuple-stub; нет контракта `required` / `optional_defaults` / `validate` / `load`.

### AC/DoD
- [x] (P0) `ProviderConfigSpec` protocol/dataclass: `required: tuple[str, ...]`, `optional_defaults: dict[str, str]`, `validate(env) -> None`, `load(env) -> settings`.
- [x] (P0) `EIDProviderDescriptor.config_spec` typed as `ProviderConfigSpec`; remove `empty_config_spec()` tuple stub.
- [x] (P0) Mock descriptor → no-op spec (no required fields).
- [x] (P1) Export `ProviderConfigSpec` from `core.providers`.

### Где менять код
- `doge-identity-service/src/core/providers/config_spec.py` (new)
- `doge-identity-service/src/core/providers/descriptor.py`
- `doge-identity-service/src/core/providers/mock/descriptor.py`
- `doge-identity-service/src/core/providers/__init__.py`

### Out of scope
- `AuthentigateSettings` — t02
- Delegated validation hook in `schema.py` — t03
- `.env.example` — t04

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.providers.config_spec import ProviderConfigSpec; from core.providers.descriptor import EIDProviderDescriptor; print(ProviderConfigSpec, EIDProviderDescriptor)"
.venv/bin/python -m pytest tests/test_provider_plugin_backbone.py -q
```
