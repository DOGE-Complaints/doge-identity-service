## Task workspace — `task-ids-14-04-t04-smspm-delivery-offline-tests`

- Story: [`../STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../STORY-IDS-SMSPM-04-delivery-report-webhook.md)
- Prerequisite: [`t01`](../task-ids-14-04-t01-smspm-delivery-route-handler/README.md), [`t02`](../task-ids-14-04-t02-smspm-delivery-ingest/README.md), [`t03`](../task-ids-14-04-t03-smspm-sender-report-url/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000049`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md) (T06, AC #1/#2/#3/#5/#6)  
---

## Task: tests — SMSPM delivery webhook + report offline

### Цель
Offline tests: happy-path status update; 401 bad secret; idempotent replay; confirm path unchanged when `delivery_status=failed` (D-04-5); `report` in send payload when env set.

### Почему это важно
Story AC #6 T06 + AC #1 ungated confirm: без live SMSPM; зеркало PV-07 tests, но GET + secret path.

### Факты из кода
1. Mirror [`tests/test_telnyx_delivery_webhook.py`](../../../../../../../tests/test_telnyx_delivery_webhook.py) — happy / invalid signature 401 / idempotent replay / audit without PII (`test_delivery_audit_logged_without_pii`).
2. Ingest unit [`tests/test_telnyx_delivery_ingest.py`](../../../../../../../tests/test_telnyx_delivery_ingest.py) — `apply_delivery_update` replay/unknown id.
3. Sender tests [`tests/test_smspm_sms_sender.py`](../../../../../../../tests/test_smspm_sms_sender.py) exist (SMSPM-02); extend or add sibling for `report`.
4. `rg webhooks/smspm` in `tests/` = 0.
5. Confirm handler [`handlers.py:537-635`](../../../../../../../src/core/api/handlers.py) ignores `delivery_status`.

### Gap / Проблема
Нет offline coverage GET SMSPM webhook / 401 secret / forward-only / ungated confirm / optional `report`.

### AC/DoD
- [x] (P0) Happy-path GET valid secret → `OK` + `delivery_status` updated by provider message id (AC #1/#2).
- [x] (P0) Bad secret → 401; session unchanged (AC #2).
- [x] (P0) Idempotent replay / stale status does not regress final (AC #3, D-04-3).
- [x] (P0) Confirm still 200 when session `delivery_status=failed` (D-04-5, AC #1).
- [x] (P0) Audit capture has no plaintext phone/OTP/`toNumber` (AC #4).
- [x] (P0) `SMSPM_REPORT_URL` set → send JSON includes `report`; unset → no `report` key (AC #5).
- [x] (P1) `.venv/bin/python -m pytest -q -m "not live_integration"` green (P3).

### Где менять код
- `doge-identity-service/tests/` (**new** webhook tests; sender `report` cases)

### Out of scope
- Live SMSPM network
- Env docs (t05)
- Ed25519 tests (Telnyx suite stays)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_smspm_delivery_webhook.py tests/test_smspm_sms_sender.py -q -m "not live_integration"
```
