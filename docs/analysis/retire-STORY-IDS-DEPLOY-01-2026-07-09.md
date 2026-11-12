# Retirement: STORY-IDS-DEPLOY-01 — Railway deployability

**Date:** 2026-07-09 · **Method:** `.cursor/rules/analysis.mdc` — code-verified  
**Decision:** remove `railway-deploy/` package from active backlog; deploy SSOT → [`run-and-healthcheck.md`](../runbook/run-and-healthcheck.md)

## Why retired (not marked Done)

Story AC described `startCommand` in `railway.json`; as-built uses split [`railpack.json`](../../railpack.json) + [`railway.json`](../../railway.json). Operator confirmed Railway deploy works. Keeping a stale story with unchecked AC would mislead; runbook already documents the real layout.

## AC vs code (final)

| Item | Story expected | As-built | Verdict |
|------|----------------|----------|---------|
| T01 startCommand | `railway.json` | [`railpack.json:7`](../../railpack.json) | Done (different file) |
| T02 pilot env | Railway variables | [`schema.py:183-197`](../../src/core/config/schema.py) `pilot_required` | Done (ops) |
| T03 CORS | explicit origins | `asgi_app.py` middleware + [`cors-allowed-origins.md`](../runbook/cors-allowed-origins.md) | Done |
| T04 DEV_OTP_ECHO | flag + log OTP | grep `DEV_OTP_ECHO` in `src/` → **0** | **Dropped** (operator) |
| T05 JWKS live | ES256 `/me` | SEC-06 Done; no `SUPABASE_JWT_SECRET` in src | Done |
| T06 deploy gate | `/health` 200, smoke | `make smoke`; operator Railway deploy green | Done (ops) |
| requirements.txt | — | present for Railpack | Done |

## Dropped scope

**D-4 / DEV_OTP_ECHO** — OTP echo in railway logs under pilot. Alternatives documented in [`sms-mock-testing.md`](../runbook/sms-mock-testing.md) §6 (Telnyx, local+file).

## Index sync

| Artifact | Change |
|----------|--------|
| `docs/tasks/backlog-stories/railway-deploy/` | deleted |
| `identity-backlog-dashboard.md` | packages 11→10, stories 34→33, Todo 3→2, **91%** |
| `backlog-stories/INDEX.md` | DEPLOY-01 removed from open list |
| `bullrun-launch-index.md` | next = ONB-01 only; DEPLOY registry row removed |

## Operator evidence

Railway deploy operational (operator-validated 2026-07-09). No deploy URL stored in git.
