# STORY-IDS-02-03: Auth security primitives — BearerTokenAuth stub

## Meta
- Key: `STORY-IDS-02-03-auth-security-primitives-bearer-stub`
- Parent Epic: [`../../../EPIC-IDS-02-fastapi-transport.md`](../../../EPIC-IDS-02-fastapi-transport.md)
- Type: Technical Story (Security Primitive)
- Status: Done
- Decision Ref: [`../../../../requirements/09-supabase-jwt-validation.md`](../../../../requirements/09-supabase-jwt-validation.md)

## Story Goal
Подготовить transport-level auth primitives: `UnauthorizedError`, protocol `BearerTokenAuth`, stub implementation и dependency `get_current_user`.

## AC / DoD (из EPIC-IDS-02)
- [x] `StubBearerTokenAuth().validate({})` бросает `UnauthorizedError`
- [x] `StubBearerTokenAuth().validate({"authorization": "Bearer xyz"})` возвращает stub `UserClaims`
- [x] `BearerTokenAuth` оформлен как Protocol
- [x] `UnauthorizedError.code == "AUTHENTICATION_REQUIRED"`

## Story gate
- [story-acceptance-gate-STORY-IDS-02-03.md](./story-acceptance-gate-STORY-IDS-02-03.md) — **PASS** (2026-05-29)

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-02-03-t01-unauthorized-error-and-protocol`](./task-ids-02-03-t01-unauthorized-error-and-protocol/README.md) | pkg-000003 |
| 2 | [`task-ids-02-03-t02-stub-bearer-auth-and-current-user`](./task-ids-02-03-t02-stub-bearer-auth-and-current-user/README.md) | pkg-000003 |
| 3 | [`task-ids-02-03-t03-auth-primitives-verification`](./task-ids-02-03-t03-auth-primitives-verification/README.md) | pkg-000003 |
