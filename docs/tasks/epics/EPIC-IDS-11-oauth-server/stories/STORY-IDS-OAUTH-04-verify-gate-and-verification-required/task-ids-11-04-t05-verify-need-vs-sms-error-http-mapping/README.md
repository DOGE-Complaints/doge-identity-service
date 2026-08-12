## Task workspace — `task-ids-11-04-t05-verify-need-vs-sms-error-http-mapping`

- Story: [`../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)
- Prerequisite: [`task-ids-11-04-t04-verification-required-contract`](../task-ids-11-04-t04-verification-required-contract/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000034`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) Scope §SmsErrorCode/HTTP; Story AC #4  
---

## Task: implement — verify-need vs SMS error HTTP mapping

### Цель
Явно развести verify-need (403 + `verification_required`) от OTP-ошибок (`SmsErrorCode` → 400) (Story AC #4).

### Почему это важно
Клиенты не должны путать «нужна верификация телефона» с «неверный OTP»; разные HTTP semantics.

### Факты из кода
1. OTP → 400: [`handlers.py:96-99`](../../../../../../../src/core/api/handlers.py) — `_sms_error_http_status`.
2. `SmsErrorCode` enum в phone verification paths.
3. Verify-need contract (t04) — должен отдавать **403**.

### Gap / Проблема
Нет явного разделения: verify-need может быть смешан с SMS error paths или неверным status code.

### AC/DoD
- [ ] (P0) Story AC #4: verify-need → **403** + `verification_required` body (not `SmsErrorCode`/400).
- [ ] (P0) Документировать separation от `_sms_error_http_status` (comment or module boundary).
- [ ] (P1) Regression assertion: phone OTP paths остаются 400 (не регрессия t06).

### Где менять код
- `doge-identity-service/src/core/oauth/handlers.py`
- `doge-identity-service/src/core/oauth/verification_required.py`

### Out of scope
- Изменение OTP handler semantics
- Offline test file (t06)
- Gateway enforcement

### Проверка
```bash
cd doge-identity-service
grep -n '_sms_error_http_status\|403' src/core/oauth/handlers.py src/core/api/handlers.py
```
