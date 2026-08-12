## Task workspace — `task-ids-10-06-t02-telnyx-sms-sender-http-send`

- Story: [`../STORY-IDS-PV-06-telnyx-sms-sender.md`](../STORY-IDS-PV-06-telnyx-sms-sender.md)
- Prerequisite: t01 (`TelnyxSettings`)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000027`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md) Scope bullet 2; [`../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md) §2  
---

## Task: implement — `TelnyxSmsSender.send` HTTP success path

### Цель
Реализовать тонкий HTTP-адаптер Telnyx Messaging API: POST `/v2/messages`, parse success → `SmsSendResult`.

### Почему это важно
Story AC #2: корректный POST + `accepted=True` + `provider_message_id` при `queued`/`sent`.

### Факты из кода
1. Port contract: [`SmsSenderPort.send`](../../../../../../../src/core/phone/base.py) → `SmsSendResult`.
2. Mock reference: [`MockSmsSender`](../../../../../../../src/core/phone/mock/sender.py).
3. eID HTTP pattern (sync httpx from runtime): [`runtime_factory.py`](../../../../../../../src/core/providers/runtime_factory.py) — `httpx.Client` injected via runtime.
4. `SmsProviderRuntime` today: only `config` ([`runtime_factory.py:7-8`](../../../../../../../src/core/phone/runtime_factory.py)) — **no httpx client yet** (t04).
5. Spec §2: `POST {base}/v2/messages`, Bearer, body `{from, to, text, type:"SMS", messaging_profile_id?}`.

### Gap / Проблема
Нет `TelnyxSmsSender`; flow calls `registry.get_active().send` ([`handlers.py`](../../../../../../../src/core/api/handlers.py)) but only mock registered.

### AC/DoD
- [ ] (P0) `TelnyxSmsSender` implements `SmsSenderPort`; constructor takes `TelnyxSettings` + `httpx.Client` (or runtime).
- [ ] (P0) `send(to_e164, text)`: `POST {base}/v2/messages` with `Authorization: Bearer {api_key}`.
- [ ] (P0) Request body: `{from, to, text, type: "SMS"}`; include `messaging_profile_id` when alphanumeric from.
- [ ] (P0) Success: HTTP 200 + `data.id` + `data.to[0].status ∈ {queued, sent}` → `SmsSendResult(accepted=True, provider_message_id=data.id)`.
- [ ] (P1) Story AC #2: evidence via unit test (t05) or inline mock httpx.
- [ ] (P1) Path: `doge-identity-service/src/core/phone/telnyx/sender.py`.

### Где менять код
- `doge-identity-service/src/core/phone/telnyx/sender.py` (new)

### Out of scope
- Error mapping → `SmsErrorCode` — t03
- Descriptor/registry — t04
- Live trial test — t05 (skip without creds)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.phone.telnyx.sender import TelnyxSmsSender; print(TelnyxSmsSender)"
```
