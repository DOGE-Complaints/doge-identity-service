## Task workspace — `task-ids-10-02-t01-sms-provider-config-spec`

- Story: [`../STORY-IDS-PV-02-provider-owned-config.md`](../STORY-IDS-PV-02-provider-owned-config.md)
- Prerequisite: STORY-IDS-PV-01 Done ([`../STORY-IDS-PV-01-phone-provider-backbone/STORY-IDS-PV-01-phone-provider-backbone.md`](../STORY-IDS-PV-01-phone-provider-backbone/STORY-IDS-PV-01-phone-provider-backbone.md))

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000023`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md) Scope #1; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §7  
---

## Task: implement — `SmsProviderConfigSpec` type and descriptor wire

### Цель
Формализовать `SmsProviderConfigSpec` (`required`, `optional_defaults`, `validate`/`load`) в phone-пакете и перевести `SmsProviderDescriptor` + mock descriptor с generic `ProviderConfigSpec` на phone-тип — Story Scope bullet 1.

### Почему это важно
Story AC #4: провайдер-поля не в `AppConfig`; делегированная валидация (t02) требует typed `config_spec` на дескрипторе.

### Факты из кода
1. eID образец: [`config_spec.py:16-29`](../../../../../../../src/core/providers/config_spec.py) — `ProviderConfigSpec`.
2. PV-01 mock uses `ProviderConfigSpec` directly ([`mock/descriptor.py:9-13`](../../../../../../../src/core/phone/mock/descriptor.py)).
3. [`descriptor.py:19`](../../../../../../../src/core/phone/descriptor.py) — `config_spec: ProviderConfigSpec`.
4. `SmsProviderConfigSpec` module **отсутствует** (glob `src/core/phone/config_spec.py` — 0).

### Gap / Проблема
Phone layer reuses eID `ProviderConfigSpec` without dedicated SMS type name from story Scope.

### AC/DoD
- [ ] (P0) `SmsProviderConfigSpec` in `core/phone/config_spec.py` (alias or thin wrapper over `ProviderConfigSpec` with same API).
- [ ] (P0) `SmsProviderDescriptor.config_spec` typed as `SmsProviderConfigSpec`.
- [ ] (P0) `MOCK_SMS_CONFIG_SPEC` updated; mock descriptor unchanged behavior (no required fields).
- [ ] (P1) Export from `core.phone` package.

### Где менять код
- `doge-identity-service/src/core/phone/config_spec.py` (new)
- `doge-identity-service/src/core/phone/descriptor.py`
- `doge-identity-service/src/core/phone/mock/descriptor.py`
- `doge-identity-service/src/core/phone/__init__.py`

### Out of scope
- `AppConfig` phone fields — t02
- E.164 utility — t03
- `.env.example` — t04

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.phone.config_spec import SmsProviderConfigSpec; from core.phone.mock.descriptor import MOCK_SMS_CONFIG_SPEC; print(SmsProviderConfigSpec, MOCK_SMS_CONFIG_SPEC)"
```
