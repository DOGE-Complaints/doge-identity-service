## Task workspace — `task-ids-12-01-t06-offline-rate-limit-tests`

- Story: [`../STORY-IDS-SEC-01-rate-limiting.md`](../STORY-IDS-SEC-01-rate-limiting.md)
- Prerequisite: [`task-ids-12-01-t05-otp-cooldown-coexistence-policy`](../task-ids-12-01-t05-otp-cooldown-coexistence-policy/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000035`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md) Story AC #5  
---

## Task: implement — offline rate limit tests

### Цель
Покрыть offline-тестами 429+`retry_after` на N+1 запросе и callback per-ip — Story AC #5.

### Почему это важно
G-1 закрывается только с демонстрацией enforcement в тестах, не только в конфиге.

### Факты из кода
1. OAuth/eID test patterns: [`test_oauth_server_flow.py`](../../../../../../../tests/test_oauth_server_flow.py), eID tests in `tests/`.
2. No `test_rate_limiting.py` yet.
3. eid/start route: [`asgi_app.py:283`](../../../../../../../src/core/api/asgi_app.py).

### Gap / Проблема
Нет теста, доказывающего HTTP 429 + `retry_after` в envelope на превышении окна.

### AC/DoD
- [ ] (P0) Story AC #5: new `tests/test_rate_limiting.py`.
- [ ] (P0) eid/start: 6th request in 10min window → 429 + `retry_after` in envelope.
- [ ] (P0) callback per-ip: over-limit → 429.
- [ ] (P1) Regression: OTP cooldown still 400 (cross-ref t05).
- [ ] (P1) Reuse TestClient + JWT fixtures from existing tests.

### Где менять код
- `doge-identity-service/tests/test_rate_limiting.py` (new)

### Out of scope
- Live integration / Redis
- phone/request HTTP limit tests (follow-up)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_rate_limiting.py -m "not live_integration" -q
```
