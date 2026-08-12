## Task workspace — `task-ids-12-02-t03-phone-request-route-wiring`

- Story: [`../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md)
- Prerequisite: [`task-ids-12-02-t02-phone-request-rate-limit-dependency`](../task-ids-12-02-t02-phone-request-rate-limit-dependency/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000036`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) Scope §1; Story AC #1  
---

## Task: implement — wire phone request route rate limit

### Цель
Подключить `Depends(require_phone_request_rate_limit)` на `POST /auth/phone/request` **до** `handle_phone_request`.

### Почему это важно
Story AC #1: роут wired на HTTP rate-limit; порядок Depends → handler → cooldown (analysis §4).

### Факты из кода
1. Current route: [`asgi_app.py:344-358`](../../../../../../../src/core/api/asgi_app.py) — only `get_current_user`.
2. eid/start wiring reference: [`asgi_app.py:301-304`](../../../../../../../src/core/api/asgi_app.py) `Depends(require_eid_start_rate_limit)`.
3. Import block: [`rate_limit_dependency.py`](../../../../../../../src/core/api/rate_limit_dependency.py) exports.

### Gap / Проблема
`POST /auth/phone/request` не в rate-limit enforcement chain.

### AC/DoD
- [ ] (P0) `Depends(require_phone_request_rate_limit)` on `auth_phone_request`.
- [ ] (P0) Import `require_phone_request_rate_limit` in `asgi_app.py`.
- [ ] (P1) Order: rate limit → JWT auth → handler (cooldown inside handler unchanged).

### Где менять код
- `doge-identity-service/src/core/api/asgi_app.py`

### Out of scope
- Config (t01), dependency impl (t02), docs (t04), tests (t05)

### Проверка
```bash
grep -n "phone/request\|require_phone_request" doge-identity-service/src/core/api/asgi_app.py
```
