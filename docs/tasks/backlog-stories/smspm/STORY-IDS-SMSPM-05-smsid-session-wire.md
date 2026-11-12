# STORY-IDS-SMSPM-05 — SMSPM `smsId` = phone session id (draft)

## Meta
- **Key:** `STORY-IDS-SMSPM-05-smsid-session-wire`
- **Epic:** [`EPIC-IDS-SMSPM`](EPIC-IDS-SMSPM.md) / [`EPIC-IDS-14`](../../epics/EPIC-IDS-14-smspm/EPIC-IDS-14-smspm.md)
- **Status:** ⚪ Todo (P5 draft; optional PA.3 refine)
- **Источник:** [SMSPM-02 D-02-6](STORY-IDS-SMSPM-02-sms-sender.md); audit [`identity-smspm-02-code-audit-2026-08-20.md`](../../../analysis/identity-smspm-02-code-audit-2026-08-20.md) F2
- **Зависит от:** [SMSPM-02](STORY-IDS-SMSPM-02-sms-sender.md) 🟢 pkg-000047
- **Wave origin:** P5 `run_mode=epic_ids_14_smspm_02_audit_2026_08_20` (F2 WAIVED `out-of-DoD`)

## Зачем простыми словами
SMSPM принимает optional `smsId`. Сейчас sender умеет поле, но `/auth/phone/request` не передаёт id phone-сессии — correlating logs (message id ↔ session) без PII не работает на live path.

## Scope (outcome)
- Optional `smsId=session.id` на пути request → `SmsSenderPort.send`, без утечки OTP/hash/token/full MSISDN.
- Контракт Port и все реализации (`mock` / `file` / `telnyx` / `smspm`) совместимы.
- Offline-тесты: smspm payload + mock/file/telnyx не ломаются.

## Decisions (draft — PA.3 may lock)

| ID | Решение | Почему |
|----|---------|--------|
| **D-05-1** | `smsId` = `PhoneVerificationSession.id` (не E.164, не OTP) | D-02-6; связываемость без PII |
| **D-05-2** | Расширить `SmsSenderPort.send` optional `sms_id` **или** эквивалент, принятый всеми senders | Handler не может передать extra kwarg только smspm без лома mock/file/telnyx |
| **D-05-3** | Вне AC SMSPM-02; OTP delivery без `smsId` остаётся валидной | F2 optional recommend, не parent AC |

## Паттерн

| Что | Якорь |
|-----|-------|
| Handler call | [`handlers.py:504`](../../../../src/core/api/handlers.py) `sender.send(to_e164=…, text=…)` — нет `sms_id` |
| Port | [`base.py:42`](../../../../src/core/phone/base.py) `send(*, to_e164, text)` |
| SMSPM optional | [`sender.py:19,27-28`](../../../../src/core/phone/smspm/sender.py) |
| Session create | [`otp_engine.py`](../../../../src/core/phone/otp_engine.py) — id уже есть до send |

## Подзадачи (sketch)

- **T01 — Port + senders.** Optional `sms_id` на Protocol и mock/file/telnyx/smspm (no-op кроме smspm JSON).
- **T02 — Handler.** После `create_phone_verification_session` передать `sms_id=session.id`.
- **T03 — Tests.** smspm `smsId` в body; mock/file/telnyx regression; no PII in logs.

## Точки в коде

| Файл | Действие |
|------|----------|
| `src/core/phone/base.py` | optional arg на Port |
| `src/core/phone/{mock,file,telnyx,smspm}/` send | принять `sms_id` |
| `src/core/api/handlers.py` | передать `session.id` |
| `tests/test_smspm_sms_sender.py` + sender tests | cover + no regression |

## Вне scope
- SMSPM-02 Done / parent AC (не переоткрывать).
- Runbook ([SMSPM-03](STORY-IDS-SMSPM-03-operator-runbook-smoke.md)); webhook/`report` ([SMSPM-04](STORY-IDS-SMSPM-04-delivery-report-webhook.md)).
- SPIKE creds.

## Acceptance Criteria (draft)

- [ ] `/auth/phone/request` при `SMS_PROVIDER=smspm` кладёт `smsId=session.id` в JSON POST (D-05-1).
- [ ] `mock` / `file` / `telnyx` принимают тот же Port без регрессий (D-05-2).
- [ ] Логи без OTP/hash/token/full MSISDN; SMSPM-02 AC остаются зелёными (D-05-3).

## Парадигма-якорь
[STORY-IDS-SMSPM-02-sms-sender.md](STORY-IDS-SMSPM-02-sms-sender.md) D-02-6; [identity-smspm-02-code-audit-2026-08-20.md](../../../analysis/identity-smspm-02-code-audit-2026-08-20.md) F2.
