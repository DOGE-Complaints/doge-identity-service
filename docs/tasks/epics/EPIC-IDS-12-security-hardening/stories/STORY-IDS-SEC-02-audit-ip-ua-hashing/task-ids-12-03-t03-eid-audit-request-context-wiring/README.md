## Task workspace — `task-ids-12-03-t03-eid-audit-request-context-wiring`

- Story: [`../STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../STORY-IDS-SEC-02-audit-ip-ua-hashing.md)
- Prerequisite: [`task-ids-12-03-t02-audit-ip-ua-hmac-hashing-helper`](../task-ids-12-03-t02-audit-ip-ua-hmac-hashing-helper/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000037`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md) Scope §проброс (eID); Story AC #1, #2  
---

## Task: implement — eID audit request context wiring

### Цель
Пробросить IP/UA из HTTP request в `_log_eid_audit` и заполнить `EIDAuditEvent.ip_hash` / `user_agent_hash` — Story Scope §проброс, AC #1 (eID), #2.

### Почему это важно
eID-аудит сейчас всегда пишет `None` — [`handlers.py:162-163`](../../../../../../../src/core/api/handlers.py).

### Факты из кода
1. `_log_eid_audit` без request — [`handlers.py:138-166`](../../../../../../../src/core/api/handlers.py).
2. Call sites: `handle_auth_eid_start`, `handle_auth_eid_callback` — [`handlers.py`](../../../../../../../src/core/api/handlers.py).
3. Routes have `Request` but don't pass to handlers — [`asgi_app.py:301-342`](../../../../../../../src/core/api/asgi_app.py).
4. Supabase repo already maps hash cols — [`db_supabase.py:202-203`](../../../../../../../src/core/infrastructure/db_supabase.py).

### Gap / Проблема
Request-контекст не доходит до eID audit layer.

### AC/DoD
- [ ] (P0) `_log_eid_audit` принимает hashed `ip_hash` / `user_agent_hash` (or audit context from t02).
- [ ] (P0) `asgi_app.py` передаёт request (or precomputed hashes) в `handle_auth_eid_start` / `handle_auth_eid_callback`.
- [ ] (P0) Все `_log_eid_audit` call sites в eID handlers получают non-None hashes when request has IP/UA.
- [ ] (P1) Story AC #1 eID half; AC #2 hash-only storage.

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`
- `doge-identity-service/src/core/api/asgi_app.py`

### Out of scope
- Phone audit (t04)
- Offline integration tests (t05)
- PhoneAuditEvent model (t01)

### Проверка
```bash
cd doge-identity-service
grep -n "ip_hash=None" src/core/api/handlers.py  # should be gone from _log_eid_audit path
.venv/bin/python -m pytest -m "not live_integration" -q --tb=no -x
```
