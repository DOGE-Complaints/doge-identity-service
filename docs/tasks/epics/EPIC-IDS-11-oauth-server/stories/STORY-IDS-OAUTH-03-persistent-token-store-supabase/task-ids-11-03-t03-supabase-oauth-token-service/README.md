## Task workspace — `task-ids-11-03-t03-supabase-oauth-token-service`

- Story: [`../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md)
- Prerequisite: t01 migration SQL

---
**Приоритет:** P0  
**Сложность:** L  
**Статус:** done  
**Wave:** `pkg-000033`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) Scope §`SupabaseOAuthTokenService`; Story AC #2 (codes part)  
---

## Task: implement — SupabaseOAuthTokenService

### Цель
Реализовать `OAuthTokenService` через PostgREST + `oauth_authorization_codes` — персистентная выдача/обмен authorization codes с single-use и TTL.

### Почему это важно
Authorization codes сейчас в `InMemoryOAuthTokenService._codes` ([`repositories.py:461`](../../../../../../../src/core/infrastructure/repositories.py)) — редеплой обнуляет активные логины.

### Факты из кода
1. Protocol: [`contracts.py:139-161`](../../../../../../../src/core/domain/contracts.py) — `issue_authorization_code`, `issue_access_token`, `validate_access_token`.
2. In-memory logic to mirror: [`repositories.py:463-545`](../../../../../../../src/core/infrastructure/repositories.py) — PKCE, `invalid_grant`, JWT issue/validate.
3. Access token **stateless** (не персистить): [`repositories.py:536-545`](../../../../../../../src/core/infrastructure/repositories.py) — `_decode_jwt` only.
4. Client secret check uses `oauth_client_store` — same as in-memory path.
5. PostgREST insert/update pattern: [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py).

### Gap / Проблема
Нет `SupabaseOAuthTokenService`; `OAuthTokenService` always in-memory in [`providers.py:89-92`](../../../../../../../src/core/infrastructure/providers.py).

### AC/DoD
- [x] (P0) `SupabaseOAuthTokenService` implements `OAuthTokenService` protocol.
- [x] (P0) `issue_authorization_code` persists row; `issue_access_token` marks `consumed=true`, enforces TTL/PKCE/client match (mirror in-memory errors).
- [x] (P0) `validate_access_token` — stateless JWT decode (reuse shared JWT helpers from in-memory or extract minimal shared module).
- [x] (P0) Single-use + `expires_at` enforced in DB layer (update/read with conditions).
- [x] (P1) Traceability: Story AC #2; Scope «Access-токен — без изменений».

### Где менять код
- `doge-identity-service/src/core/infrastructure/db_supabase.py`
- Optional refactor: shared JWT encode/decode if duplication exceeds in-memory (minimal scope)

### Out of scope
- `AuthorizationRequestStore` (t02)
- Refresh tokens / revocation list (backlog «Вне scope»)
- DI wiring (t04)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -c "from core.infrastructure.db_supabase import SupabaseOAuthTokenService"
```
