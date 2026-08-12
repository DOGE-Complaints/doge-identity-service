## Task workspace — `task-ids-10-03-t04-otp-verify-attempts-expiry-result`

- Story: [`../STORY-IDS-PV-03-otp-engine-session.md`](../STORY-IDS-PV-03-otp-engine-session.md)
- Prerequisite: t03 (`create_phone_verification_session`)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000024`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md) Scope bullets 3, 5; AC #3, #5  
---

## Task: implement — OTP verify, attempts, expiry, `PhoneVerificationResult`

### Цель
Реализовать `verify_phone_code` с error mapping и успешный `PhoneVerificationResult` — Story Scope сверка + result; AC #3, #5.

### Почему это важно
Закрывает confirm-половину флоу до HTTP (PV-05); `subject_hash` без provider prefix — анти-Sybil по E.164.

### Факты из кода
1. `SmsErrorCode`: `CODE_MISMATCH`, `CODE_EXPIRED`, `TOO_MANY_ATTEMPTS` ([`base.py:14-16`](../../../../../../../src/core/phone/base.py)).
2. `SmsSenderError` with code ([`base.py:26-34`](../../../../../../../src/core/phone/base.py)).
3. `hash_secret` for code compare and `subject_hash` ([`hashing.py:9-11`](../../../../../../../src/core/security/hashing.py)).
4. `AppConfig.phone_max_attempts` ([`schema.py:67`](../../../../../../../src/core/config/schema.py)).
5. eID handler prefixes subject for profile ([`handlers.py:325-327`](../../../../../../../src/core/api/handlers.py)) — phone story: **no** provider prefix on `subject_hash`.

### Gap / Проблема
No verify function; no attempts increment; no result builder.

### AC/DoD
- [ ] (P0) Expired session (`expires_at < now` or `status=expired`) → `SmsSenderError(CODE_EXPIRED)` (Story AC #3).
- [ ] (P0) Wrong code → `CODE_MISMATCH`, increment `attempts` on session (Story AC #3).
- [ ] (P0) `attempts >= phone_max_attempts` → `TOO_MANY_ATTEMPTS` (Story AC #3).
- [ ] (P0) Correct code → `mark_consumed`, return `PhoneVerificationResult` with `subject_hash = hash_secret(e164, key=eid_secret)` **without** provider prefix (Story AC #5).
- [ ] (P1) Constant-time compare for code hash (`hmac.compare_digest` pattern).

### Где менять код
- `doge-identity-service/src/core/phone/otp_engine.py`
- `doge-identity-service/src/core/phone/__init__.py`

### Out of scope
- HTTP confirm handler — PV-05
- Profile attach — PV-04
- Tests — t05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.phone.otp_engine import verify_phone_code; print(verify_phone_code)"
```
