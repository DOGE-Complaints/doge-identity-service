## Task workspace — `task-ids-09-04-t03-delegated-validation-schema-cleanup`

- Story: [`../STORY-IDS-EID-04-provider-owned-config.md`](../STORY-IDS-EID-04-provider-owned-config.md)
- Prerequisite: t01 ProviderConfigSpec; t02 authentigate + eideasy config_spec stubs

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000017`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §F4  
---

## Task: implement — delegated validation and remove provider-if from schema

### Цель
После generic parse вызывать `descriptor.config_spec.validate(env)` для активного провайдера; убрать провайдер-`if` из ядра (`eideasy` block → eideasy config_spec).

### Почему это важно
Story AC #2: `EID_PROVIDER=authentigate` без required → `ConfigError` с именем поля, fail-fast. AC #3: no provider logic in `schema.py` body.

### Факты из кода
1. eideasy-only if: [`schema.py:109-112`](../../../../../../../src/core/config/schema.py).
2. Generic membership only should remain: [`schema.py:96-98`](../../../../../../../src/core/config/schema.py).
3. Config entry: [`providers.py:10-23`](../../../../../../../src/core/config/providers.py) → `load_config_from_env`.
4. Existing eideasy test: [`tests/test_config_schema.py:75-86`](../../../../../../../tests/test_config_schema.py).
5. Descriptor lookup: [`registry_builder.py:12-13`](../../../../../../../src/core/providers/registry_builder.py) `_DESCRIPTOR_BY_NAME`.

### Gap / Проблема
Validation hardcoded in schema; authentigate has no fail-fast (F4).

### AC/DoD
- [x] (P0) After generic checks in `load_config_from_env`: resolve active descriptor → `config_spec.validate(env)` → `ConfigError` with missing field name.
- [x] (P0) Remove `if eid_provider == "eideasy"` block from [`schema.py:109-112`](../../../../../../../src/core/config/schema.py); move to eideasy `config_spec` (minimal `providers/eideasy/config.py` or descriptor stub).
- [x] (P0) `schema.py` retains only generic + `eid_provider` membership — no other provider-specific logic.
- [x] (P1) `test_eideasy_provider_requires_credentials` still passes via delegated path.

### Где менять код
- `doge-identity-service/src/core/config/schema.py`
- `doge-identity-service/src/core/providers/eideasy/config.py` (new, minimal)
- optional `doge-identity-service/src/core/providers/eideasy/descriptor.py` (stub for config_spec)
- `doge-identity-service/src/core/providers/registry_builder.py` (eideasy descriptor registration if needed)

### Out of scope
- `.env.example` — t04
- New offline tests — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_config_schema.py -q
grep -n "eideasy\|authentigate" src/core/config/schema.py
```
