## Task workspace — `task-ids-14-03-t01-runbook-mode-c-env-table`

- Story: [`../STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../STORY-IDS-SMSPM-03-operator-runbook-smoke.md)
- Prerequisite: SMSPM-01 🟢 env names in `.env.example`; SMSPM-02 🟢 sender (product already Done)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000048`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md) (T01, AC #1, D-03-1)  
---

## Task: add — runbook mode C env checklist (`SMS_PROVIDER=smspm`)

### Цель
В существующем [`phone-sms-verification.md`](../../../../../../runbook/phone-sms-verification.md) появится режим C: intro A/B/**C** и env-таблица `SMS_PROVIDER=smspm` + `SMSPM_HASH` / `SMSPM_TOKEN` / `SMSPM_FROM` / optional `SMSPM_API_BASE_URL` **без значений секретов**. Не новый файл (D-03-1).

### Почему это важно
Story AC #1: оператор должен видеть чеклист включения SMSPM в том же SSOT, что mock/Telnyx.

### Факты из кода
1. Runbook intro [`phone-sms-verification.md:4`](../../../../../../runbook/phone-sms-verification.md) — «Два режима: **A — mock** … и **B — live Telnyx**»; нет режима C / `smspm`.
2. §2 ядро [`phone-sms-verification.md:35`](../../../../../../runbook/phone-sms-verification.md) — `SMS_PROVIDER=mock                 # mock | telnyx` (нет `smspm`).
3. §2 есть только «Режим B» Telnyx ([`phone-sms-verification.md:44-51`](../../../../../../runbook/phone-sms-verification.md)); блока SMSPM нет.
4. Имена env уже в [`.env.example:60,80-84`](../../../../../../../.env.example) — `mock | file | telnyx | smspm`; `SMSPM_HASH`/`TOKEN`/`FROM` пустые; `SMSPM_API_BASE_URL=https://api.smspm.com`.
5. Обязательные + optional base [`config.py:10-12,30-35`](../../../../../../../src/core/phone/smspm/config.py) — `SMSPM_REQUIRED_ENV`; `SMSPM_API_BASE_URL` default `https://api.smspm.com`.
6. SA §5.1 — HASH/TOKEN/FROM + optional `SMSPM_API_BASE_URL`; `SMSPM_REPORT_URL` = phase-2 (не T01).

### Gap / Проблема
Операторский runbook не документирует `SMS_PROVIDER=smspm` и обязательные `SMSPM_*`, хотя config уже принимает их.

### AC/DoD
- [x] (P0) Intro описывает режимы A (mock), B (Telnyx), **C (smspm)** — без удаления B (D-03-2).
- [x] (P0) §2 содержит env-чеклист режима C: `SMS_PROVIDER=smspm`, `SMSPM_HASH`, `SMSPM_TOKEN`, `SMSPM_FROM`, optional `SMSPM_API_BASE_URL` (имена, без секретов).
- [x] (P1) Не добавлять `SMSPM_REPORT_URL` (SMSPM-04).
- [x] (P1) Не создавать второй runbook-файл (D-03-1). Не править `src/`.

### Где менять код
- `doge-identity-service/docs/runbook/phone-sms-verification.md` only (intro + §2 mode C)

### Out of scope
- Curl smoke шаги (t02)
- Troubleshooting rows (t03)
- Live execute (t04)
- Product `src/`

### Проверка
```bash
rg -n 'режим C|Режим C|SMS_PROVIDER=smspm|SMSPM_HASH|SMSPM_API_BASE_URL' doge-identity-service/docs/runbook/phone-sms-verification.md
rg -n 'SMSPM_REPORT_URL' doge-identity-service/docs/runbook/phone-sms-verification.md
```
