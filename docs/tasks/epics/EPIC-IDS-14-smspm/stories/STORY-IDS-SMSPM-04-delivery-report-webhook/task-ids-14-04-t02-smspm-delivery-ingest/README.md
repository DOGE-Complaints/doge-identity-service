## Task workspace — `task-ids-14-04-t02-smspm-delivery-ingest`

- Story: [`../STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../STORY-IDS-SMSPM-04-delivery-report-webhook.md)
- Prerequisite: [`t01`](../task-ids-14-04-t01-smspm-delivery-route-handler/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000049`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md) (T02–T04, AC #1/#3/#4, D-04-2, D-04-3, D-04-5, D-04-6)  
---

## Task: implement — parse/map SMSPM delivery query; forward-only session update; audit without phone

### Цель
Parse GET query `id`/`status`; omit storing `toNumber` plaintext; map to `CANONICAL_DELIVERY_STATUSES`; `apply_delivery_update` forward-only by `provider_message_id`; audit event without phone/OTP.

### Почему это важно
Story AC #1/#3/#4: observability statuses without gating OTP confirm (D-04-5) and without PII in audit (D-04-6).

### Факты из кода
1. Glob `src/core/phone/smspm/delivery_ingest.py` = 0; package files = `__init__.py`, `config.py`, `descriptor.py`, `sender.py`, `errors.py`.
2. Canonical + ranks [`telnyx/delivery_ingest.py:10-23,71-100`](../../../../../../../src/core/phone/telnyx/delivery_ingest.py) — `CANONICAL_DELIVERY_STATUSES`; `apply_delivery_update` noop if equal / final / `new_rank < current_rank`.
3. Confirm ungated: [`handlers.py:537-635`](../../../../../../../src/core/api/handlers.py) `handle_phone_confirm` has **no** `delivery_status`; [`otp_engine.py`](../../../../../../../src/core/phone/otp_engine.py) `rg delivery_status` = 0.
4. Session field [`models.py:80`](../../../../../../../src/core/domain/models.py) `delivery_status`; persist [`db_supabase.py:692,712`](../../../../../../../src/core/infrastructure/db_supabase.py).
5. Audit logger [`handlers.py:112-140`](../../../../../../../src/core/api/handlers.py) `_log_phone_audit` — no phone field; Telnyx uses `event_type="telnyx_delivery_status_updated"`.
6. Guide query [`SMSPM_SMS_Delivery_Integration_Guide.md:1056-1065`](../../../../../../backlog-stories/inbound/SMSPM_SMS_Delivery_Integration_Guide.md) — `id`, `status` (`submitted`/`delivered`/`failed`), `toNumber`.
7. Map (D-04-2, existing vocabulary only): `queued`→`queued`; `submitted`→`sent`; `delivered`→`delivered`; `failed`→`failed`.

### Gap / Проблема
Нет parse/map SMSPM GET callback; нельзя форкать вторую схему статусов; `toNumber` из query нельзя писать в audit plaintext.

### AC/DoD
- [x] (P0) New `src/core/phone/smspm/delivery_ingest.py` parses `id`/`status`; does **not** store `toNumber` (T02, D-04-6).
- [x] (P0) Map D-04-2 into `CANONICAL_DELIVERY_STATUSES`; reuse `apply_delivery_update` (do not fork ranks) (T03, D-04-3).
- [x] (P0) Session `delivery_status` updates by `provider_message_id`; replay/stale → noop forward-only (AC #1/#3).
- [x] (P0) Audit event analog of Telnyx delivery update: no plaintext phone/OTP/`toNumber` (T04, AC #4).
- [x] (P1) Do **not** add delivery check to `handle_phone_confirm` / `otp_engine.py` (D-04-5).

### Где менять код
- `doge-identity-service/src/core/phone/smspm/delivery_ingest.py` (**new** — parse/map)
- `doge-identity-service/src/core/api/handlers.py` (wire ingest + `_log_phone_audit`)

### Out of scope
- Route 401/OK (t01)
- Sender `report` (t03)
- Tests (t04)
- Ed25519

### Проверка
```bash
rg -n 'apply_delivery_update|CANONICAL_DELIVERY_STATUSES|toNumber' doge-identity-service/src/core/phone/smspm/delivery_ingest.py
rg -n 'delivery_status' doge-identity-service/src/core/phone/otp_engine.py doge-identity-service/src/core/api/handlers.py
```
