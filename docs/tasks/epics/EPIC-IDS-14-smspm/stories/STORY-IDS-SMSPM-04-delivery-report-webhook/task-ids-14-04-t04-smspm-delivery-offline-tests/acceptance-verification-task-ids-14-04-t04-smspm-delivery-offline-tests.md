# Acceptance verification — task-ids-14-04-t04-smspm-delivery-offline-tests

- **Gate:** PASS
- **Wave:** pkg-000049
- **Story:** STORY-IDS-SMSPM-04-delivery-report-webhook
- **Date:** 2026-08-20T11:06:55Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| Happy-path GET → `OK` + status update | PASS | `test_valid_secret_updates_delivery_status` |
| Bad secret → 401 | PASS | `test_bad_secret_returns_401_and_session_unchanged` |
| Idempotent replay / stale | PASS | `test_idempotent_replay_does_not_regress_final_status` |
| Confirm 200 when `delivery_status=failed` | PASS | `test_confirm_succeeds_when_delivery_status_failed` |
| Audit without PII | PASS | `test_delivery_audit_logged_without_pii` |
| `report` when env set | PASS | `test_smspm_send_includes_report_when_url_set` |
| Full offline suite green | PASS | `.venv/bin/python -m pytest -q -m "not live_integration"` → **443 passed, 13 deselected** |
