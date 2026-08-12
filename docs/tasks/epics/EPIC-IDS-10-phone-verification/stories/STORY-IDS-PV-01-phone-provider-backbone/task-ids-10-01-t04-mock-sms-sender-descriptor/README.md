## Task workspace — `task-ids-10-01-t04-mock-sms-sender-descriptor`

- Story: [`../STORY-IDS-PV-01-phone-provider-backbone.md`](../STORY-IDS-PV-01-phone-provider-backbone.md)
- Prerequisite: t03 (`build_sms_registry` skeleton)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000022`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md) Scope; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §3  
---

## Task: implement — `MockSmsSender` + mock descriptor (эталон)

### Цель
Реализовать `MockSmsSender` (in-memory/log capture, всегда `accepted=True`) и зарегистрировать через `SmsProviderDescriptor` в `ALL_SMS_PROVIDER_DESCRIPTORS` — Story Scope bullet 5, AC #2.

### Почему это важно
Mock — эталон plugin registration для Telnyx (PV-06) и offline dev без сети; зеркало [`mock/descriptor.py`](../../../../../../../src/core/providers/mock/descriptor.py).

### Факты из кода
1. eID mock эталон: [`mock/mock_provider.py`](../../../../../../../src/core/providers/mock/mock_provider.py), [`mock/descriptor.py:20-24`](../../../../../../../src/core/providers/mock/descriptor.py).
2. `build_sms_registry` из t03 ожидает `MOCK_SMS_DESCRIPTOR` в descriptor tuple.
3. Architecture §3: провайдер тонкий — только `send`; OTP generation не в провайдере.
4. t01 `SmsSenderPort.send(*, to_e164, text) -> SmsSendResult`.

### Gap / Проблема
Нет mock SMS sender; реестр не может собрать `mock` provider instance.

### AC/DoD
- [x] (P0) `MockSmsSender` implements `SmsSenderPort`; `send` returns `SmsSendResult(accepted=True, ...)`.
- [x] (P0) In-memory capture of sent messages (list or log) for test assertions.
- [x] (P0) `MOCK_SMS_DESCRIPTOR` wraps `MockSmsSender.build(runtime)` pattern.
- [x] (P0) `MOCK_SMS_DESCRIPTOR` registered in `ALL_SMS_PROVIDER_DESCRIPTORS`; `build_sms_registry` yields active + `mock`.
- [x] (P1) Story AC #2 traceability (mock via descriptor; registry builds active + mock).

### Где менять код
- `doge-identity-service/src/core/phone/mock/mock_sender.py` (new)
- `doge-identity-service/src/core/phone/mock/descriptor.py` (new)
- `doge-identity-service/src/core/phone/mock/__init__.py` (new)
- `doge-identity-service/src/core/phone/registry_builder.py` (append `MOCK_SMS_DESCRIPTOR`)

### Out of scope
- Telnyx adapter — PV-06
- HTTP client creation policy — minimal in runtime; full factory wire PV-05
- Offline test file — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "
from types import SimpleNamespace
from core.phone.registry_builder import build_sms_registry
from core.phone.runtime import SmsProviderRuntime
from core.config.schema import load_config
cfg = load_config()
rt = SmsProviderRuntime(config=cfg, http_client=None, settings={})
reg = build_sms_registry(rt)
m = reg.get('mock')
print(m.send(to_e164='+37255555555', text='123456'))
"
```
