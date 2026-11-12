# Acceptance verification — task-ids-14-02-t04-smspm-sender-offline-tests

- **Gate:** PASS
- **Wave:** pkg-000047
- **Story:** STORY-IDS-SMSPM-02-sms-sender
- **Date:** 2026-08-20T10:27:17Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| success 200 + `messages[0].id` → accepted + id | PASS | `test_smspm_send_success_queued` |
| 401 → `SEND_FAILED`; invalid phone → `INVALID_PHONE`; 5xx → `PROVIDER_UNAVAILABLE`; missing id → `UNKNOWN` | PASS | `test_smspm_send_maps_*`; `test_smspm_send_missing_message_id_maps_unknown` |
| log capture: no hash/token/OTP/full MSISDN | PASS | `test_smspm_send_does_not_log_secrets_otp_or_msisdn` |
| Payload has no `report` | PASS | `test_smspm_send_success_queued` asserts `"report" not in body` |
| Existing config + mock/file/telnyx remain green | PASS | `tests/test_smspm_config.py` 11 passed; full offline 428 passed, 13 deselected |

Commands: `.venv/bin/pytest tests/test_smspm_sms_sender.py tests/test_smspm_config.py -q -m "not live_integration"` → 22 passed, 1 deselected (2026-08-20T10:27:17Z)
