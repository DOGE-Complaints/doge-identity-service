# STORY-IDS-OAUTH-03 — Durable OAuth-стор (Supabase Postgres) против потери при редеплое

## Meta
- **Key:** `STORY-IDS-OAUTH-03-persistent-token-store-supabase`
- **Epic:** `EPIC-IDS-ONBOARDING` (umbrella); код-алиас `EPIC-IDS-OAUTH`
- **Type:** story
- **Status:** 🟢 Done
- **Источник:** [`oauth-validation-2026-06-12`](../../../analysis/oauth-validation-2026-06-12.md) (durability MEDIUM); решение 2026-06-12 — «хранить в Supabase, не in-memory».
- **Зависит от:** [STORY-IDS-OAUTH-01](STORY-IDS-OAUTH-01-oauth-server-endpoints.md) (**🟢 построен** — authorization_request-store + code-выдача, pkg-000029)

## Зачем простыми словами
Любой редеплой/рестарт **при `DB_BACKEND=in_memory`** обнуляет in-memory `OAuthTokenService` — теряются **authorization codes** и **состояние handshake** (`oauth_request_id`). Это рвало логин «в процессе» и не работало при нескольких инстансах. **OAUTH-03 (🟢)** добавил хранение в **Supabase Postgres** при `DB_BACKEND=supabase`; demo/offline-тесты по-прежнему используют in-memory.

**Важно (что НЕ нужно хранить):** access-токены — **stateless HS256-JWT**, валидируются подписью+`exp` без хранилища ([`claims_from_access_token_jwt`](../../../../src/core/oauth/access_token_jwt.py)) — они **переживают редеплой** при стабильном `OAUTH_ACCESS_TOKEN_SECRET`. Персистится только короткоживущее состояние выдачи.

## Решение владельца (зафиксировать)
Остаёмся собственным **Authorization Server** (ADR-IDS-002 — Supabase-managed OAuth отклонён: контроль над claims/scope/TTL). Supabase используется **только как слой персистентности (Postgres)**, не как OAuth-сервер. Access-токены остаются stateless.

## Scope
- **Миграция Supabase:** таблицы `oauth_authorization_requests` (handshake) и `oauth_authorization_codes` (выданные codes). Поля (минимум): `id/code | request_id`, `supabase_user_id`, `client_id`, `redirect_uri`, `scopes`, `code_challenge`, `code_challenge_method`, `state`, `expires_at`, `consumed bool`, `created_at`. Индекс по `expires_at` (очистка), уникальность `code`. По образцу [`supabase/migrations/`](../../../../supabase/migrations/).
- **`SupabaseOAuthTokenService`** (PostgREST, как другие Supabase-репозитории [`db_supabase.py`](../../../../src/core/infrastructure/db_supabase.py)): реализует тот же контракт, что `InMemoryOAuthTokenService` (`issue_authorization_code`/`issue_access_token`/`validate_access_token`) + хранение `authorization_request`. Single-use (`consumed`) и TTL (`expires_at`) enforce'ятся в сторе.
- **DI-выбор по backend:** при `DB_BACKEND=supabase` — `SupabaseOAuthTokenService` + `SupabaseAuthorizationRequestStore`; при `in_memory` (demo/tests) — `InMemoryOAuthTokenService` + `InMemoryAuthorizationRequestStore` ([`providers.py:91-103`](../../../../src/core/infrastructure/providers.py)).
- **Access-токен — без изменений** (stateless HS256, та же выдача/валидация).

## Вне scope
- Refresh-токены (в MVP не выдаём — [req-14](../../../requirements/14-oauth-server-custom-gpt.md)).
- Revocation-лист (post-MVP; access-токен короткоживущий).
- Перенос OAuth-сервера в Supabase (отклонено ADR-IDS-002).
- OAuth client-store — уже есть `SupabaseOAuthClientStore` (из env).

## Точки в коде (построено, pkg-000033)

- **Миграция:** [`20260624000001_oauth_authorization_tables.sql`](../../../../supabase/migrations/20260624000001_oauth_authorization_tables.sql) — `oauth_authorization_requests` + `oauth_authorization_codes` (TTL-индексы, RLS).
- **Supabase stores:** `SupabaseAuthorizationRequestStore` (save/get/consume) и `SupabaseOAuthTokenService` (issue code/token, атомарный consume кода через conditional PATCH) — [`db_supabase.py`](../../../../src/core/infrastructure/db_supabase.py).
- **DI переключение:** `db_backend=="supabase"` → Supabase-сторы; `in_memory` → `InMemory*` — [`providers.py:91-103`](../../../../src/core/infrastructure/providers.py).
- **Stateless access-token:** `claims_from_access_token_jwt` — без обращения к БД — [`access_token_jwt.py`](../../../../src/core/oauth/access_token_jwt.py) (общий для InMemory и Supabase путей).
- **Demo/in-memory:** `InMemoryOAuthTokenService` / `InMemoryAuthorizationRequestStore` — только при `DB_BACKEND=in_memory` ([`repositories.py:430+`](../../../../src/core/infrastructure/repositories.py)).

## Acceptance Criteria
- [x] Миграция создаёт `oauth_authorization_requests` + `oauth_authorization_codes` (TTL-индекс, single-use).
- [x] `SupabaseOAuthTokenService` реализует контракт `OAuthTokenService` + хранение request-state; single-use/TTL в БД.
- [x] `DB_BACKEND=supabase` → используется Supabase-стор; `in_memory` → прежний (тесты зелёные).
- [x] **Durability-тест:** code/request, «выданный» до пересоздания стора, валиден после (эмуляция редеплоя); просроченный/использованный → `invalid_grant`.
- [x] Access-токен валиден после пересоздания стора **без** обращения к БД (stateless подтверждён тестом).
- [x] Offline-тесты (mock PostgREST) зелёные; миграция — в `test_supabase_migrations_sql`.

## Парадигма-якорь
[ADR-IDS-002](../../../requirements/05-adr-log.md) (мы — Authorization Server), [req-14](../../../requirements/14-oauth-server-custom-gpt.md), [08-supabase-migrations](../../../requirements/08-supabase-migrations.md).
