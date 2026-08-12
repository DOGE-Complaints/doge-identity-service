## Task workspace — `task-ids-11-01-t01-authorization-request-store-and-contracts`

- Story: [`../STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../STORY-IDS-OAUTH-01-oauth-server-endpoints.md)
- Prerequisite: STORY-IDS-AUTHCORE-01 Done

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000029`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) Scope bullet `authorization_request`-store + `oauth_request_id`-handshake; Story AC #6  
---

## Task: implement — authorization request store + contracts

### Цель
Добавить доменную модель и store для pending OAuth authorization request (`oauth_request_id` handshake между `/oauth/authorize` и `/oauth/authorize/complete`).

### Почему это важно
Движок `InMemoryOAuthTokenService` умеет code/token/PKCE, но **не хранит** промежуточный authorize-запрос — без store невозможен spa-login redirect flow (req-14).

### Факты из кода
1. `authorization_request` — **0 matches** в `src/` (gap).
2. [`repositories.py:430-506`](../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryOAuthTokenService` (code/token/PKCE S256).
3. [`contracts.py:122-151`](../../../../../../../src/core/domain/contracts.py) — `OAuthClientStore`, token service ports.
4. [`dependencies.py:53-54,107-108`](../../../../../../../src/core/api/dependencies.py) — `oauth_client_store`, `oauth_token_service` wired.
5. [`providers.py:88`](../../../../../../../src/core/infrastructure/providers.py) — DI providers for OAuth.

### Gap / Проблема
Нет `AuthorizationRequest` entity, port и in-memory implementation; нет `oauth_request_id` генерации/TTL.

### AC/DoD
- [x] (P0) `AuthorizationRequest` model: `oauth_request_id`, `client_id`, `redirect_uri`, `scope`, `state`, PKCE fields, `created_at`, TTL.
- [x] (P0) `AuthorizationRequestStore` port: `save`, `get`, `consume` (one-time).
- [x] (P0) `InMemoryAuthorizationRequestStore` in `repositories.py` (MVP; OAUTH-03 durable later).
- [x] (P0) Wire store in `dependencies.py` / `providers.py`.
- [x] (P1) Unit tests: save/get/consume/TTL expiry.

### Где менять код
- `doge-identity-service/src/core/domain/models.py`
- `doge-identity-service/src/core/domain/contracts.py`
- `doge-identity-service/src/core/infrastructure/repositories.py`
- `doge-identity-service/src/core/api/dependencies.py`
- `doge-identity-service/src/core/infrastructure/providers.py`

### Out of scope
- HTTP handlers / routes (t03–t04)
- Supabase durable store (OAUTH-03)
- Introspection (OAUTH-02)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```
