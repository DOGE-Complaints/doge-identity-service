## Task workspace — `task-ids-12-01-t05-otp-cooldown-coexistence-policy`

- Story: [`../STORY-IDS-SEC-01-rate-limiting.md`](../STORY-IDS-SEC-01-rate-limiting.md)
- Prerequisite: [`task-ids-12-01-t04-sensitive-routes-wiring`](../task-ids-12-01-t04-sensitive-routes-wiring/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000035`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md) Scope §OTP-cooldown; Story AC #4  
---

## Task: implement — OTP cooldown coexistence policy

### Цель
Зафиксировать и протестировать сосуществование HTTP 429 (t03) и доменного OTP cooldown — Story AC #4.

### Почему это важно
Cooldown возвращает 400 `RATE_LIMITED`, не 429; оператор: HTTP limit не дублирует cooldown на phone/request.

### Факты из кода
1. OTP cooldown: [`handlers.py:456-473`](../../../../../../../src/core/api/handlers.py) → `SmsErrorCode.RATE_LIMITED`.
2. HTTP mapping: [`_sms_error_http_status`](../../../../../../../src/core/api/handlers.py) → 400 (not 503).
3. Default cooldown: `phone_resend_cooldown_s=60` — [`schema.py:237`](../../../../../../../src/core/config/schema.py).
4. Test exists: `test_phone_request_rate_limited_before_cooldown` in [`test_phone_verification_flow.py`](../../../../../../../tests/test_phone_verification_flow.py).

### Gap / Проблема
Нет документированной политики: что остаётся domain 400 vs HTTP 429 window limit.

### AC/DoD
- [ ] (P0) Story AC #4: policy documented — cooldown stays domain 400; HTTP 429 only from t03 layer on wired routes.
- [ ] (P0) phone/request: no HTTP rate-limit in pkg-000035; cooldown unchanged.
- [ ] (P1) Regression test: OTP cooldown still 400 after t03 lands.
- [ ] (P1) Comment in handlers or rate_limit module referencing separation from `_sms_error_http_status`.

### Где менять код
- `doge-identity-service/src/core/api/handlers.py` (comment only if needed)
- `doge-identity-service/docs/runtime-docs/04-security.md` (anti-abuse note, t07 may expand)

### Out of scope
- phone/request HTTP rate-limit implementation (follow-up story)
- Changing cooldown semantics

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_phone_verification_flow.py::test_phone_request_rate_limited_before_cooldown -q
```
