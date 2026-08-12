## Task workspace — `task-ids-11-01-t06-offline-oauth-server-tests`

- Story: [`../STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../STORY-IDS-OAUTH-01-oauth-server-endpoints.md)
- Prerequisite: t01–t05 (implementation)

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** done  
**Wave:** `pkg-000029`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) Story AC #1–#7 (offline coverage)  
---

## Task: implement — offline OAuth server flow tests

### Цель
Покрыть offline-тестами полный authorize → complete → token flow и негативные сценарии (PKCE, invalid_grant, client_secret, RFC errors, authorize validations).

### Почему это важно
Story AC #8: «Покрыто тестами (offline)» — gate для OAUTH-01.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../STORY-IDS-OAUTH-01-oauth-server-endpoints.md) (8 checkboxes).
2. AC traceability: authorize validations t03; token/complete t04; errors/secret t02; store t01.
3. Existing transport patterns in `tests/` (httpx ASGI client).

### Gap / Проблема
Нет `tests/test_oauth_server_flow.py`; oauth routes untested end-to-end offline.

### AC/DoD
- [x] (P0) Happy path: authorize → complete (mock JWT) → token → access token issued.
- [x] (P0) `invalid_client`, `invalid_redirect_uri`, `invalid_scope` on authorize.
- [x] (P0) `state` preserved through redirect chain.
- [x] (P0) PKCE: wrong `code_verifier` → `invalid_grant`.
- [x] (P0) Wrong `client_secret` → rejection.
- [x] (P0) Reused/expired code → `invalid_grant`.
- [x] (P0) RFC 6749 error body shape assertions.
- [x] (P1) Extend transport smoke if oauth routes listed there.

### Где менять код
- `doge-identity-service/tests/test_oauth_server_flow.py` (new)
- `doge-identity-service/tests/` (smoke/transport if applicable)

### Out of scope
- Live ChatGPT / Supabase integration
- Introspection tests (OAUTH-02)
- Story gate doc (t07)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_oauth_server_flow.py -q
.venv/bin/python -m pytest -m "not live_integration" -q
```
