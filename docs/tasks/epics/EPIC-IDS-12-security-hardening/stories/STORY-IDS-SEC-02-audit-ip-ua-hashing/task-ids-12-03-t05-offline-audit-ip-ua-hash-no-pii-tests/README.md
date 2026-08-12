## Task workspace — `task-ids-12-03-t05-offline-audit-ip-ua-hash-no-pii-tests`

- Story: [`../STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../STORY-IDS-SEC-02-audit-ip-ua-hashing.md)
- Prerequisite: [`task-ids-12-03-t03-eid-audit-request-context-wiring`](../task-ids-12-03-t03-eid-audit-request-context-wiring/README.md), [`task-ids-12-03-t04-phone-audit-request-context-wiring`](../task-ids-12-03-t04-phone-audit-request-context-wiring/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000037`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md) Scope §без PII; Story AC #2, #4  
---

## Task: tests — offline audit IP/UA hash and no-PII coverage

### Цель
Offline-тесты: hash-поля заполнены, сырой IP/UA отсутствует, PII-инвариант сохранён — Story Scope §без PII, AC #2, #4.

### Почему это важно
Существующий `test_phone_audit_events_contain_no_pii` не проверяет hash-поля — [`test_phone_verification_flow.py:265-289`](../../../../../../../tests/test_phone_verification_flow.py).

### Факты из кода
1. Phone PII regression — [`test_phone_verification_flow.py:265`](../../../../../../../tests/test_phone_verification_flow.py).
2. eID audit in-memory repo — [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py).
3. Test client can set headers (`User-Agent`, `X-Forwarded-For` with trusted proxy env).

### Gap / Проблема
Нет тестов, доказывающих hashed IP/UA в обоих режимах и отсутствие raw values.

### AC/DoD
- [ ] (P0) Phone flow test: audit events have non-None `ip_hash`/`user_agent_hash` when request carries IP/UA; serialized audit contains neither raw IP nor raw UA string.
- [ ] (P0) eID flow test (start or callback path): `EIDAuditEvent` records populated hashes, not raw IP/UA.
- [ ] (P0) Story AC #4: extend/no regression on phone/code PII — phone number and OTP code still absent from audit serialization.
- [ ] (P1) Story AC #2: assert hash format (hex, length consistent with HMAC-SHA256).

### Где менять код
- `doge-identity-service/tests/test_phone_verification_flow.py`
- `doge-identity-service/tests/` (new or extended eID audit test module, e.g. `test_audit_ip_ua_hashing.py`)

### Out of scope
- Live Supabase integration tests
- PV-09 durable store tests

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_phone_verification_flow.py tests/test_audit_ip_ua_hashing.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
