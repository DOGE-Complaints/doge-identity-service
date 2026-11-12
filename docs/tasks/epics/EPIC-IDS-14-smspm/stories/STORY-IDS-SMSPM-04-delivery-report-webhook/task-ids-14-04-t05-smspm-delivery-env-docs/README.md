## Task workspace — `task-ids-14-04-t05-smspm-delivery-env-docs`

- Story: [`../STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../STORY-IDS-SMSPM-04-delivery-report-webhook.md)
- Prerequisite: [`t01`](../task-ids-14-04-t01-smspm-delivery-route-handler/README.md), [`t03`](../task-ids-14-04-t03-smspm-sender-report-url/README.md)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000049`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-04-delivery-report-webhook.md) (T07, AC #6, D-04-7)  
---

## Task: add — document `SMSPM_WEBHOOK_SHARED_SECRET` and `SMSPM_REPORT_URL`

### Цель
Document env names in `.env.example` and runbook pointer: `SMSPM_WEBHOOK_SHARED_SECRET`, `SMSPM_REPORT_URL`. No secret values. GET webhook row in endpoint table.

### Почему это важно
Story AC #6 T07: оператор должен увидеть phase-2 env рядом с HASH/TOKEN/FROM, без второго runbook-файла.

### Факты из кода
1. [`.env.example:80-84`](../../../../../../../.env.example) — HASH/TOKEN/FROM/`API_BASE_URL` only; Telnyx has `TELNYX_WEBHOOK_PUBLIC_KEY` L78.
2. Runbook [`phone-sms-verification.md:4`](../../../../../../../docs/runbook/phone-sms-verification.md) mode C exists; table L24 Telnyx POST webhook only; L140–141 Telnyx delivery note.
3. `rg SMSPM_REPORT_URL|SMSPM_WEBHOOK` in `.env.example` and runbook (SMSPM-03 t01): REPORT_URL not in runbook by design until this story.

### Gap / Проблема
Phase-2 env names and GET webhook path не задокументированы.

### AC/DoD
- [x] (P0) `.env.example` SMSPM block lists `SMSPM_WEBHOOK_SHARED_SECRET` and `SMSPM_REPORT_URL` (empty / comment; D-04-7).
- [x] (P0) Runbook: GET `/webhooks/smspm/delivery/{shared_secret}` row + env **names** (no values); Telnyx §B remains.
- [x] (P1) Do not create a second runbook file. Do not commit secrets.

### Где менять код
- `doge-identity-service/.env.example`
- `doge-identity-service/docs/runbook/phone-sms-verification.md`

### Out of scope
- Product `src/` in this task (t01–t03)
- Live smoke (SMSPM-03 t04)
- SMSPM-05 draft

### Проверка
```bash
rg -n 'SMSPM_WEBHOOK_SHARED_SECRET|SMSPM_REPORT_URL' doge-identity-service/.env.example
rg -n 'webhooks/smspm|SMSPM_WEBHOOK_SHARED_SECRET|SMSPM_REPORT_URL' doge-identity-service/docs/runbook/phone-sms-verification.md
```
