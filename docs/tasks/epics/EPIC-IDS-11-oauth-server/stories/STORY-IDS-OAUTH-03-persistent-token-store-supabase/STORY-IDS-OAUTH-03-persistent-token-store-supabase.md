# STORY-IDS-OAUTH-03 — Durable OAuth-стор (Supabase Postgres) против потери при редеплое

## Meta
- **Key:** `STORY-IDS-OAUTH-03-persistent-token-store-supabase`
- **Parent Epic:** [`../../EPIC-IDS-11-oauth-server.md`](../../EPIC-IDS-11-oauth-server.md)
- **Epic alias (код/backlog):** `EPIC-IDS-OAUTH` · продуктовый зонтик [`EPIC-IDS-ONBOARDING`](../../../../backlog-stories/identity-onboarding/EPIC-IDS-ONBOARDING.md)
- **Status:** 🟢 Done
- **source:** [`doge-identity-service/docs/tasks/backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md)
- **Decision Ref:** [`../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md); [`oauth-validation-2026-06-12`](../../../../../analysis/oauth-validation-2026-06-12.md) (durability MEDIUM)
- **Источник:** [`oauth-validation-2026-06-12`](../../../../../analysis/oauth-validation-2026-06-12.md) (durability MEDIUM); решение 2026-06-12 — «хранить в Supabase, не in-memory».
- **Зависит от:** [STORY-IDS-OAUTH-01](../../../../backlog-stories/oauth/STORY-IDS-OAUTH-01-oauth-server-endpoints.md) (**🟢 построен** — authorization_request-store + code-выдача, pkg-000029)

## Зачем простыми словами
Любой редеплой/рестарт сейчас обнуляет in-memory `OAuthTokenService` — теряются **authorization codes** и **состояние handshake** (`oauth_request_id`). Это рвёт логин «в процессе» (5-минутное окно) и не работает при нескольких инстансах. Делаем хранение этого состояния в **Supabase Postgres**, чтобы редеплой/масштабирование не ломали авторизацию.

**Важно (что НЕ нужно хранить):** access-токены — **stateless HS256-JWT**, валидируются подписью+`exp` без хранилища ([`validate_access_token`/`_decode_jwt`](../../../../../../src/core/infrastructure/repositories.py)) — они **уже переживают редеплой** при стабильном `OAUTH_ACCESS_TOKEN_SECRET`. Персистить нужно только короткоживущее состояние выдачи.

## Решение владельца (зафиксировать)
Остаёмся собственным **Authorization Server** (ADR-IDS-002 — Supabase-managed OAuth отклонён: контроль над claims/scope/TTL). Supabase используется **только как слой персистентности (Postgres)**, не как OAuth-сервер. Access-токены остаются stateless.

