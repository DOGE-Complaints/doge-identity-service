## Task workspace — `task-ids-14-02-t02-smspm-error-mapping`

- Story: [`../STORY-IDS-SMSPM-02-sms-sender.md`](../STORY-IDS-SMSPM-02-sms-sender.md)
- Prerequisite: [`t01`](../task-ids-14-02-t01-smspm-sms-sender-send/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000047`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md) (T02, D-02-2, D-02-7)  
---

## Task: implement — SMSPM `errors.py` mapping D-02-2

### Цель
`src/core/phone/smspm/errors.py`: map HTTP/timeout to existing `SmsErrorCode` (D-02-2); timeout → `PROVIDER_UNAVAILABLE`.

### Почему это важно
Story AC #3: ошибки мапятся по D-02-2; auth не раскрывать клиенту; секреты не в логах (D-02-7).

### Факты из кода
1. Mirror [`telnyx/errors.py:52-60`](../../../../../../../src/core/phone/telnyx/errors.py) — `map_telnyx_error` / `map_telnyx_timeout` → `SmsSenderError` + `SmsErrorCode`.
2. Codes [`base.py:8-17`](../../../../../../../src/core/phone/base.py) — `INVALID_PHONE`, `PROVIDER_UNAVAILABLE`, `SEND_FAILED`, `UNKNOWN` already exist.
3. No `src/core/phone/smspm/errors.py` on disk (glob 0).

### Gap / Проблема
Нет SMSPM-специфичного mapping 401 / invalid phone / 5xx / timeout.

### AC/DoD
- [x] (P0) 401 → `SEND_FAILED`.
- [x] (P0) invalid phone string → `INVALID_PHONE`.
- [x] (P0) 5xx / timeout → `PROVIDER_UNAVAILABLE`.
- [x] (P0) else `SEND_FAILED` / `UNKNOWN` (D-02-2).
- [x] (P1) Mapping messages/logs must not include hash/token/OTP/full MSISDN (D-02-7).

### Где менять код
- `doge-identity-service/src/core/phone/smspm/errors.py` (**new**)
- `doge-identity-service/src/core/phone/smspm/sender.py` (call mapper — t01 file)

### Out of scope
- Descriptor wire (t03)
- Tests (t04)
- New `SmsErrorCode` values

### Проверка
```bash
cd doge-identity-service
rg -n 'SEND_FAILED|INVALID_PHONE|PROVIDER_UNAVAILABLE' src/core/phone/smspm/errors.py
```
