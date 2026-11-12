## Task workspace — `task-ids-14-01-t04-env-example-smspm-block`

- Story: [`../STORY-IDS-SMSPM-01-provider-config-registry.md`](../STORY-IDS-SMSPM-01-provider-config-registry.md)
- Prerequisite: none (docs-only; может идти после t01 naming)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000046`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-01-provider-config-registry.md) (T04, AC #4, D-01-1, D-01-2)  
---

## Task: add — SMSPM block in `.env.example`

### Цель
Комментарий `mock | file | telnyx | smspm`; блок `SMSPM_*` (пустые значения, без секретов).

### Почему это важно
Story AC #4; оператор должен видеть имя провайдера и обязательные ключи без копирования секретов в git.

### Факты из кода
1. [`.env.example:60`](../../../../../../../.env.example) — `SMS_PROVIDER=mock  # активный провайдер: mock | file | telnyx` (нет `smspm`).
2. [`.env.example:71-79`](../../../../../../../.env.example) — блок Telnyx; строка 79 placeholder «другой SMS-провайдер позже».

### Gap / Проблема
Нет блока `SMSPM_*` и комментарий провайдеров не включает `smspm`.

### AC/DoD
- [x] (P0) Комментарий у `SMS_PROVIDER` содержит `mock | file | telnyx | smspm`.
- [x] (P0) Блок `SMSPM_HASH`, `SMSPM_TOKEN`, `SMSPM_FROM` пустые; `SMSPM_API_BASE_URL` default `https://api.smspm.com` (без секретов).
- [x] (P1) Не править runbook `phone-sms-verification.md` (SMSPM-03).

### Где менять код
- `doge-identity-service/.env.example` only

### Out of scope
- Runbook / live smoke (SMSPM-03)
- Product Python besides comments in env example

### Проверка
```bash
rg -n 'smspm|SMSPM_' doge-identity-service/.env.example
```
