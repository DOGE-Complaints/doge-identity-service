## Task workspace — `task-ids-14-02-t03-smspm-descriptor-wire`

- Story: [`../STORY-IDS-SMSPM-02-sms-sender.md`](../STORY-IDS-SMSPM-02-sms-sender.md)
- Prerequisite: [`t01`](../task-ids-14-02-t01-smspm-sms-sender-send/README.md), [`t02`](../task-ids-14-02-t02-smspm-error-mapping/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000047`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md) (T03); D-01-4 HTTP client already via `_needs_sms_http_client`  
---

## Task: implement — descriptor `build` → `SmspmSmsSender`

### Цель
Заменить stub: `SMSPM_SMS_DESCRIPTOR.build` возвращает `SmspmSmsSender` с `runtime.http_client` (уже создаётся для non-mock/file).

### Почему это важно
Story AC #1: путь request → `SmsSenderPort.send` должен вызывать реальный POST, не stub.

### Факты из кода
1. Stub build [`descriptor.py:26-30`](../../../../../../../src/core/phone/smspm/descriptor.py) — `_build_smspm_sms_sender` returns `SmspmSmsStub()`.
2. Telnyx wire [`telnyx/descriptor.py:10-16`](../../../../../../../src/core/phone/telnyx/descriptor.py) — requires `runtime.http_client`.
3. HTTP gate [`runtime_factory.py:14-15,31-32`](../../../../../../../src/core/phone/runtime_factory.py) — `_needs_sms_http_client` = `sms_provider not in {"mock","file"}`; do **not** add allow-list.

### Gap / Проблема
Registry всё ещё собирает stub; HTTP send недостижим с `SMS_PROVIDER=smspm`.

### AC/DoD
- [x] (P0) `_build_smspm_sms_sender` returns `SmspmSmsSender(settings=…, http_client=runtime.http_client)`.
- [x] (P0) Missing http_client → RuntimeError (mirror Telnyx).
- [x] (P0) `SmspmSmsStub` removed or unused.
- [x] (P1) Do not change `_needs_sms_http_client` allow-list.

### Где менять код
- `doge-identity-service/src/core/phone/smspm/descriptor.py`

### Out of scope
- `registry_builder.py` append (already SMSPM-01)
- Tests (t04)
- OTP engine / handlers rewrite

### Проверка
```bash
cd doge-identity-service
rg -n 'SmspmSmsSender|SmspmSmsStub|http_client' src/core/phone/smspm/descriptor.py
```
