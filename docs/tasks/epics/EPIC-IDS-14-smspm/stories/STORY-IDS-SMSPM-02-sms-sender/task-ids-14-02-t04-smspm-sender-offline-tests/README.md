## Task workspace — `task-ids-14-02-t04-smspm-sender-offline-tests`

- Story: [`../STORY-IDS-SMSPM-02-sms-sender.md`](../STORY-IDS-SMSPM-02-sms-sender.md)
- Prerequisite: [`t01`](../task-ids-14-02-t01-smspm-sms-sender-send/README.md), [`t02`](../task-ids-14-02-t02-smspm-error-mapping/README.md), [`t03`](../task-ids-14-02-t03-smspm-descriptor-wire/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000047`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md) (T04, D-02-1, D-02-2, D-02-7)  
---

## Task: tests — SMSPM sender offline mock HTTP

### Цель
Offline-тесты с mock HTTP: success; 401; invalid phone; 5xx; missing id; assert no secrets/OTP/full MSISDN in log capture.

### Почему это важно
Story AC #3/#4/#5: mapping + log hygiene + no regression for mock/file/telnyx (existing suite still green).

### Факты из кода
1. Mirror [`tests/test_telnyx_sms_sender.py`](../../../../../../../tests/test_telnyx_sms_sender.py) — mock HTTP + live marker later in file.
2. Config tests already exist [`tests/test_smspm_config.py`](../../../../../../../tests/test_smspm_config.py) (SMSPM-01; do not replace).
3. No `tests/test_smspm_sms_sender.py` on disk (glob 0).

### Gap / Проблема
Нет offline coverage send/errors/logs для SMSPM HTTP.

### AC/DoD
- [x] (P0) success (200 + `messages[0].id`) → accepted + `provider_message_id`.
- [x] (P0) 401 → `SEND_FAILED`; invalid phone → `INVALID_PHONE`; 5xx → `PROVIDER_UNAVAILABLE`; missing id → fail mapping (`SEND_FAILED`/`UNKNOWN`).
- [x] (P0) log capture: no hash/token/OTP/full MSISDN (D-02-7).
- [x] (P1) Payload has no `report` field (D-02-5).
- [x] (P1) Existing `test_smspm_config.py` + mock/file/telnyx tests remain green (run in t06 too).

### Где менять код
- `doge-identity-service/tests/test_smspm_sms_sender.py` (**new**)

### Out of scope
- Live network (t05)
- SPIKE creds
- Runbook

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_smspm_sms_sender.py -q -m "not live_integration"
```
