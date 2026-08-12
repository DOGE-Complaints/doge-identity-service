# STORY-IDS-04-05: Supabase JWT validator + `SupabaseJwtBearerTokenAuth`

## Meta
- Key: `STORY-IDS-04-05-supabase-jwt-bearer-auth`
- Parent Epic: [`../../EPIC-IDS-04-soa-service-factory.md`](../../EPIC-IDS-04-soa-service-factory.md)
- Type: Technical Story (Auth)
- Status: Done
- Decision Ref: [`../../EPIC-IDS-04-soa-service-factory.md`](../../EPIC-IDS-04-soa-service-factory.md) §6 Story 5

## Story Goal
Заменить stub auth: `SupabaseJwtValidatorImpl` (joserfc HS256) + `SupabaseJwtBearerTokenAuth` в auth-цепочке FastAPI.

## AC / DoD (из EPIC-IDS-04 §6 Story 5)
- [x] `SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(valid_token)` → `UserClaims` с корректным `supabase_user_id` (req-09 acceptance).
- [x] `SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(expired_token)` raises `JwtValidationError` (req-09 acceptance).
- [x] `SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(alg_none_token)` raises `JwtValidationError` (req-09 §"Атака на alg: none").
- [x] `SupabaseJwtValidatorImpl(jwt_secret=S, supabase_url=U).validate(token_with_iss_mismatch)` raises `JwtValidationError`.
- [x] `SupabaseJwtBearerTokenAuth(validator=...)` корректно конвертирует `JwtValidationError` → `UnauthorizedError(code="AUTHENTICATION_REQUIRED")`.
- [x] `GET /me` с валидным токеном — `bearer_token_auth.validate(headers)` возвращает `UserClaims`; `/me` остаётся stub до функционального эпика, но 401 больше не возвращается.

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-04-05-t01-supabase-jwt-validator-impl`](./task-ids-04-05-t01-supabase-jwt-validator-impl/README.md) | pkg-000005 |
| 2 | [`task-ids-04-05-t02-supabase-jwt-bearer-token-auth`](./task-ids-04-05-t02-supabase-jwt-bearer-token-auth/README.md) | pkg-000005 |
| 3 | [`task-ids-04-05-t03-story5-acceptance-verification`](./task-ids-04-05-t03-story5-acceptance-verification/README.md) | pkg-000005 |
