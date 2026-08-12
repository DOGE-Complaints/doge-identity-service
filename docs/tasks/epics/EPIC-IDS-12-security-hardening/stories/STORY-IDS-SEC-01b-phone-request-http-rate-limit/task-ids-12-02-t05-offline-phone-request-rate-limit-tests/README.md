## Task workspace — `task-ids-12-02-t05-offline-phone-request-rate-limit-tests`

- Story: [`../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md)
- Prerequisite: [`task-ids-12-02-t03-phone-request-route-wiring`](../task-ids-12-02-t03-phone-request-route-wiring/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000036`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) Scope §offline-тест; Story AC #4  
---

## Task: implement — offline phone request rate limit tests

### Цель
Offline-тесты: N+1 phone/request → 429 + `retry_after`; regression cooldown → 400 без `retry_after` — Story AC #4.

### Почему это важно
Scope §offline-тест; доказывает оба сценария сосуществования политик.

### Факты из кода
1. Existing cooldown test: `test_phone_otp_cooldown_still_domain_400_not_http_429` — [`test_rate_limiting.py`](../../../../../../../tests/test_rate_limiting.py).
2. Phone flow helpers: [`test_phone_verification_flow.py`](../../../../../../../tests/test_phone_verification_flow.py) `_request_phone`, `_EE_PHONE`.
3. eid 429 test pattern: `test_eid_start_rate_limit_returns_429_with_retry_after` — [`test_rate_limiting.py`](../../../../../../../tests/test_rate_limiting.py).

### Gap / Проблема
Нет теста HTTP window limit на `POST /auth/phone/request`.

### AC/DoD
- [ ] (P0) Test: N+1 `POST /auth/phone/request` in window → 429, `error.code=rate_limit_exceeded`, `retry_after` present.
- [ ] (P0) Regression: cooldown path still 400 `RATE_LIMITED`, no `retry_after` in envelope.
- [ ] (P1) Env fixture sets low `RATE_LIMIT_PHONE_REQUEST_*` for deterministic N+1.
- [ ] (P1) Full offline suite green.

### Где менять код
- `doge-identity-service/tests/test_rate_limiting.py`

### Out of scope
- Live integration tests
- Changing cooldown semantics

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_rate_limiting.py -m "not live_integration" -q
```
