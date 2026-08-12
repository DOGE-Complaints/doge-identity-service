## Task workspace — `task-ids-11-04-t01-oauth-request-context-schema`

- Story: [`../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md)
- Prerequisite: STORY-IDS-OAUTH-03 🟢 Done (pkg-000033)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000034`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-04-verify-gate-and-verification-required.md) Scope §relay (storage)  
---

## Task: implement — OAuth request context schema (model + migration + stores)

### Цель
Расширить `AuthorizationRequest` и durable handshake-стор колонками `requested_action` и `return_context` — prerequisite для relay authorize→complete.

### Почему это важно
Поля `return_context`/`requested_action` есть на `VerificationSession`, но не на OAuth handshake; без schema relay невозможен (Story Scope §relay).

### Факты из кода
1. `AuthorizationRequest` без контекста: [`models.py:138-147`](../../../../../../../src/core/domain/models.py).
2. `VerificationSession` с полями: [`models.py:56-58`](../../../../../../../src/core/domain/models.py).
3. Durable table без колонок: [`20260624000001_oauth_authorization_tables.sql`](../../../../../../../supabase/migrations/20260624000001_oauth_authorization_tables.sql).
4. In-memory store: [`repositories.py`](../../../../../../../src/core/infrastructure/repositories.py) — `InMemoryAuthorizationRequestStore`.
5. Supabase store: [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) — `SupabaseAuthorizationRequestStore`.
6. Action enum: `eid:verify` \| `stories:submit` — [`20260525000002_create_eid_verification_sessions.sql`](../../../../../../../supabase/migrations/20260525000002_create_eid_verification_sessions.sql).
7. Migration tests: [`tests/test_supabase_migrations_sql.py`](../../../../../../../tests/test_supabase_migrations_sql.py).

### Gap / Проблема
OAuth handshake не хранит `requested_action`/`return_context` ни в доменной модели для `AuthorizationRequest`, ни в Supabase/in-memory stores.

### AC/DoD
- [ ] (P0) `AuthorizationRequest` расширен полями `requested_action` (optional enum) и `return_context` (optional string).
- [ ] (P0) Новая миграция `ALTER oauth_authorization_requests` добавляет колонки; optional CHECK на допустимые action values.
- [ ] (P0) `InMemoryAuthorizationRequestStore` и `SupabaseAuthorizationRequestStore` читают/пишут новые поля.
- [ ] (P1) Entry в `test_supabase_migrations_sql.py` для новой миграции.
- [ ] (P1) Traceability: prerequisite для Story AC #1 (t02).

### Где менять код
- `doge-identity-service/src/core/domain/models.py`
- `doge-identity-service/supabase/migrations/` (new ALTER migration)
- `doge-identity-service/src/core/infrastructure/repositories.py`
- `doge-identity-service/src/core/infrastructure/db_supabase.py`
- `doge-identity-service/tests/test_supabase_migrations_sql.py`

### Out of scope
- OAuth handler relay (t02)
- Verify-gate branch (t03)
- `verification_required` contract (t04)

### Проверка
```bash
cd doge-identity-service
grep -E 'requested_action|return_context' src/core/domain/models.py
test -f supabase/migrations/*oauth*context*.sql || ls supabase/migrations/*oauth*
```
