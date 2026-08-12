## Task workspace — `task-ids-11-04-t06-offline-oauth-verify-gate-tests`

- Story: [`../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)
- Prerequisite: [`task-ids-11-04-t05-verify-need-vs-sms-error-http-mapping`](../task-ids-11-04-t05-verify-need-vs-sms-error-http-mapping/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000034`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) Story AC #5 (tests)  
---

## Task: implement — offline OAuth verify-gate tests

### Цель
Покрыть offline-тестами relay authorize→complete, unverified branch, contract payload, 403 vs 400 separation (Story AC #5).

### Почему это важно
Verify-gate — критический security/UX path; без тестов регрессии неизбежны.

### Факты из кода
1. OAuth test patterns: [`tests/test_oauth_server.py`](../../../../../../../tests/test_oauth_server.py).
2. OAUTH-03 store mocks: [`tests/test_oauth_supabase_stores.py`](../../../../../../../tests/test_oauth_supabase_stores.py).
3. Implementation targets t01–t05.

### Gap / Проблема
Нет `test_oauth_verify_gate.py` для relay + verify-gate + contract + HTTP mapping.

### AC/DoD
- [ ] (P0) Story AC #5: новый `tests/test_oauth_verify_gate.py`.
- [ ] (P0) Relay: authorize с `requested_action`/`return_context` → complete видит persisted values.
- [ ] (P0) Unverified branch: `phone_verified=false` + verify-requiring action → no code, verify signal.
- [ ] (P0) Contract payload `{error, reason, verify_url}` shape asserted.
- [ ] (P0) 403 verify-need vs 400 OTP separation (mock/regression).
- [ ] (P1) Reuse OAUTH-03 in-memory store patterns.

### Где менять код
- `doge-identity-service/tests/test_oauth_verify_gate.py` (new)

### Out of scope
- Live integration tests
- Story gate doc (t07)
- Gateway tests

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_oauth_verify_gate.py -m "not live_integration" -q
```
