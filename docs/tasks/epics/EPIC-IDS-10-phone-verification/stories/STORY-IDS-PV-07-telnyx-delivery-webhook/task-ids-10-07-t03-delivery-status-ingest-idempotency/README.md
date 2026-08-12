## Task workspace — `task-ids-10-07-t03-delivery-status-ingest-idempotency`

- Story: [`../STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../STORY-IDS-PV-07-telnyx-delivery-webhook.md)
- Prerequisite: t01 session fields + `get_by_provider_message_id`

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000028`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md) Scope bullets 3–4; Story AC #1, #3; spec §2.7  
---

## Task: implement — delivery status ingest + forward-only idempotency

### Цель
Парсить Telnyx events (`message.sent` / `message.delivered` / `message.finalized`) и монотонно обновлять `delivery_status` по `provider_message_id`.

### Почему это важно
Story AC #1 и #3: обновление статуса + идемпотентность (не откатывать финальный статус).

### Факты из кода
1. Spec §2.7: статусы `queued|sent|delivered|failed|gw_timeout|dlr_timeout`; events `message.sent`, `message.delivered`, `message.finalized` ([`telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md)).
2. t01 добавляет `delivery_status` / `delivery_updated_at` на сессию (prerequisite).
3. `delivery_ingest` module **отсутствует**.

### Gap / Проблема
Нет parser + monotonic update policy для webhook payload → session.

### AC/DoD
- [x] (P0) `parse_telnyx_messaging_webhook(payload: dict) -> TelnyxDeliveryEvent` — `event_type`, `provider_message_id`, `delivery_status`, `occurred_at`.
- [x] (P0) `apply_delivery_update(store, *, provider_message_id, new_status, occurred_at)` — forward-only: final statuses (`delivered|failed|gw_timeout|dlr_timeout`) не откатываются; duplicate same status → no-op.
- [x] (P0) Unknown `provider_message_id` → no-op or explicit not-found (document choice; не 500).
- [x] (P1) Unit tests: mapper for `sent`/`delivered`/`finalized`+failed; idempotent replay; stale event ignored.

### Где менять код
- `doge-identity-service/src/core/phone/telnyx/delivery_ingest.py` (new)
- `doge-identity-service/tests/test_telnyx_delivery_ingest.py` (new)

### Out of scope
- HTTP handler (t04)
- Audit logging (t04)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_telnyx_delivery_ingest.py -q
```
