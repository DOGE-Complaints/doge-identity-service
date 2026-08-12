# STORY-IDS-02-05: Routes contract — health/ready + identity stubs

## Meta
- Key: `STORY-IDS-02-05-routes-contract-health-ready-identity-stubs`
- Parent Epic: [`../../../EPIC-IDS-02-fastapi-transport.md`](../../../EPIC-IDS-02-fastapi-transport.md)
- Type: Technical Story (Routing Contract)
- Status: Done
- Decision Ref: [`../../../../requirements/10-me-endpoint.md`](../../../../requirements/10-me-endpoint.md), [`../../../../requirements/11-eid-verification-flow.md`](../../../../requirements/11-eid-verification-flow.md), [`../../../../requirements/14-oauth-server-custom-gpt.md`](../../../../requirements/14-oauth-server-custom-gpt.md), [`../../../../requirements/15-story-authorization.md`](../../../../requirements/15-story-authorization.md)

## Story Goal
Закрепить contract маршрутов: реальные `/health`, `/ready` и stub-handlers для identity endpoints без бизнес-логики.

## AC / DoD (из EPIC-IDS-02)
- [x] `/health` -> 200, `data.status == "ok"`
- [x] `/ready` (`in_memory`) -> 200, `db_backend == "in_memory"`, `db_ready is True`
- [x] `/me` без token -> 401 `AUTHENTICATION_REQUIRED`
- [x] `/me` с bearer stub -> 501 `NOT_IMPLEMENTED`
- [x] `OPTIONS /me` -> 200
- [x] `app.routes` содержит все paths из таблицы Story 5
- [x] `asgi_app.py` не содержит бизнес-логики

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-02-05-t01-health-and-readiness-handlers`](./task-ids-02-05-t01-health-and-readiness-handlers/README.md) | pkg-000003 |
| 2 | [`task-ids-02-05-t02-identity-route-contract-stubs`](./task-ids-02-05-t02-identity-route-contract-stubs/README.md) | pkg-000003 |
| 3 | [`task-ids-02-05-t03-options-preflight-contract`](./task-ids-02-05-t03-options-preflight-contract/README.md) | pkg-000003 |
| 4 | [`task-ids-02-05-t04-audit-a2-ready-supabase-503-test`](./task-ids-02-05-t04-audit-a2-ready-supabase-503-test/README.md) | override epic_ids_02_audit_2026_05_28 |

## Open audit gaps (post-audit 2026-05-28)

| Finding | Gap task | Status |
|---------|----------|--------|
| A-2 [LOW] | [t04 ready supabase 503 test](./task-ids-02-05-t04-audit-a2-ready-supabase-503-test/README.md) | done |

## Story gate
- [story-acceptance-gate-STORY-IDS-02-05.md](./story-acceptance-gate-STORY-IDS-02-05.md) — **PASS** (2026-05-29)
