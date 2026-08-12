## Task workspace — `task-ids-10-06-t03-telnyx-error-code-mapping`

- Story: [`../STORY-IDS-PV-06-telnyx-sms-sender.md`](../STORY-IDS-PV-06-telnyx-sms-sender.md)
- Prerequisite: t02 (`TelnyxSmsSender` skeleton)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000027`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md) Scope bullet 3; [`../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md) §3  
---

## Task: implement — Telnyx error → `SmsErrorCode` mapping

### Цель
Маппинг Telnyx API errors в канон `SmsErrorCode`; raise `SmsSenderError`; no PII in logs.

### Почему это важно
Story AC #3: ошибки по таблице спеки; сырой код/номер не логируется.

### Факты из кода
1. `SmsErrorCode` enum: [`base.py`](../../../../../../../src/core/phone/base.py).
2. `SmsSenderError`: same module — `code: SmsErrorCode`.
3. Spec §3 table: `40309/40331→COUNTRY_NOT_ALLOWED`; `429/10011/40318→RATE_LIMITED`; `5xx/timeout→PROVIDER_UNAVAILABLE`; invalid phone→`INVALID_PHONE`; config/sender/content→`SEND_FAILED`; missing `data.id`/unknown→`UNKNOWN`.
4. Telnyx error shape: `errors[].code`, `title`, `detail` (spec §3).
5. Handler already maps `SmsSenderError` → API envelope ([`handlers.py`](../../../../../../../src/core/api/handlers.py)).

### Gap / Проблема
`TelnyxSmsSender` has no error parsing; non-200 responses unhandled.

### AC/DoD
- [ ] (P0) Map Telnyx error codes per spec §3 (see table above).
- [ ] (P0) HTTP 5xx and `httpx` timeout → `PROVIDER_UNAVAILABLE`.
- [ ] (P0) Missing `data.id` on 200 or unmapped error → `UNKNOWN`.
- [ ] (P0) Raise `SmsSenderError(code=...)` — never log raw phone, OTP, or full API key.
- [ ] (P1) Story AC #3: log messages use `SmsErrorCode` or sanitized provider code only.
- [ ] (P1) Path: `doge-identity-service/src/core/phone/telnyx/errors.py` (or co-located in `sender.py` — fix in implementation).

### Где менять код
- `doge-identity-service/src/core/phone/telnyx/errors.py` (new, preferred)
- `doge-identity-service/src/core/phone/telnyx/sender.py` (integrate)

### Out of scope
- Webhook delivery status — PV-07
- Config validation errors — t01 (`ConfigError`, not `SmsSenderError`)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.phone.telnyx.errors import map_telnyx_error; print(map_telnyx_error)"
```
