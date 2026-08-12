# Epic acceptance gate — EPIC-IDS-02

- Epic: `EPIC-IDS-02-fastapi-transport`
- Gate status: **PASS** (automated AC + unit/transport tests)
- Package: `pkg-000003`
- Verified: 2026-05-29

## Story gates

| Story | Gate |
|-------|------|
| STORY-IDS-02-01 | [PASS](./stories/STORY-IDS-02-01-response-envelope-error-trace-id/story-acceptance-gate-STORY-IDS-02-01.md) |
| STORY-IDS-02-02 | [PASS](./stories/STORY-IDS-02-02-logging-setup/story-acceptance-gate-STORY-IDS-02-02.md) |
| STORY-IDS-02-03 | [PASS](./stories/STORY-IDS-02-03-auth-security-primitives-bearer-stub/story-acceptance-gate-STORY-IDS-02-03.md) |
| STORY-IDS-02-04 | [PASS](./stories/STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware/story-acceptance-gate-STORY-IDS-02-04.md) |
| STORY-IDS-02-05 | [PASS](./stories/STORY-IDS-02-05-routes-contract-health-ready-identity-stubs/story-acceptance-gate-STORY-IDS-02-05.md) |

## Automated evidence

- `pytest tests/ -q -m "not live_integration"` → **40 passed**
- `core.api.asgi_app:app` importable (`make serve` entrypoint)
- Transport tests: `/health`, `/ready`, `/me` 401/501, `OPTIONS /me`, route table

## Operator smoke (§8 epic — manual)

```bash
cd doge-identity-service && make serve
# curl health, ready, me без auth → 401, me с Bearer → 501
```
