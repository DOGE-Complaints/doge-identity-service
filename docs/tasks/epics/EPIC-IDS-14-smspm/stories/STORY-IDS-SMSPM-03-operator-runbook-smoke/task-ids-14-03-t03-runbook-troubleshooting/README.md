## Task workspace — `task-ids-14-03-t03-runbook-troubleshooting`

- Story: [`../STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../STORY-IDS-SMSPM-03-operator-runbook-smoke.md)
- Prerequisite: [`t01`](../task-ids-14-03-t01-runbook-mode-c-env-table/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000048`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md) (T03, AC #3)  
---

## Task: add — runbook troubleshooting rows for SMSPM

### Цель
В §7 runbook — короткие строки: missing creds, country/prefix, rate limit / SEND_FAILED. Без копирования inbound SMSPM guide целиком.

### Почему это важно
Story AC #3: оператор должен отличить config-промах от country/rate-limit и от provider SEND_FAILED.

### Факты из кода
1. §7 сейчас [`phone-sms-verification.md:135-144`](../../../../../../runbook/phone-sms-verification.md) — есть `COUNTRY_NOT_ALLOWED`, `RATE_LIMITED`; `CONFIG_ERROR` только для `TELNYX_*`; live SMS-не-приходит только Telnyx/SPIKE-08.
2. Missing SMSPM creds → `ConfigError` [`config.py:15-18`](../../../../../../../src/core/phone/smspm/config.py) (`SMSPM_HASH`/`TOKEN`/`FROM`).
3. 401 / 4xx → `SEND_FAILED` [`errors.py:30-32,36-38`](../../../../../../../src/core/phone/smspm/errors.py); HTTP клиенту [`handlers.py:97-99`](../../../../../../../src/core/api/handlers.py) `SEND_FAILED`/`PROVIDER_UNAVAILABLE` → 503.

### Gap / Проблема
Таблица §7 не покрывает `SMS_PROVIDER=smspm` missing creds и SEND_FAILED.

### AC/DoD
- [x] (P0) Строка missing creds: при `SMS_PROVIDER=smspm` пустые `SMSPM_HASH`/`TOKEN`/`FROM` → `CONFIG_ERROR` (зеркало Telnyx-строки).
- [x] (P0) Country/prefix и rate limit остаются в таблице (можно ссылкой на существующие строки, без дубля гида).
- [x] (P0) Строка SEND_FAILED / 503 для live SMSPM (невалидные creds/4xx) — кратко.
- [x] (P1) Не копировать inbound `SMSPM_SMS_Delivery_Integration_Guide.md`. Не править `src/`.

### Где менять код
- `doge-identity-service/docs/runbook/phone-sms-verification.md` only (§7)

### Out of scope
- Env / curl секции (t01–t02)
- Live execute (t04)
- Product `src/`
- SMSPM-04 webhook

### Проверка
```bash
rg -n 'SMSPM_|SEND_FAILED|CONFIG_ERROR|COUNTRY_NOT_ALLOWED|RATE_LIMITED' doge-identity-service/docs/runbook/phone-sms-verification.md
```
