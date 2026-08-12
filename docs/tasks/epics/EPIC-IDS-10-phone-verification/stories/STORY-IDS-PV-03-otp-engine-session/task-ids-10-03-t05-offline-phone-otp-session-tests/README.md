## Task workspace — `task-ids-10-03-t05-offline-phone-otp-session-tests`

- Story: [`../STORY-IDS-PV-03-otp-engine-session.md`](../STORY-IDS-PV-03-otp-engine-session.md)
- Prerequisite: t01–t04 implemented

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000024`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md) AC #1–#6  
---

## Task: test — offline phone OTP engine and session store coverage

### Цель
Покрыть тестами session store, OTP generate/verify, invalidation, error paths — Story AC #1–#6.

### Почему это важно
OTP security-critical; story AC #6 требует сценарии: успех, несовпадение, просрочка, лимит, повтор-инвалидация.

### Факты из кода
1. eID session store tests pattern: [`test_inmemory_repositories.py`](../../../../../../../tests/test_inmemory_repositories.py).
2. Phone config tests: [`test_phone_config_schema.py`](../../../../../../../tests/test_phone_config_schema.py).
3. Baseline: 268 pytest offline (post PV-02).

### Gap / Проблема
No `test_phone_otp_engine.py` / `test_phone_verification_session_store.py`.

### AC/DoD
- [ ] (P0) Store: create, get_by_id, get_active_by_user, mark_consumed/failed, expire_pending (Story AC #1).
- [ ] (P0) OTP: crypto random length; only hash stored; caplog — plaintext code not logged (Story AC #2).
- [ ] (P0) Verify success path → `PhoneVerificationResult` with `subject_hash = hash_secret(e164)` (Story AC #3, #5).
- [ ] (P0) Verify: `CODE_MISMATCH` + attempts++; `TOO_MANY_ATTEMPTS`; `CODE_EXPIRED` (Story AC #3).
- [ ] (P0) Repeat create invalidates prior session code (Story AC #4).
- [ ] (P1) Full offline suite green (Story AC #6).

### Где менять код
- `doge-identity-service/tests/test_phone_verification_session_store.py` (new)
- `doge-identity-service/tests/test_phone_otp_engine.py` (new)

### Out of scope
- Story acceptance doc — t06
- HTTP/integration — PV-05

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_phone_verification_session_store.py tests/test_phone_otp_engine.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
