## Task workspace — `task-ids-10-02-t02-appconfig-phone-fields-sms-provider-validation`

- Story: [`../STORY-IDS-PV-02-provider-owned-config.md`](../STORY-IDS-PV-02-provider-owned-config.md)
- Prerequisite: t01 (`SmsProviderConfigSpec`)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000023`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md); [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §7  
---

## Task: implement — `AppConfig` phone fields, `SMS_PROVIDER` membership, delegated validation

### Цель
Добавить ядровые phone-поля в `AppConfig` + парсинг env; валидировать `SMS_PROVIDER` по [`registered_sms_provider_names()`](../../../../../../../src/core/phone/registry_builder.py); вызывать `_validate_active_sms_provider_config` → `descriptor.config_spec.validate(env)` — Story Scope bullets 2, 4; AC #1, #4.

### Почему это важно
Закрывает PV-01 bridge `getattr(config, "sms_provider", "mock")`; зеркало [`schema.py:110-128`](../../../../../../../src/core/config/schema.py) для eID.

### Факты из кода
1. `AppConfig` **без** `sms_provider` / `phone_*` ([`schema.py`](../../../../../../../src/core/config/schema.py) — grep пуст).
2. eID membership: [`schema.py:110-116`](../../../../../../../src/core/config/schema.py).
3. eID delegated validate: [`schema.py:93-98`](../../../../../../../src/core/config/schema.py) `_validate_active_eid_provider_config`.
4. PV-01 registry: [`registry_builder.py:24`](../../../../../../../src/core/phone/registry_builder.py) uses `getattr(runtime.config, "sms_provider", "mock")`.
5. Architecture defaults §7: `SMS_PROVIDER=mock`, `PHONE_ALLOWED_DIAL_PREFIXES=+372`, OTP params.

### Gap / Проблема
No typed `AppConfig.sms_provider`; no fail-fast on unknown `SMS_PROVIDER` at config load.

### AC/DoD
- [ ] (P0) `AppConfig` fields: `sms_provider`, `phone_allowed_dial_prefixes` (tuple), `phone_code_length`, `phone_code_ttl_s`, `phone_max_attempts`, `phone_resend_cooldown_s`, `phone_one_account_per_number`.
- [ ] (P0) Parse env keys verbatim from story Scope; defaults per architecture §7 for demo profile.
- [ ] (P0) `SMS_PROVIDER` membership check → `ConfigError` with allowed names (Story AC #1).
- [ ] (P0) `_validate_active_sms_provider_config(env, sms_provider)` delegates to active descriptor `config_spec.validate(env)`.
- [ ] (P0) `build_sms_registry` uses `runtime.config.sms_provider` directly.
- [ ] (P1) [`providers.py`](../../../../../../../src/core/config/providers.py) default `SMS_PROVIDER=mock`.

### Где менять код
- `doge-identity-service/src/core/config/schema.py`
- `doge-identity-service/src/core/config/providers.py`
- `doge-identity-service/src/core/phone/registry_builder.py`
- `doge-identity-service/src/core/phone/registry.py` (optional: type `get_active(config: AppConfig)`)

### Out of scope
- E.164 normalize/prefix gate — t03
- `TELNYX_*` in `AppConfig` — PV-06
- Comprehensive tests — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.config.providers import provide_app_config; c=provide_app_config(); print(c.sms_provider, c.phone_allowed_dial_prefixes)"
```
