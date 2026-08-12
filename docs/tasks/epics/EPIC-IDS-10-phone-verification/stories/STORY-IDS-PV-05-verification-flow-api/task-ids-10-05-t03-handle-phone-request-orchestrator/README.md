## Task workspace — `task-ids-10-05-t03-handle-phone-request-orchestrator`

- Story: [`../STORY-IDS-PV-05-verification-flow-api.md`](../STORY-IDS-PV-05-verification-flow-api.md)
- Prerequisite: t02 DI wiring; PV-02 e164; PV-03 otp_engine

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** todo  
**Wave:** `pkg-000026`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md) Scope bullets 1, 3; [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §5  
---

## Task: implement — `handle_phone_request` orchestrator

### Цель
Реализовать `POST /auth/phone/request` orchestration — Story Scope §request + §оркестратор-хендлеры.

### Почему это важно
Story AC #1, #2: session + SMS send + prefix/cooldown errors.

### Факты из кода
1. E.164 + prefix: [`e164.py`](../../../../../../../src/core/phone/e164.py) → `SmsSenderError` with `SmsErrorCode`.
2. OTP session create: [`create_phone_verification_session`](../../../../../../../src/core/phone/otp_engine.py:32) — invalidates prior session on success (PV-03).
3. SMS send: [`SmsSenderRegistry.get_active`](../../../../../../../src/core/phone/registry.py:24), [`MockSmsSender.send`](../../../../../../../src/core/phone/mock/mock_sender.py:22).
4. Rate-limit config: `config.phone_resend_cooldown_s` ([`schema.py`](../../../../../../../src/core/config/schema.py)).
5. eID error mapping образец: `EIDProviderError` → envelope in [`handlers.py`](../../../../../../../src/core/api/handlers.py).
6. `handle_phone_request` **отсутствует**.

### Gap / Проблема
No request orchestration; rate-limit (`PHONE_RESEND_COOLDOWN_S`) not enforced at API layer.

### AC/DoD
- [ ] (P0) `handle_phone_request(deps, *, current_user, phone: str, trace_id)` in `handlers.py`.
- [ ] (P0) Flow: normalize E.164 → `assert_allowed_dial_prefix` → **rate-limit** check (`get_active_by_user`; if `created_at + cooldown > now` → `SmsErrorCode.RATE_LIMITED`, no new session).
- [ ] (P0) On success path: `create_phone_verification_session` → build SMS text with OTP (core-owned, code not logged) → `registry.get_active(config).send` → audit success.
- [ ] (P0) Response `{ sent: true, expires_at }` (ISO UTC, mirror eID `_format_utc_iso`).
- [ ] (P0) `SmsSenderError` → `build_error_envelope(code=exc.code.value, ...)` with appropriate HTTP status (400 for client errors).
- [ ] (P1) Story AC #2: `COUNTRY_NOT_ALLOWED` on bad prefix; `RATE_LIMITED` on early resend; successful new request invalidates old code (PV-03).

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`
- Optional: `doge-identity-service/src/core/phone/sms_text.py` (minimal SMS template)

### Out of scope
- ASGI route registration — t05
- Confirm flow — t04
- Telnyx-specific send — PV-06

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_phone_verification_flow.py -q -k request 2>/dev/null || echo "t05 adds e2e tests"
```
