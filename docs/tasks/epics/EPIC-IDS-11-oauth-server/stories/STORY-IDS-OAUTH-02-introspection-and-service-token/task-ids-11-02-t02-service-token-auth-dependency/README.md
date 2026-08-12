## Task workspace — `task-ids-11-02-t02-service-token-auth-dependency`

- Story: [`../STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../STORY-IDS-OAUTH-02-introspection-and-service-token.md)
- Prerequisite: t01 (SERVICE_API_TOKEN in config)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000030`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md) Scope §middleware/зависимость; Story AC #2  
---

## Task: implement — service token FastAPI dependency

### Цель
Реализовать проверку входящего сервисного токена (`Authorization: Bearer` или `X-Service-Token`) как FastAPI dependency, mirror gateway [`ServiceTokenAuth`](../../../../../../../../doge-complaints-gateway/src/core/api/security.py).

### Почему это важно
Без gate любой клиент сможет вызывать introspection; Story AC #2 требует 401/403 без валидного сервисного токена.

### Факты из кода
1. Gateway reference: [`security.py:16-62`](../../../../../../../../doge-complaints-gateway/src/core/api/security.py) — `extract_service_token`, `ServiceTokenAuth.require`.
2. [`security.py`](../../../../../../../src/core/api/security.py) — identity has `CompositeBearerTokenAuth` for user tokens only.
3. [`dependencies.py`](../../../../../../../src/core/api/dependencies.py) — API deps factory.

### Gap / Проблема
Нет `ServiceTokenAuth` / `require_service_token` dependency в identity.

### AC/DoD
- [x] (P0) `ServiceTokenAuth` (or equivalent) built from `AppConfig.service_api_token`; disabled when empty.
- [x] (P0) FastAPI `Depends` rejects missing/invalid service token with 401/403.
- [x] (P0) Accept `Authorization: Bearer <token>` and `X-Service-Token` (gateway parity).
- [x] (P1) Unit tests: valid/missing/invalid service token.
- [x] (P1) Traceability: Story AC #2.

### Где менять код
- `doge-identity-service/src/core/api/security.py`
- `doge-identity-service/src/core/api/dependencies.py`
- `doge-identity-service/src/core/infrastructure/providers.py`
- `doge-identity-service/tests/` (service auth tests)

### Out of scope
- Introspection handler logic (t03)
- `/oauth/introspect` route (t04)
- User Bearer on same request (user token in body — t03/t04)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q -k "service"
```
