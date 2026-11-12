## Task workspace — `task-ids-14-03-t02-runbook-curl-smoke`

- Story: [`../STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../STORY-IDS-SMSPM-03-operator-runbook-smoke.md)
- Prerequisite: [`t01`](../task-ids-14-03-t01-runbook-mode-c-env-table/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000048`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md`](../../../../../../backlog-stories/smspm/STORY-IDS-SMSPM-03-operator-runbook-smoke.md) (T02, AC #2, D-03-2, D-03-4)  
---

## Task: add — runbook live-smoke curl path for mode C

### Цель
Описать curl-путь request → confirm → `/me` для `SMS_PROVIDER=smspm` зеркалом Telnyx §6. Mock (§5) и Telnyx (§6 B) остаются (D-03-2). Ожидание `/me`: `phone_verified` + `phone_provider` отражает `smspm` (D-03-4).

### Почему это важно
Story AC #2: оператор должен повторить тот же продуктовый smoke, что для Telnyx, без второго документа.

### Факты из кода
1. Telnyx live curl [`phone-sms-verification.md:107-126`](../../../../../../runbook/phone-sms-verification.md) — POST `/auth/phone/request`, `/confirm`, GET `/me` с `"phone_provider": "telnyx"`.
2. Режим A mock [`phone-sms-verification.md:75-103`](../../../../../../runbook/phone-sms-verification.md) — pytest + curl request (confirm в mock недоступен через curl).
3. `/me` отдаёт `phone_provider` [`me_response.py:32,47`](../../../../../../../src/core/api/me_response.py).
4. Sender уже Done — [`descriptor.py:10-16`](../../../../../../../src/core/phone/smspm/descriptor.py) `SmspmSmsSender` (не менять в этой story).

### Gap / Проблема
Нет curl-секции режима C; оператор не видит шаги smspm live-smoke рядом с Telnyx.

### AC/DoD
- [x] (P0) В runbook есть live-smoke curl-путь режима C: `/auth/phone/request` → SMS на EE → `/auth/phone/confirm` → GET `/me`.
- [x] (P0) Ожидание `/me`: `phone_verified` true и `"phone_provider": "smspm"` (D-03-4).
- [x] (P0) Секции mock (A) и Telnyx (B) по-прежнему описаны (D-03-2).
- [x] (P1) Не править `src/`. Не новый runbook-файл.

### Где менять код
- `doge-identity-service/docs/runbook/phone-sms-verification.md` only (новый § после B / §6C)

### Out of scope
- Env table (t01)
- Troubleshooting (t03)
- Фактический live прогон (t04)
- Product `src/`

### Проверка
```bash
rg -n 'phone_provider.: .smspm|/auth/phone/request|/auth/phone/confirm' doge-identity-service/docs/runbook/phone-sms-verification.md
rg -n 'Режим A|mock|Режим B|telnyx|Telnyx' doge-identity-service/docs/runbook/phone-sms-verification.md
```
