## Task workspace — `task-ids-11-02-t05-offline-introspection-tests`

- Story: [`../STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../STORY-IDS-OAUTH-02-introspection-and-service-token.md)
- Prerequisite: t01–t04

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000030`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md) Story AC #4  
---

## Task: test — offline introspection flow + gateway contract

### Цель
Offline pytest: valid token → active response; invalid/expired → `{active:false}`; missing service token → 401/403; `phone_verified` reflects profile not token. Зафиксировать контракт ответа для gateway в task evidence.

### Почему это важно
Story AC #4 требует тесты и контракт для gateway intake ([`09-gateway-expectations`](../../../../../../../runtime-docs/09-gateway-expectations.md)).

### Факты из кода
1. [`tests/test_oauth_server_flow.py`](../../../../../../../tests/test_oauth_server_flow.py) — OAUTH-01 flow test pattern.
2. Gateway expects `{active, sub, phone_verified}` per [`09-gateway-expectations.md:24`](../../../../../../../runtime-docs/09-gateway-expectations.md).

### Gap / Проблема
Нет `test_oauth_introspection*.py` coverage.

### AC/DoD
- [x] (P0) Test: valid OAuth token + valid service token → `{active:true, sub, phone_verified}`.
- [x] (P0) Test: expired/invalid user token → `{active:false}`.
- [x] (P0) Test: no/invalid service token → 401/403 even with valid user token.
- [x] (P0) Test: profile `phone_verified=true/false` drives response (not JWT claim).
- [x] (P1) Contract table in test module docstring or README evidence (fields + types).
- [x] (P1) Full offline suite green: `pytest -m "not live_integration"`.
- [x] (P1) Traceability: Story AC #1–#4.

### Где менять код
- `doge-identity-service/tests/test_oauth_introspection.py` (new)
- `doge-identity-service/tests/conftest.py` (fixtures if needed)

### Out of scope
- Gateway-side tests
- Live integration / E2E with real gateway
- Story gate doc (t06)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```
