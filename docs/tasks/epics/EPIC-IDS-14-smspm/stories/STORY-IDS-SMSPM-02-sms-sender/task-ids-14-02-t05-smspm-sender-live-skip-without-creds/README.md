## Task workspace — `task-ids-14-02-t05-smspm-sender-live-skip-without-creds`

- Story: [`../STORY-IDS-SMSPM-02-sms-sender.md`](../STORY-IDS-SMSPM-02-sms-sender.md)
- Prerequisite: [`t04`](../task-ids-14-02-t04-smspm-sender-offline-tests/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000047`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-02-sms-sender.md) (T05); SPIKE-01 ops out of queue  
---

## Task: tests — live SMSPM send skip-without-creds

### Цель
Live test: `@pytest.mark.live_integration` + skip-without-creds; проходит после SPIKE (не в этой очереди).

### Почему это важно
Story AC #4: live (T05) skip без creds и проходит после SPIKE. Do **not** invent SPIKE tasks.

### Факты из кода
1. Telnyx pattern [`test_telnyx_sms_sender.py:251-256`](../../../../../../../tests/test_telnyx_sms_sender.py) — skip if `TELNYX_API_KEY` / `TELNYX_MESSAGING_PROFILE_ID` unset.
2. SMSPM required env [`config.py:12`](../../../../../../../src/core/phone/smspm/config.py) — `SMSPM_HASH`, `SMSPM_TOKEN`, `SMSPM_FROM`.
3. Offline suite marker: pytest `-m "not live_integration"` used by identity profile.

### Gap / Проблема
Нет live-marked SMSPM send test with skip-without-creds.

### AC/DoD
- [x] (P0) Live test marked `live_integration`.
- [x] (P0) Skip if `SMSPM_HASH` / `SMSPM_TOKEN` / `SMSPM_FROM` missing (no fail in default CI).
- [x] (P1) Default `pytest -m "not live_integration"` still excludes this test.
- [x] (P1) No SPIKE task folder; no secrets committed.

### Где менять код
- `doge-identity-service/tests/test_smspm_sms_sender.py` (live test in same file as t04)

### Out of scope
- SPIKE account setup
- Runbook smoke (SMSPM-03)
- Committing `.env` secrets

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_smspm_sms_sender.py -q -m "not live_integration"
.venv/bin/python -m pytest tests/test_smspm_sms_sender.py -q -m live_integration
# expected: skipped without SMSPM_* creds
```
