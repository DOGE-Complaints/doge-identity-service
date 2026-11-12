# Story acceptance gate — STORY-IDS-REQ9-01-make-env-required

- **Story:** make `.env` required on serve/dev (G8)
- **Package:** `pkg-000053-20260926-epic-ids-16-req9-01-make-env-required.yaml`
- **Result:** PASS
- **Date:** 2026-09-26T12:08:20Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-IDS-REQ901-01 (G8): `make serve`/`dev` require `./.env` | PASS | t01 — [`Makefile:4-11`](../../../../../../../Makefile); fail-closed empty-dir |
| AC-IDS-REQ901-02: `/health` `/ready` remain | PASS | [`asgi_app.py:288`](../../../../../../../src/core/api/asgi_app.py), `:295` |
| AC-IDS-REQ901-03: `SERVICE_API_TOKEN` unchanged | PASS | t02 — [`.env.example:137`](../../../../../../../.env.example) |
| AC-IDS-REQ901-04: `API_BASE_URL`/`PORT` + runbook required wording | PASS | t02 — `.env.example` + [`run-and-healthcheck.md`](../../../../../../runbook/run-and-healthcheck.md) §1–2 |

## Commands (live verification 2026-09-26T12:08:20Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
cd doge-identity-service && .venv/bin/python -m pytest tests/ -q -m "not live_integration"
# 456 passed, 13 deselected
rg -n 'if \[ -f \./\.env \]|set -a && \. \./\.env' doge-identity-service/Makefile
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
