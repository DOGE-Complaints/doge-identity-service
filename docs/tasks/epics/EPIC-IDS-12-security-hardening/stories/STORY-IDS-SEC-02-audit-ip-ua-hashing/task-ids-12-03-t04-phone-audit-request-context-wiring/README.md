## Task workspace — `task-ids-12-03-t04-phone-audit-request-context-wiring`

- Story: [`../STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../STORY-IDS-SEC-02-audit-ip-ua-hashing.md)
- Prerequisite: [`task-ids-12-03-t01-phone-audit-event-ip-ua-model-fields`](../task-ids-12-03-t01-phone-audit-event-ip-ua-model-fields/README.md), [`task-ids-12-03-t02-audit-ip-ua-hmac-hashing-helper`](../task-ids-12-03-t02-audit-ip-ua-hmac-hashing-helper/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000037`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md) Scope §проброс + §оба режима; Story AC #1, #3  
---

## Task: implement — phone audit request context wiring

### Цель
Пробросить IP/UA в `_log_phone_audit` и заполнить `PhoneAuditEvent.ip_hash` / `user_agent_hash` — Story Scope §проброс (phone), AC #1 (phone), #3.

### Почему это важно
Phone audit paths (`handle_phone_request`, `handle_phone_confirm`) вызывают `_log_phone_audit` без request-контекста — [`handlers.py:111-135`](../../../../../../../src/core/api/handlers.py).

### Факты из кода
1. `_log_phone_audit` builds event without hash fields — [`handlers.py:124-134`](../../../../../../../src/core/api/handlers.py).
2. Multiple call sites in phone handlers — [`handlers.py:464+`](../../../../../../../src/core/api/handlers.py).
3. Routes: `auth_phone_request`, `auth_phone_confirm` — [`asgi_app.py:345-375`](../../../../../../../src/core/api/asgi_app.py).

### Gap / Проблема
Request-контекст не доходит до phone audit layer.

### AC/DoD
- [ ] (P0) `_log_phone_audit` принимает и записывает `ip_hash` / `user_agent_hash` on `PhoneAuditEvent`.
- [ ] (P0) `asgi_app.py` передаёт request context into `handle_phone_request` / `handle_phone_confirm`.
- [ ] (P0) All `_log_phone_audit` call sites supply hashes from t02 helper.
- [ ] (P1) Story AC #1 phone half; AC #3 model fields populated.

### Где менять код
- `doge-identity-service/src/core/api/handlers.py`
- `doge-identity-service/src/core/api/asgi_app.py`

### Out of scope
- eID wiring (t03)
- Durable Supabase phone audit (PV-09)
- Full story gate (t06)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_phone_verification_flow.py -m "not live_integration" -q --tb=no -x
```
