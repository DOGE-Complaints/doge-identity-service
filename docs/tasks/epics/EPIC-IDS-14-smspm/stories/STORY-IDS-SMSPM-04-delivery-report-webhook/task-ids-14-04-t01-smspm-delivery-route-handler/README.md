## Task workspace — `task-ids-14-04-t01-smspm-delivery-route-handler`

- Story: [`../STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../STORY-IDS-SMSPM-04-delivery-report-webhook.md)
- Prerequisite: SMSPM-02 🟢 sender; PV-07 analog Telnyx POST webhook

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000049`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md) (T01, AC #2, D-04-1, D-04-7, D-G6)  
---

## Task: implement — GET SMSPM delivery webhook route + handler

### Цель
`GET /webhooks/smspm/delivery/{shared_secret}`: mismatch → 401; valid secret → plain `200` body `OK`. Optional `SMSPM_WEBHOOK_SHARED_SECRET` on settings (**not** `SMSPM_REQUIRED_ENV`). GET + secret path — **not** Ed25519.

### Почему это важно
Story AC #2 / D-04-1: SMSPM guide uses GET query + `OK`, unlike Telnyx POST + Ed25519.

### Факты из кода
1. Telnyx route is **POST** [`asgi_app.py:395-408`](../../../../../../../src/core/api/asgi_app.py) — `handle_telnyx_messaging_webhook`; no Bearer (`get_current_user` not used).
2. Telnyx handler [`handlers.py:653-754`](../../../../../../../src/core/api/handlers.py) — Ed25519 via `verify_telnyx_webhook_signature`; missing `TELNYX_WEBHOOK_PUBLIC_KEY` → 503 `CONFIG_ERROR` (L660–667); success `return None, 204`.
3. `rg webhooks/smspm` in `src/` = 0; no `handle_smspm_*` in [`handlers.py`](../../../../../../../src/core/api/handlers.py).
4. Config [`config.py:12,21-35`](../../../../../../../src/core/phone/smspm/config.py) — `SMSPM_REQUIRED_ENV = ("SMSPM_HASH", "SMSPM_TOKEN", "SMSPM_FROM")`; `SmspmSettings` has no shared-secret field.
5. Epic D-G6 — GET query + body `OK`; shared secret in path; no Ed25519 ([`EPIC-IDS-14-smspm.md`](../../../../EPIC-IDS-14-smspm.md)).

### Gap / Проблема
Нет публичного GET webhook SMSPM; Telnyx POST/Ed25519 нельзя копировать (D-G6).

### AC/DoD
- [x] (P0) `GET /webhooks/smspm/delivery/{shared_secret}` registered; no `get_current_user` (D-04-1).
- [x] (P0) Valid secret → HTTP 200 plain body `OK` (not Telnyx 204 JSON envelope).
- [x] (P0) Secret mismatch → 401; do **not** apply session update.
- [x] (P0) Missing `SMSPM_WEBHOOK_SHARED_SECRET` → 503 `CONFIG_ERROR` (mirror Telnyx missing public key) — not Ed25519.
- [x] (P1) Optional secret field on `SmspmSettings`; **not** added to `SMSPM_REQUIRED_ENV` (D-04-7).
- [x] (P1) No Ed25519 / Telnyx signature headers on this route.

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py` (GET route)
- `doge-identity-service/src/core/api/handlers.py` (`handle_smspm_delivery_webhook`)
- `doge-identity-service/src/core/phone/smspm/config.py` (optional `SMSPM_WEBHOOK_SHARED_SECRET`)

### Out of scope
- Query parse / session update (t02)
- Sender `report` (t03)
- Tests (t04); env docs (t05)
- Gate confirm by delivery (D-04-5)

### Проверка
```bash
rg -n 'webhooks/smspm/delivery|handle_smspm_delivery' doge-identity-service/src/core/api/asgi_app.py doge-identity-service/src/core/api/handlers.py
rg -n 'SMSPM_WEBHOOK_SHARED_SECRET|SMSPM_REQUIRED_ENV' doge-identity-service/src/core/phone/smspm/config.py
rg -n 'Ed25519|verify_telnyx' doge-identity-service/src/core/api/handlers.py | head
```
