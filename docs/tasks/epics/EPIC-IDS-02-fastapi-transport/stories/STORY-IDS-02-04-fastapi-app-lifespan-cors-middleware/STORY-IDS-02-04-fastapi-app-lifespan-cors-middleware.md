# STORY-IDS-02-04: FastAPI app, lifespan, CORS, middleware, exception handlers

## Meta
- Key: `STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware`
- Parent Epic: [`../../../EPIC-IDS-02-fastapi-transport.md`](../../../EPIC-IDS-02-fastapi-transport.md)
- Type: Technical Story (ASGI Composition)
- Status: Done
- Decision Ref: [`../../../../analysis/interview-cpo-cto-epics-2026-05-27.md`](../../../../analysis/interview-cpo-cto-epics-2026-05-27.md)

## Story Goal
Собрать `create_app(config)` с CORS на этапе сборки, lifespan c DI/logging и transport middleware/exception handlers.

## AC / DoD (из EPIC-IDS-02)
- [x] `GET /health` возвращает 200 envelope
- [x] `OPTIONS /me` возвращает 200 (preflight)
- [x] `x-trace-id` отражается в envelope
- [x] `/me` без `Authorization` даёт 401 `AUTHENTICATION_REQUIRED`
- [x] `app.title == "doge-identity-service"`
- [x] `CORSMiddleware` регистрируется в `create_app`, `allow_origins` из `config.cors_allowed_origins`

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-02-04-t01-create-app-and-lifespan`](./task-ids-02-04-t01-create-app-and-lifespan/README.md) | pkg-000003 |
| 2 | [`task-ids-02-04-t02-runtime-middleware-and-exception-handlers`](./task-ids-02-04-t02-runtime-middleware-and-exception-handlers/README.md) | pkg-000003 |
| 3 | [`task-ids-02-04-t03-api-dependencies-cache-hooks`](./task-ids-02-04-t03-api-dependencies-cache-hooks/README.md) | pkg-000003 |
| 4 | [`task-ids-02-04-t04-audit-a1-cors-response-headers-test`](./task-ids-02-04-t04-audit-a1-cors-response-headers-test/README.md) | override epic_ids_02_audit_2026_05_28 |

## Open audit gaps (post-audit 2026-05-28)

| Finding | Gap task | Status |
|---------|----------|--------|
| A-1 [MEDIUM] | [t04 cors headers test](./task-ids-02-04-t04-audit-a1-cors-response-headers-test/README.md) | done |

## Story gate
- [story-acceptance-gate-STORY-IDS-02-04.md](./story-acceptance-gate-STORY-IDS-02-04.md) — **PASS** (2026-05-29)
