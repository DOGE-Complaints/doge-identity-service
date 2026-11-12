## Task workspace — `task-ids-14-04-t03-smspm-sender-report-url`

- Story: [`../STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../STORY-IDS-SMSPM-04-delivery-report-webhook.md)
- Prerequisite: SMSPM-02 🟢 [`sender.py`](../../../../../../../src/core/phone/smspm/sender.py); [`t01`](../task-ids-14-04-t01-smspm-delivery-route-handler/README.md) optional secret path

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000049`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md) (T05, AC #5, D-04-4, D-04-7)  
---

## Task: implement — optional `report` on SMSPM send when `SMSPM_REPORT_URL` set

### Цель
If `SMSPM_REPORT_URL` set → include `report` in POST send JSON (URL with secret path from public API base). If unset → SMSPM-02 payload unchanged (no `report` key).

### Почему это важно
Story AC #5 / D-04-4: SMSPM only callbacks if send includes `report`; MVP without env must stay SMSPM-02.

### Факты из кода
1. Sender payload [`sender.py:20-28`](../../../../../../../src/core/phone/smspm/sender.py) — keys `hash`/`token`/`toNumber`/`fromNumber`/`text` + optional `smsId` only; **no** `report`.
2. Settings [`config.py:21-35`](../../../../../../../src/core/phone/smspm/config.py) — no `report_url`; `SMSPM_REQUIRED_ENV` is HASH/TOKEN/FROM only.
3. SA §5.1 `SMSPM_REPORT_URL` optional phase-2 ([`solution-architecture-smspm-sms-provider.md`](../../../../../../backlog-stories/smspm/solution-architecture-smspm-sms-provider.md)).
4. Guide send `report` optional ([`SMSPM_SMS_Delivery_Integration_Guide.md:1035-1046`](../../../../../../backlog-stories/inbound/SMSPM_SMS_Delivery_Integration_Guide.md)).

### Gap / Проблема
Sender не передаёт callback URL; SMSPM не сможет слать GET delivery reports.

### AC/DoD
- [x] (P0) `SmspmSettings` optional `SMSPM_REPORT_URL` (empty default); **not** in `SMSPM_REQUIRED_ENV` (D-04-7).
- [x] (P0) If set → POST JSON includes `report` (D-04-4, AC #5).
- [x] (P0) If unset → payload has no `report` key (SMSPM-02 / D-02-5 preserved).
- [x] (P1) Do not log the full report URL with secret if avoidable; never log HASH/TOKEN.

### Где менять код
- `doge-identity-service/src/core/phone/smspm/config.py`
- `doge-identity-service/src/core/phone/smspm/sender.py`

### Out of scope
- Webhook ingest (t01–t02)
- Tests (t04); `.env.example` (t05)
- Auto-retry on `failed`

### Проверка
```bash
rg -n 'SMSPM_REPORT_URL|report' doge-identity-service/src/core/phone/smspm/config.py doge-identity-service/src/core/phone/smspm/sender.py
rg -n 'SMSPM_REQUIRED_ENV' doge-identity-service/src/core/phone/smspm/config.py
```
