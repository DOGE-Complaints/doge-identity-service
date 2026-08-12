## Task workspace — `task-ids-10-07-t04-webhook-handler-route-and-audit`

- Story: [`../STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../STORY-IDS-PV-07-telnyx-delivery-webhook.md)
- Prerequisite: t02 signature verifier; t03 delivery ingest

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000028`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md) Scope bullets 1, 5; Story AC #1, #2, #4  
---

## Task: implement — webhook handler, public route, delivery audit

### Цель
`POST /webhooks/telnyx/messaging` — публичный endpoint: verify → ingest → audit без PII.

### Почему это важно
Story AC #1, #2, #4: HTTP surface + отклонение bad signature + audit event.

### Факты из кода
1. [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py) — phone routes с Bearer; публичный образец: `GET /auth/{provider}/callback` (line ~264) **без** `get_current_user`.
2. [`handlers.py:104-118`](../../../../../../../src/core/api/handlers.py) — `_log_phone_audit` pattern для `PhoneAuditEvent`.
3. `handle_telnyx_messaging_webhook` **отсутствует**.
4. `POST /webhooks/telnyx/messaging` **отсутствует**.

### Gap / Проблема
Нет handler и маршрута для Telnyx delivery webhook.

### AC/DoD
- [x] (P0) `handle_telnyx_messaging_webhook(deps, *, raw_body: bytes, headers, trace_id)` — signature verify → parse → `apply_delivery_update` → audit (`telnyx_delivery_status_updated` или канон; **no** phone/code/raw payload).
- [x] (P0) Invalid/missing signature → **401 or 403**, body not processed (Story AC #2).
- [x] (P0) Register `POST /webhooks/telnyx/messaging` in `asgi_app.py` **без** `Depends(get_current_user)`.
- [x] (P0) Success → 2xx (204 or 200).
- [x] (P1) Audit: `success=True`, `provider=telnyx`, `failure_reason` only on verify/parse failure codes (no PII).

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`
- `doge-identity-service/src/core/api/asgi_app.py`

### Out of scope
- E2E HTTP tests (t05)
- Live Telnyx webhook (SPIKE-PV-08)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.api.asgi_app import create_app; create_app()"
```
