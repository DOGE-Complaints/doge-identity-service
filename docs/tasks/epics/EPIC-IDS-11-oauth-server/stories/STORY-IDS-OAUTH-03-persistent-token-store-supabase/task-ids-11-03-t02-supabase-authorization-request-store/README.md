## Task workspace — `task-ids-11-03-t02-supabase-authorization-request-store`

- Story: [`../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md)
- Prerequisite: t01 migration SQL

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000033`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) Scope §request-state; Story AC #2 (request part)  
---

## Task: implement — SupabaseAuthorizationRequestStore

### Цель
Реализовать PostgREST-backed `AuthorizationRequestStore` для handshake (`oauth_request_id`) — часть durable OAuth state из Story Scope.

### Почему это важно
Handlers [`handlers.py:28-102`](../../../../../../../src/core/oauth/handlers.py) используют отдельный порт `oauth_authorization_request_store`; без Supabase-реализации handshake теряется при рестарте даже при `DB_BACKEND=supabase`.

### Факты из кода
1. Port: [`contracts.py:123-128`](../../../../../../../src/core/domain/contracts.py) — `AuthorizationRequestStore` (`save`, `get`, `consume`).
2. Domain model: [`models.py:138-147`](../../../../../../../src/core/domain/models.py) — `AuthorizationRequest`.
3. In-memory reference: [`repositories.py:431-449`](../../../../../../../src/core/infrastructure/repositories.py) — TTL + single-use on `consume`.
4. PostgREST pattern: [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) — `SupabaseVerificationSessionStore` / `SupabaseDatabase`.
5. **Архитектурная оговорка:** backlog Scope называет `SupabaseOAuthTokenService` «+ хранение authorization_request»; в коде два DI-слота (как OAUTH-01 t01) — request-store реализуется отдельным классом, AC #2 закрывается парой t02+t03.

### Gap / Проблема
Нет Supabase-реализации `AuthorizationRequestStore`; только `InMemoryAuthorizationRequestStore`.

### AC/DoD
- [x] (P0) `SupabaseAuthorizationRequestStore` in `db_supabase.py`: `save` / `get` / `consume` against `oauth_authorization_requests`.
- [x] (P0) `consume` enforces single-use + TTL (`expires_at`); expired → `None` (mirror in-memory).
- [x] (P0) Row ↔ `AuthorizationRequest` mapping (scopes as JSON/array per migration).
- [x] (P1) Export in `db_supabase.__all__` if project convention requires.
- [x] (P1) Traceability: Story AC #2 (request-state persistence).

### Где менять код
- `doge-identity-service/src/core/infrastructure/db_supabase.py`

### Out of scope
- Authorization codes / `OAuthTokenService` (t03)
- DI selection (t04)
- Migration SQL (t01)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.infrastructure.db_supabase import SupabaseAuthorizationRequestStore"
```
