## Task workspace — `task-ids-12-01-t03-rate-limit-dependency-429-envelope`

- Story: [`../STORY-IDS-SEC-01-rate-limiting.md`](../STORY-IDS-SEC-01-rate-limiting.md)
- Prerequisite: [`task-ids-12-01-t02-in-memory-rate-limiter-store`](../task-ids-12-01-t02-in-memory-rate-limiter-store/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000035`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md) Scope §сквозной слой + §429; Story AC #2, #3  
---

## Task: implement — rate limit dependency + 429 envelope

### Цель
Сквозной FastAPI dependency/middleware: enforce **до** handler; HTTP 429 + `retry_after` в envelope — Story AC #2, #3.

### Почему это важно
Без единого слоя лимиты дублируются в хендлерах; spec 16 требует 429 + retry_after.

### Факты из кода
1. Envelope today: `{"error":{"code","message","trace_id"}}` — [`envelope.py:10-20`](../../../../../../../src/core/api/envelope.py).
2. Spec 16 flat: `{"error":"rate_limit_exceeded","retry_after":N}` — AC требует **согласование** с nested envelope + code `rate_limit_exceeded`.
3. Routes registered in [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py).
4. User key from `UserClaims` via `get_current_user` dependency.

### Gap / Проблема
Нет `build_rate_limit_envelope` и dependency, вызываемого до `handle_auth_eid_start` и callback handlers.

### AC/DoD
- [ ] (P0) Story AC #2: HTTP 429 + `retry_after` (seconds) in error envelope.
- [ ] (P0) Story AC #3: enforcement in cross-cutting layer (Depends or route wrapper), not inside business handlers.
- [ ] (P0) Error code `rate_limit_exceeded` aligned with spec 11/16.
- [ ] (P1) Optional `Retry-After` response header.

### Где менять код
- `doge-identity-service/src/core/api/envelope.py`
- `doge-identity-service/src/core/security/rate_limit.py` (dependency helpers)
- `doge-identity-service/src/core/api/asgi_app.py` (wire Depends)

### Out of scope
- Per-route config defaults (t01)
- OTP cooldown policy (t05)
- phone/request wiring (follow-up)

### Проверка
```bash
cd doge-identity-service
grep -n 'rate_limit_exceeded\|retry_after' src/core/api/envelope.py src/core/security/*.py
```
