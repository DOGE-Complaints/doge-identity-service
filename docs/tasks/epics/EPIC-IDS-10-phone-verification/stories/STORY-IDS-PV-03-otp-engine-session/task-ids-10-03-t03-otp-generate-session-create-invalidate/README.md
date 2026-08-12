## Task workspace — `task-ids-10-03-t03-otp-generate-session-create-invalidate`

- Story: [`../STORY-IDS-PV-03-otp-engine-session.md`](../STORY-IDS-PV-03-otp-engine-session.md)
- Prerequisite: t01, t02 (models + store)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000024`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md) Scope bullets 2, 4; AC #2, #4  
---

## Task: implement — OTP generation, session create, repeat invalidation

### Цель
Реализовать OTP generate + `create_phone_verification_session` с инвалидацией прежней сессии пользователя — Story Scope OTP engine + repeat invalidation; AC #2, #4.

### Почему это важно
Ядро генерирует OTP (не SMS-провайдер); повторный request не должен оставлять два активных кода (architecture §10.1 P3).

### Факты из кода
1. HMAC: [`hash_secret`](../../../../../../../src/core/security/hashing.py:9-11).
2. `AppConfig`: `phone_code_length`, `phone_code_ttl_s`, `eid_secret` ([`schema.py:63-69`](../../../../../../../src/core/config/schema.py)).
3. `secrets` module — stdlib crypto RNG for OTP digits.
4. OTP module **отсутствует** under `src/core/phone/`.

### Gap / Проблема
No OTP generation; no session create with hash-only storage; no invalidation on repeat.

### AC/DoD
- [ ] (P0) Generate numeric OTP length `config.phone_code_length` via `secrets` (Story AC #2).
- [ ] (P0) `code_hash = hash_secret(code, key=config.eid_secret)`; session stores hash only, not plaintext.
- [ ] (P0) `expires_at = now + timedelta(seconds=config.phone_code_ttl_s)`.
- [ ] (P0) Plaintext OTP **not** logged (no `print`/`logger` of code).
- [ ] (P0) On new session for same `supabase_user_id`, invalidate prior `started` session (Story AC #4).
- [ ] (P1) Return tuple `(session, plaintext_code)` for caller (PV-05 sends SMS); code only in memory for send step.

### Где менять код
- `doge-identity-service/src/core/phone/otp_engine.py` (new)
- `doge-identity-service/src/core/phone/__init__.py` (exports)

### Out of scope
- Code verification — t04
- SMS send — PV-05/PV-06
- E.164 normalize — PV-02 (`e164.py`), used by PV-05 caller

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.phone.otp_engine import create_phone_verification_session; print(create_phone_verification_session)"
```
