# Acceptance verification — task-ids-14-04-t02-smspm-delivery-ingest

- **Gate:** PASS
- **Wave:** pkg-000049
- **Story:** STORY-IDS-SMSPM-04-delivery-report-webhook
- **Date:** 2026-08-20T11:06:55Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| Parse `id`/`status`; do not store `toNumber` | PASS | [`delivery_ingest.py:28-46`](../../../../../../../src/core/phone/smspm/delivery_ingest.py) |
| Map D-04-2; reuse `apply_delivery_update` | PASS | `_STATUS_MAP` + handler [`handlers.py:821-826`](../../../../../../../src/core/api/handlers.py) |
| Forward-only by `provider_message_id` | PASS | telnyx `apply_delivery_update`; `test_idempotent_replay_does_not_regress_final_status` |
| Audit without phone/OTP/`toNumber` | PASS | [`handlers.py:829-836`](../../../../../../../src/core/api/handlers.py) `smspm_delivery_status_updated`; `test_delivery_audit_logged_without_pii` |
| Confirm/otp_engine not gated | PASS | no `delivery_status` in confirm path; `test_confirm_succeeds_when_delivery_status_failed` |
