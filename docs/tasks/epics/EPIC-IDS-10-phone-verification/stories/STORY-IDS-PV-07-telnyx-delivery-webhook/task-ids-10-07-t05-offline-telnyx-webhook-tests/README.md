## Task workspace — `task-ids-10-07-t05-offline-telnyx-webhook-tests`

- Story: [`../STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../STORY-IDS-PV-07-telnyx-delivery-webhook.md)
- Prerequisite: t01–t04 implemented

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000028`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md) Story AC #5; AC #1–#4 integration evidence  
---

## Task: tests — offline Telnyx delivery webhook suite

### Цель
Offline-тесты: валидный/невалидный webhook, идемпотентность, маппинг статусов (Story AC #5 verbatim).

### Почему это важно
Story AC #5; образец e2e — [`test_phone_verification_flow.py`](../../../../../../../tests/test_phone_verification_flow.py).

### Факты из кода
1. `tests/test_telnyx_delivery_webhook.py` **отсутствует**.
2. t01–t04 provide handler + route + signature + ingest.
3. Fixture pattern: in-memory deps via `create_app` + TestClient or handler direct invoke.

### Gap / Проблема
Нет offline coverage для webhook HTTP path end-to-end.

### AC/DoD
- [x] (P0) Valid signed webhook → session `delivery_status` updated by `provider_message_id`.
- [x] (P0) Invalid/missing signature → 401 or 403; session unchanged.
- [x] (P0) Idempotent replay: duplicate event does not regress final status.
- [x] (P0) Status mapping: `message.sent` → `sent`; `message.delivered` → `delivered`; `message.finalized` + failed payload → `failed` (or spec mapping).
- [x] (P0) Audit event logged without raw phone / OTP / full payload in messages.
- [x] (P1) `pytest -m "not live_integration" -q` — 0 failed.

### Где менять код
- `doge-identity-service/tests/test_telnyx_delivery_webhook.py` (new)

### Out of scope
- Live Telnyx webhook (SPIKE-PV-08 gate)
- OpenAPI doc update

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_telnyx_delivery_webhook.py -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
