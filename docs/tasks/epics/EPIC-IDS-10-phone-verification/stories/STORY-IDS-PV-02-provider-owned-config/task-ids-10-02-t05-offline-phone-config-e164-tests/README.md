## Task workspace — `task-ids-10-02-t05-offline-phone-config-e164-tests`

- Story: [`../STORY-IDS-PV-02-provider-owned-config.md`](../STORY-IDS-PV-02-provider-owned-config.md)
- Prerequisite: t01–t04 implemented

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000023`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md) AC #1–#5  
---

## Task: test — offline phone config and E.164 coverage

### Цель
Покрыть тестами `SMS_PROVIDER` validation, `AppConfig` phone fields, E.164 normalization, prefix allowlist gate — Story AC #1–#5.

### Почему это важно
EID-04 pattern: [`test_config_schema.py`](../../../../../../../tests/test_config_schema.py) for provider membership; phone needs parallel coverage.

### Факты из кода
1. eID tests: [`test_config_schema.py:75+`](../../../../../../../tests/test_config_schema.py) — unknown provider `ConfigError`.
2. `_demo_config` in [`test_service_factory.py:29`](../../../../../../../tests/test_service_factory.py), [`test_eid_providers.py`](../../../../../../../tests/test_eid_providers.py), [`test_inmemory_repositories.py`](../../../../../../../tests/test_inmemory_repositories.py) — need new `AppConfig` fields after t02.
3. Baseline: 260 pytest offline (post PV-01).

### Gap / Проблема
No `test_phone_config_schema.py` / `test_phone_e164.py`; fixtures may break after `AppConfig` extension.

### AC/DoD
- [ ] (P0) Test: unknown `SMS_PROVIDER` → `ConfigError` with allowed names (Story AC #1).
- [ ] (P0) Test: `PHONE_ALLOWED_DIAL_PREFIXES` parsed to tuple on `AppConfig`.
- [ ] (P0) Test: `+372...` passes prefix gate; `+1...` → `COUNTRY_NOT_ALLOWED` (Story AC #2).
- [ ] (P0) Test: E.164 normalize — spaces, parens, without `+` (Story AC #3).
- [ ] (P0) Test: core phone params readable from `AppConfig`; no `TELNYX_*` on `AppConfig` (Story AC #4).
- [ ] (P1) Update `_demo_config` fixtures with phone field defaults.
- [ ] (P1) Full offline suite green (Story AC #5).

### Где менять код
- `doge-identity-service/tests/test_phone_config_schema.py` (new)
- `doge-identity-service/tests/test_phone_e164.py` (new)
- `doge-identity-service/tests/test_service_factory.py`
- `doge-identity-service/tests/test_eid_providers.py`
- `doge-identity-service/tests/test_inmemory_repositories.py`

### Out of scope
- Story acceptance doc — t06
- Live Telnyx tests — PV-06

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_phone_config_schema.py tests/test_phone_e164.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
