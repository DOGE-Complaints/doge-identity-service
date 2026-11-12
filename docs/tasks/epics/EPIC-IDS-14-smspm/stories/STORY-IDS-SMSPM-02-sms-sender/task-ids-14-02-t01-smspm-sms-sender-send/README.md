## Task workspace — `task-ids-14-02-t01-smspm-sms-sender-send`

- Story: [`../STORY-IDS-SMSPM-02-sms-sender.md`](../STORY-IDS-SMSPM-02-sms-sender.md)
- Prerequisite: SMSPM-01 🟢 (`SmspmSettings` + stub descriptor)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000047`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md) (T01, D-02-1, D-02-3, D-02-4, D-02-5, D-02-6)  
---

## Task: implement — `SmspmSmsSender.send` HTTP POST to SMSPM

### Цель
`src/core/phone/smspm/sender.py`: POST JSON (`hash`, `token`, `toNumber` strip `+`, `fromNumber`, `text`, optional `smsId`); parse `messages[0].id` → `provider_message_id`.

### Почему это важно
Story AC #1/#2: `/auth/phone/request` должен доставить SMS через SMSPM; при D-02-1 id попадает в сессию (handlers уже пишет `provider_message_id`).

### Факты из кода
1. Stub [`descriptor.py:19-23`](../../../../../../../src/core/phone/smspm/descriptor.py) — `SmspmSmsStub.send` raises `PROVIDER_UNAVAILABLE` («SMSPM HTTP send is not implemented»).
2. Mirror [`telnyx/sender.py:21-54`](../../../../../../../src/core/phone/telnyx/sender.py) — `TelnyxSmsSender.send` uses Bearer; SMSPM must **not** copy Bearer (D-02-4).
3. Port [`base.py:38-42`](../../../../../../../src/core/phone/base.py) — `send(*, to_e164, text) -> SmsSendResult`.
4. Session store [`handlers.py:504-506`](../../../../../../../src/core/api/handlers.py) — already copies `send_result.provider_message_id` onto the session.
5. Settings [`config.py:22-35`](../../../../../../../src/core/phone/smspm/config.py) — `hash`/`token`/`from_sender`/`api_base_url` from SMSPM-01.
6. No `src/core/phone/smspm/sender.py` on disk (glob 0).

### Gap / Проблема
HTTP POST к SMSPM API отсутствует; stub блокирует доставку OTP.

### AC/DoD
- [x] (P0) `SmspmSmsSender.send` POSTs JSON: `hash`, `token`, `toNumber` (E.164 без `+`, D-02-3), `fromNumber`, `text`; auth in body not Bearer (D-02-4).
- [x] (P0) HTTP 200 + `messages[0].id` → `SmsSendResult(accepted=True, provider_message_id=…)` (D-02-1); `"Added to queue"` is success.
- [x] (P0) MVP payload **without** `report` URL (D-02-5).
- [x] (P1) Optional `smsId` on impl (D-02-6) without changing `otp_engine.py` / Port required args.
- [x] (P1) Do not log token/hash/OTP/full MSISDN (D-02-7) in sender.

### Где менять код
- `doge-identity-service/src/core/phone/smspm/sender.py` (**new**)

### Out of scope
- `errors.py` mapping (t02)
- Descriptor `build` wire (t03)
- Tests (t04–t05)
- Runbook (SMSPM-03); webhook/`report` (SMSPM-04)

### Проверка
```bash
cd doge-identity-service
rg -n 'toNumber|fromNumber|messages' src/core/phone/smspm/sender.py
rg -n 'report|Bearer' src/core/phone/smspm/sender.py
```
