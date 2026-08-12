## Task workspace — `task-ids-11-03-t04-di-oauth-store-backend-selection`

- Story: [`../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md)
- Prerequisite: t02 SupabaseAuthorizationRequestStore; t03 SupabaseOAuthTokenService

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000033`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) Scope §DI-выбор; Story AC #3  
---

## Task: implement — DI backend selection for OAuth stores

### Цель
При `DB_BACKEND=supabase` поднимать Supabase OAuth stores; при `in_memory` — сохранить текущие InMemory* реализации.

### Почему это важно
Сейчас [`providers.py:89-93`](../../../../../../../src/core/infrastructure/providers.py) всегда создаёт `InMemoryOAuthTokenService` + `InMemoryAuthorizationRequestStore` даже когда profile/eID repos уже Supabase-backed.

### Факты из кода
1. OAuth DI gap: [`providers.py:89-93`](../../../../../../../src/core/infrastructure/providers.py).
2. Supabase branch starts at [`providers.py:68-85`](../../../../../../../src/core/infrastructure/providers.py) — `SupabaseDatabase.from_http`, other repos wired.
3. Factory slots: [`service_factory.py:32-33`](../../../../../../../src/core/infrastructure/service_factory.py) — `oauth_token_service`, `oauth_authorization_request_store`.
4. Handlers unchanged: [`handlers.py`](../../../../../../../src/core/oauth/handlers.py) consume ports via `ApiDependencies`.

### Gap / Проблема
`DB_BACKEND=supabase` не переключает OAuth persistence — durability AC не достижим в pilot.

### AC/DoD
- [x] (P0) `db_backend=supabase` → `SupabaseAuthorizationRequestStore` + `SupabaseOAuthTokenService` (shared `supabase_db`, `resolved_config`, `oauth_client_store`).
- [x] (P0) `db_backend=in_memory` → `InMemoryAuthorizationRequestStore` + `InMemoryOAuthTokenService` (unchanged behavior).
- [x] (P0) `DefaultServiceFactory` receives correct instances in both branches.
- [x] (P1) Traceability: Story AC #3.

### Где менять код
- `doge-identity-service/src/core/infrastructure/providers.py`

### Out of scope
- Store implementation bodies (t02, t03)
- Config schema changes
- Gateway / runtime-docs

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_service_factory.py tests/test_api_dependencies.py -q
```
