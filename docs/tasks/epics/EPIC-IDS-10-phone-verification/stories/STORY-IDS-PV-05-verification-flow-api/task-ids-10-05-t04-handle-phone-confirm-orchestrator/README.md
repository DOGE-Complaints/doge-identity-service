## Task workspace — `task-ids-10-05-t04-handle-phone-confirm-orchestrator`

- Story: [`../STORY-IDS-PV-05-verification-flow-api.md`](../STORY-IDS-PV-05-verification-flow-api.md)
- Prerequisite: t02 DI; t03 request (session exists); PV-04 attach

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** todo  
**Wave:** `pkg-000026`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md) Scope bullets 2, 3; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §5  
---

## Task: implement — `handle_phone_confirm` orchestrator

### Цель
Реализовать `POST /auth/phone/confirm` orchestration — Story Scope §confirm + session-binding.

### Почему это важно
Story AC #3: verify code, attach profile, dedup 409, canonical error codes.

### Факты из кода
1. Session by JWT user: `PhoneVerificationSessionStore.get_active_by_user` ([`contracts.py:77`](../../../../../../../src/core/domain/contracts.py)).
2. Verify: [`verify_phone_code`](../../../../../../../src/core/phone/otp_engine.py:67) — needs `session_id`, `submitted_code`, `e164` (for `subject_hash`); marks consumed on success.
3. Profile attach: [`attach_phone_verification`](../../../../../../../src/core/infrastructure/repositories.py) with `one_account_per_number=config.phone_one_account_per_number`.
4. `ProfileConflictError` → 409 образец: [`handlers.py:339`](../../../../../../../src/core/api/handlers.py) (eID callback).
5. `handle_phone_confirm` **отсутствует**.

### Gap / Проблема
No confirm orchestration linking OTP verify → profile flag.

### AC/DoD
- [ ] (P0) `handle_phone_confirm(deps, *, current_user, phone: str, code: str, trace_id)` — request body fields `phone` + `code` (architecture §5; needed for `verify_phone_code` e164 arg).
- [ ] (P0) Resolve active session for `current_user.supabase_user_id`; missing → appropriate `SmsErrorCode` error.
- [ ] (P0) `verify_phone_code` → on success `attach_phone_verification` with result fields (`provider`, `dial_prefix`, `verified_phone_hash=subject_hash`, `verified_at`).
- [ ] (P0) `ProfileConflictError` → 409 envelope (dedup AC#3).
- [ ] (P0) `SmsSenderError` from verify → error envelope with `SmsErrorCode` (`CODE_MISMATCH`, `CODE_EXPIRED`, `TOO_MANY_ATTEMPTS`).
- [ ] (P0) Success response `{ status: "verified" }`; audit without PII (AC#4).
- [ ] (P1) After success, profile `phone_verified=true` (via attach); `/me` reflects on next GET (PV-04).

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`

### Out of scope
- ASGI routes — t05
- Telnyx — PV-06

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_phone_verification_flow.py -q -k confirm 2>/dev/null || echo "t05 adds e2e tests"
```
