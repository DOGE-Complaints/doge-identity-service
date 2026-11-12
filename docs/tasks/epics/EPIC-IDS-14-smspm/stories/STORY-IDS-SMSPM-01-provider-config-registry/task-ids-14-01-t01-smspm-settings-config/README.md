## Task workspace — `task-ids-14-01-t01-smspm-settings-config`

- Story: [`../STORY-IDS-SMSPM-01-provider-config-registry.md`](../STORY-IDS-SMSPM-01-provider-config-registry.md)
- Prerequisite: phone SMS backbone Done (EPIC-IDS-10 / PV-02 config_spec pattern)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000046`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md) (T01, D-01-1, D-01-2, D-01-3)  
---

## Task: implement — `SmspmSettings` + `SMSPM_SMS_CONFIG_SPEC`

### Цель
Пакет `src/core/phone/smspm/`: `config.py` с load/validate (`SMSPM_HASH`, `SMSPM_TOKEN`, `SMSPM_FROM`, optional base URL) + `config_spec` / `SMSPM_SMS_CONFIG_SPEC`.

### Почему это важно
Story AC #2: при активном `smspm` без обязательных env сервис не должен стартовать. D-01-3: validate только через `config_spec` когда провайдер активен.

### Факты из кода
1. [`telnyx/config.py:16-82`](../../../../../../../src/core/phone/telnyx/config.py) — `TELNYX_REQUIRED_ENV`, `validate_telnyx_config`, `TelnyxSettings.load`, `TelnyxSmsProviderConfigSpec`, `TELNYX_SMS_CONFIG_SPEC`.
2. [`schema.py:115-120`](../../../../../../../src/core/config/schema.py) — `_validate_active_sms_provider_config` вызывает `descriptor.config_spec.validate(env)` только для registered active name.
3. Пакет `src/core/phone/smspm/` отсутствует (нет файлов под `doge-identity-service/src`).

### Gap / Проблема
Нет `SmspmSettings` / SMSPM `config_spec`; fail-fast HASH/TOKEN/FROM невозможен.

### AC/DoD
- [x] (P0) `SmspmSettings` + validate: required `SMSPM_HASH`, `SMSPM_TOKEN`, `SMSPM_FROM` (D-01-1).
- [x] (P0) Optional `SMSPM_API_BASE_URL` default `https://api.smspm.com` (D-01-2).
- [x] (P0) `SMSPM_SMS_CONFIG_SPEC` с `validate`/`load` зеркало Telnyx `config_spec`.
- [x] (P1) Exports в `smspm/__init__.py` (settings/spec). Registry append — t02.

### Где менять код
- `doge-identity-service/src/core/phone/smspm/config.py` (**new**)
- `doge-identity-service/src/core/phone/smspm/__init__.py` (**new** — settings/spec exports)

### Out of scope
- Descriptor + `ALL_SMS_PROVIDER_DESCRIPTORS` (t02)
- HTTP-отправка SMS (SMSPM-02)
- `.env.example` (t04)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.phone.smspm.config import SmspmSettings, SMSPM_SMS_CONFIG_SPEC"
rg -n 'SMSPM_HASH|SMSPM_TOKEN|SMSPM_FROM|SMSPM_API_BASE_URL' src/core/phone/smspm/
```
