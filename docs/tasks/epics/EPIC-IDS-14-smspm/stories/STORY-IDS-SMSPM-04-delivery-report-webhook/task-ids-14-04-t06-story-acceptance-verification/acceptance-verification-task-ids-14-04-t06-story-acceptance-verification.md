# Story acceptance gate — STORY-IDS-SMSPM-04-delivery-report-webhook

- **Story:** Delivery report / webhook (phase-2)
- **Package:** `pkg-000049-20260820-epic-ids-14-smspm-04-delivery-report-webhook.yaml`
- **Result:** PASS
- **Date:** 2026-08-20T11:06:55Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Статусы доставки обновляются по provider message id без изменения OTP-confirm флоу (D-04-5). | PASS | t02 ingest + `test_valid_secret_updates_delivery_status`; `test_confirm_succeeds_when_delivery_status_failed` |
| Endpoint отвечает `OK` при валидном secret; 401 при mismatch (D-04-1). | PASS | t01 GET route; `test_valid_secret_updates_delivery_status`; `test_bad_secret_returns_401_and_session_unchanged` |
| Повторные/устаревшие события идемпотентны forward-only (D-04-3). | PASS | `apply_delivery_update`; `test_idempotent_replay_does_not_regress_final_status` |
| Аудит без сырого номера/OTP (D-04-6). | PASS | `test_delivery_audit_logged_without_pii` |
| При set `SMSPM_REPORT_URL` sender передаёт `report` (D-04-4). | PASS | t03 [`sender.py:29-30`](../../../../../../../src/core/phone/smspm/sender.py); `test_smspm_send_includes_report_when_url_set` |
| Offline-тесты T06 зелёные; env задокументированы (T07). | PASS | t04 443 passed, 13 deselected; t05 `.env.example` + runbook |

## Commands (live verification 2026-08-20T11:06:55Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
cd doge-identity-service
.venv/bin/python -m pytest tests/test_smspm_delivery_webhook.py tests/test_smspm_delivery_ingest.py tests/test_smspm_config.py tests/test_smspm_sms_sender.py -q -m "not live_integration"
# 37 passed, 1 deselected
.venv/bin/python -m pytest -q -m "not live_integration"
# 443 passed, 13 deselected (2026-08-20T11:06:55Z)
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
