# Acceptance verification — task-ids-14-04-t03-smspm-sender-report-url

- **Gate:** PASS
- **Wave:** pkg-000049
- **Story:** STORY-IDS-SMSPM-04-delivery-report-webhook
- **Date:** 2026-08-20T11:06:55Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| Optional `SMSPM_REPORT_URL` not in `SMSPM_REQUIRED_ENV` | PASS | [`config.py:12,28,38`](../../../../../../../src/core/phone/smspm/config.py) |
| If set → POST JSON `report` | PASS | [`sender.py:29-30`](../../../../../../../src/core/phone/smspm/sender.py); `test_smspm_send_includes_report_when_url_set` |
| If unset → no `report` key | PASS | [`sender.py:27-30`](../../../../../../../src/core/phone/smspm/sender.py); `test_smspm_send_success_queued` |