## Scope
- **Миграция Supabase:** таблицы `oauth_authorization_requests` (handshake) и `oauth_authorization_codes` (выданные codes). Поля (минимум): `id/code | request_id`, `supabase_user_id`, `client_id`, `redirect_uri`, `scopes`, `code_challenge`, `code_challenge_method`, `state`, `expires_at`, `consumed bool`, `created_at`. Индекс по `expires_at` (очистка), уникальность `code`. По образцу [`supabase/migrations/`](../../../../../../supabase/migrations/).
- **`SupabaseOAuthTokenService`** (PostgREST, как другие Supabase-репозитории [`db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py)): реализует тот же контракт, что `InMemoryOAuthTokenService` (`issue_authorization_code`/`issue_access_token`/`validate_access_token`) + хранение `authorization_request`. Single-use (`consumed`) и TTL (`expires_at`) enforce'ятся в сторе.
- **DI-выбор по backend:** при `DB_BACKEND=supabase` — `SupabaseOAuthTokenService` + `SupabaseAuthorizationRequestStore`; при `in_memory` (demo/tests) — `InMemoryOAuthTokenService` + `InMemoryAuthorizationRequestStore` ([`providers.py:91-103`](../../../../../../src/core/infrastructure/providers.py)).
- **Access-токен — без изменений** (stateless HS256, та же выдача/валидация).

## Вне scope
- Refresh-токены (в MVP не выдаём — [req-14](../../../../../requirements/14-oauth-server-custom-gpt.md)).
- Revocation-лист (post-MVP; access-токен короткоживущий).
- Перенос OAuth-сервера в Supabase (отклонено ADR-IDS-002).
- OAuth client-store — уже есть `SupabaseOAuthClientStore` (из env).

## Точки в коде (построено, pkg-000033)

- **Миграция:** [`20260624000001_oauth_authorization_tables.sql`](../../../../../../supabase/migrations/20260624000001_oauth_authorization_tables.sql) — `oauth_authorization_requests` + `oauth_authorization_codes` (TTL-индексы, RLS).
- **Supabase stores:** `SupabaseAuthorizationRequestStore` (save/get/consume) и `SupabaseOAuthTokenService` (issue code/token, атомарный consume кода через conditional PATCH) — [`db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py).
- **DI переключение:** `db_backend=="supabase"` → Supabase-сторы; `in_memory` → `InMemory*` — [`providers.py:91-103`](../../../../../../src/core/infrastructure/providers.py).
- **Stateless access-token:** `claims_from_access_token_jwt` — без обращения к БД — [`access_token_jwt.py`](../../../../../../src/core/oauth/access_token_jwt.py) (общий для InMemory и Supabase путей).
- **Demo/in-memory:** `InMemoryOAuthTokenService` / `InMemoryAuthorizationRequestStore` — только при `DB_BACKEND=in_memory` ([`repositories.py:430+`](../../../../../../src/core/infrastructure/repositories.py)).

## Acceptance Criteria
- [x] Миграция создаёт `oauth_authorization_requests` + `oauth_authorization_codes` (TTL-индекс, single-use).
- [x] `SupabaseOAuthTokenService` реализует контракт `OAuthTokenService` + хранение request-state; single-use/TTL в БД.
- [x] `DB_BACKEND=supabase` → используется Supabase-стор; `in_memory` → прежний (тесты зелёные).
- [x] **Durability-тест:** code/request, «выданный» до пересоздания стора, валиден после (эмуляция редеплоя); просроченный/использованный → `invalid_grant`.
- [x] Access-токен валиден после пересоздания стора **без** обращения к БД (stateless подтверждён тестом).
- [x] Offline-тесты (mock PostgREST) зелёные; миграция — в `test_supabase_migrations_sql`.

## Парадигма-якорь
[ADR-IDS-002](../../../../../requirements/05-adr-log.md) (мы — Authorization Server), [req-14](../../../../../requirements/14-oauth-server-custom-gpt.md), [08-supabase-migrations](../../../../../requirements/08-supabase-migrations.md).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-11-03-t01-oauth-supabase-migration-sql`](./task-ids-11-03-t01-oauth-supabase-migration-sql/README.md) | pkg-000033 |
| 2 | [`task-ids-11-03-t02-supabase-authorization-request-store`](./task-ids-11-03-t02-supabase-authorization-request-store/README.md) | pkg-000033 |
| 3 | [`task-ids-11-03-t03-supabase-oauth-token-service`](./task-ids-11-03-t03-supabase-oauth-token-service/README.md) | pkg-000033 |
| 4 | [`task-ids-11-03-t04-di-oauth-store-backend-selection`](./task-ids-11-03-t04-di-oauth-store-backend-selection/README.md) | pkg-000033 |
| 5 | [`task-ids-11-03-t05-offline-supabase-oauth-store-tests`](./task-ids-11-03-t05-offline-supabase-oauth-store-tests/README.md) | pkg-000033 |
| 6 | [`task-ids-11-03-t06-durability-and-stateless-jwt-tests`](./task-ids-11-03-t06-durability-and-stateless-jwt-tests/README.md) | pkg-000033 |
| 7 | [`task-ids-11-03-t07-story-acceptance-verification`](./task-ids-11-03-t07-story-acceptance-verification/README.md) | pkg-000033 |
