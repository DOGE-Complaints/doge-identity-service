## Task workspace — `task-ids-10-07-t01-session-delivery-fields-and-message-id-persist`

- Story: [`../STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../STORY-IDS-PV-07-telnyx-delivery-webhook.md)
- Prerequisite: STORY-IDS-PV-03, PV-05, PV-06 Done

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000028`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md) Scope bullet 3; prerequisite для Story AC #1  
---

## Task: implement — session delivery fields + `provider_message_id` persist

### Цель
Расширить `PhoneVerificationSession` полями доставки и закрыть gap: после `send` сохранять `provider_message_id` для webhook lookup.

### Почему это важно
Story Scope: связать `delivery_status` с `PhoneVerificationSession.provider_message_id` (PV-03). Сейчас `handle_phone_request` отбрасывает `SmsSendResult` — webhook не сможет найти сессию.

### Факты из кода
1. [`models.py:68-79`](../../../../../../../src/core/domain/models.py) — `PhoneVerificationSession` имеет `provider_message_id`, **нет** `delivery_status` / `delivery_updated_at`.
2. [`contracts.py:73-82`](../../../../../../../src/core/domain/contracts.py) — store **нет** `get_by_provider_message_id`.
3. [`repositories.py:283-320`](../../../../../../../src/core/infrastructure/repositories.py) — in-memory store без lookup по message id.
4. [`handlers.py:468-478`](../../../../../../../src/core/api/handlers.py) — `sender.send(...)` без сохранения `provider_message_id`.
5. [`otp_engine.py:61`](../../../../../../../src/core/phone/otp_engine.py) — сессия создаётся с `provider_message_id=None`.

### Gap / Проблема
Нет полей доставки; `provider_message_id` не персистится после SMS send — blocker для webhook AC #1.

### AC/DoD
- [x] (P0) `PhoneVerificationSession`: `delivery_status: str | None`, `delivery_updated_at: datetime | None` (канон: `queued|sent|delivered|failed|gw_timeout|dlr_timeout`).
- [x] (P0) `PhoneVerificationSessionStore.get_by_provider_message_id(provider_message_id) -> PhoneVerificationSession | None`.
- [x] (P0) `handle_phone_request`: после успешного `send` → `store.replace` с `provider_message_id` из `SmsSendResult`.
- [x] (P1) Обновить все конструкторы `PhoneVerificationSession` (`otp_engine.py`, tests).
- [x] (P1) `tests/test_phone_verification_flow.py` — assert `provider_message_id` set when mock returns id.

### Где менять код
- `doge-identity-service/src/core/domain/models.py`
- `doge-identity-service/src/core/domain/contracts.py`
- `doge-identity-service/src/core/infrastructure/repositories.py`
- `doge-identity-service/src/core/api/handlers.py`
- `doge-identity-service/src/core/phone/otp_engine.py`
- `doge-identity-service/tests/test_phone_verification_flow.py`

### Out of scope
- Webhook signature / HTTP route (t02–t04)
- Supabase persistence migration (in-memory MVP per PV-03)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_phone_verification_flow.py -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
