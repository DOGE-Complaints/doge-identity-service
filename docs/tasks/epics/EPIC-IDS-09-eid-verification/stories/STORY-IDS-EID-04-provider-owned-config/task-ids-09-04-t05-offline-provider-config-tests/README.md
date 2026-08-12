## Task workspace — `task-ids-09-04-t05-offline-provider-config-tests`

- Story: [`../STORY-IDS-EID-04-provider-owned-config.md`](../STORY-IDS-EID-04-provider-owned-config.md)
- Prerequisite: t03 delegated validation wired

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000017`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §F4  
---

## Task: tests — offline provider-owned config validation coverage

### Цель
Offline-тесты: authentigate missing required → `ConfigError` with field name; scopes default full URL; eideasy regression via delegated path; full offline suite green.

### Почему это важно
Story AC #2 и #5: fail-fast с именем поля + offline green + test on missing required.

### Факты из кода
1. Existing eideasy test: [`tests/test_config_schema.py:75-86`](../../../../../../../tests/test_config_schema.py).
2. No provider-owned config tests yet — new file expected.
3. Offline marker: [`tests/conftest.py`](../../../../../../../tests/conftest.py) — `live_integration` exclusion.

### Gap / Проблема
No dedicated tests for authentigate delegated validation or scopes default.

### AC/DoD
- [x] (P0) `EID_PROVIDER=authentigate` without `AUTHENTIGATE_CLIENT_ID` (or similar required) → `ConfigError` mentioning field name.
- [x] (P0) Unit test: default scopes contain full claim-URL prefix (no live).
- [x] (P0) `test_eideasy_provider_requires_credentials` passes via delegated eideasy config_spec (adapt if moved).
- [x] (P1) Full offline suite green: `pytest -m "not live_integration" -q`.

### Где менять код
- `doge-identity-service/tests/test_provider_owned_config.py` (new)
- optional updates: `doge-identity-service/tests/test_config_schema.py`

### Out of scope
- Live demo / SPIKE-09 integration tests
- Story acceptance doc — t06

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_provider_owned_config.py tests/test_config_schema.py -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
