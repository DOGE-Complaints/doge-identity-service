## Task workspace — `task-ids-12-02-t02-phone-request-rate-limit-dependency`

- Story: [`../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md)
- Prerequisite: [`task-ids-12-02-t01-phone-request-rate-limit-config-schema`](../task-ids-12-02-t01-phone-request-rate-limit-config-schema/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000036`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) Scope §1; Story AC #1  
---

## Task: implement — phone request rate limit dependency

### Цель
Добавить `require_phone_request_rate_limit` — per-user ключ `user:{sub}` через существующий `_enforce_rate_limit`.

### Почему это важно
Scope §1: сквозной слой dependency до handler, тот же паттерн SEC-01.

### Факты из кода
1. eid/start pattern: [`require_eid_start_rate_limit`](../../../../../../../src/core/api/rate_limit_dependency.py) — `user:{supabase_user_id}`.
2. `_enforce_rate_limit` + `RateLimitExceeded` — [`rate_limit_dependency.py`](../../../../../../../src/core/api/rate_limit_dependency.py).
3. Route без Depends: [`asgi_app.py:344-358`](../../../../../../../src/core/api/asgi_app.py).

### Gap / Проблема
Нет dependency для phone/request route key из t01.

### AC/DoD
- [ ] (P0) `async def require_phone_request_rate_limit` с `get_current_user` + `_enforce_rate_limit`.
- [ ] (P0) Route key = `ROUTE_AUTH_PHONE_REQUEST` from t01.
- [ ] (P1) Reuse existing 429 path (`RateLimitExceeded` handler in `asgi_app.py`).

### Где менять код
- `doge-identity-service/src/core/api/rate_limit_dependency.py`

### Out of scope
- `asgi_app.py` wiring (t03)
- Cooldown handler changes

### Проверка
```bash
grep -n "require_phone_request_rate_limit" doge-identity-service/src/core/api/rate_limit_dependency.py
```
