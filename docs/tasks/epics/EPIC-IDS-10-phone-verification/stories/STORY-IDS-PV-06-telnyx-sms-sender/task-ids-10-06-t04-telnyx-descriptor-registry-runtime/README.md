## Task workspace — `task-ids-10-06-t04-telnyx-descriptor-registry-runtime`

- Story: [`../STORY-IDS-PV-06-telnyx-sms-sender.md`](../STORY-IDS-PV-06-telnyx-sms-sender.md)
- Prerequisite: t01–t03 (config, sender, errors)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000027`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md) Scope bullet 4; [`../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md) §9  
---

## Task: implement — `TELNYX_SMS_DESCRIPTOR` + registry + httpx runtime

### Цель
Зарегистрировать Telnyx в SMS registry; `SMS_PROVIDER=telnyx` → `get_active()` returns `TelnyxSmsSender`; extend runtime with sync `httpx.Client`.

### Почему это важно
Story AC #1 (runtime half): active provider resolves to Telnyx adapter with settings from `TelnyxSettings.load`.

### Факты из кода
1. Registry today: [`ALL_SMS_PROVIDER_DESCRIPTORS = (MOCK_SMS_DESCRIPTOR,)`](../../../../../../../src/core/phone/registry_builder.py:8-10) → `registered_sms_provider_names()` → `{"mock"}` only.
2. `test_unknown_sms_provider_rejected`: `SMS_PROVIDER=telnyx` → `ConfigError` ([`test_phone_config_schema.py:21-23`](../../../../../../../tests/test_phone_config_schema.py)).
3. eID runtime httpx mirror: [`build_provider_runtime`](../../../../../../../src/core/providers/runtime_factory.py:16-25) — sync `httpx.Client` when provider needs HTTP.
4. `SmsProviderRuntime`: [`runtime.py`](../../../../../../../src/core/phone/runtime.py) — extend with optional `http_client` + `settings` dict or typed slot.
5. Mock descriptor pattern: [`mock/descriptor.py`](../../../../../../../src/core/phone/mock/descriptor.py).

### Gap / Проблема
Telnyx not in descriptor set; `build_sms_provider_runtime` has no httpx; config schema rejects `telnyx` provider name.

### AC/DoD
- [ ] (P0) `TELNYX_SMS_DESCRIPTOR` in `src/core/phone/telnyx/descriptor.py`; `name="telnyx"`.
- [ ] (P0) Add to `ALL_SMS_PROVIDER_DESCRIPTORS` in [`registry_builder.py`](../../../../../../../src/core/phone/registry_builder.py).
- [ ] (P0) `build_sms_provider_runtime`: create sync `httpx.Client` when active SMS provider is telnyx; pass `TelnyxSettings` via runtime.
- [ ] (P0) `descriptor.build(runtime)` → `TelnyxSmsSender` with settings + client.
- [ ] (P0) Update [`test_phone_config_schema.py`](../../../../../../../tests/test_phone_config_schema.py): `telnyx` in allowed names (with required TELNYX_* env).
- [ ] (P1) Story AC #1: `registry.get_active(config).send` returns Telnyx instance when `SMS_PROVIDER=telnyx`.

### Где менять код
- `doge-identity-service/src/core/phone/telnyx/descriptor.py` (new)
- `doge-identity-service/src/core/phone/registry_builder.py`
- `doge-identity-service/src/core/phone/runtime_factory.py`
- `doge-identity-service/src/core/phone/runtime.py` (if needed)
- `doge-identity-service/tests/test_phone_config_schema.py`

### Out of scope
- Unit test suite — t05
- `.env.example` — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "
from core.config import load_config_from_env
from core.phone.runtime_factory import build_sms_provider_runtime
from core.phone.registry_builder import build_sms_registry
env = {'APP_PROFILE':'demo','API_BASE_URL':'http://x','DB_BACKEND':'in_memory','EID_PROVIDER':'mock','SMS_PROVIDER':'telnyx','TELNYX_API_KEY':'k','TELNYX_MESSAGING_PROFILE_ID':'p'}
cfg = load_config_from_env(env)
rt = build_sms_provider_runtime(config=cfg)
reg = build_sms_registry(rt)
print(type(reg.get_active(cfg)).__name__)
"
```
