# Story acceptance gate — STORY-IDS-SMSPM-02-sms-sender

- **Story:** SMSPM SMS sender (доставка OTP)
- **Package:** `pkg-000047-20260820-epic-ids-14-smspm-02-sms-sender.yaml`
- **Result:** PASS
- **Date:** 2026-08-20T10:27:17Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| При `SMS_PROVIDER=smspm` и валидных creds `POST /auth/phone/request` доставляет SMS через SMSPM; ответ клиенту без кода. | PASS | t01 [`sender.py`](../../../../../../../src/core/phone/smspm/sender.py) + t03 [`descriptor.py:10-16`](../../../../../../../src/core/phone/smspm/descriptor.py); [`handlers.py:494-504`](../../../../../../../src/core/api/handlers.py) `get_active` → `send`; client payload [`handlers.py:530-534`](../../../../../../../src/core/api/handlers.py) `sent`/`expires_at` only |
| При успехе (D-02-1) provider message id сохраняется в phone-сессии. | PASS | t01 `SmsSendResult.provider_message_id`; [`handlers.py:505-507`](../../../../../../../src/core/api/handlers.py) copies onto session |
| Ошибки мапятся по D-02-2; секреты/OTP/full MSISDN не в логах (D-02-7). | PASS | t02 [`errors.py`](../../../../../../../src/core/phone/smspm/errors.py); t04 `test_smspm_send_does_not_log_secrets_otp_or_msisdn` |
| Offline-тесты (T04) зелёные; live (T05) skip без creds и проходит после SPIKE. | PASS | t04 22 passed on smspm slice; t05 live `1 skipped` without `SMSPM_*` |
| `SMS_PROVIDER=mock\|file\|telnyx` без регрессий; MVP без `report` (D-02-5). | PASS | full offline 428 passed, 13 deselected; t01/t04 payload has no `report` |

## Commands (live verification 2026-08-20T10:27:17Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
cd doge-identity-service
.venv/bin/pytest tests/test_smspm_sms_sender.py tests/test_smspm_config.py -q -m "not live_integration"
# 22 passed, 1 deselected
.venv/bin/pytest tests/test_smspm_sms_sender.py -q -m live_integration
# 1 skipped, 11 deselected
.venv/bin/pytest -q -m "not live_integration"
# 428 passed, 13 deselected (2026-08-20T10:27:17Z)
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
