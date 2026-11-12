# Story acceptance gate — STORY-IDS-REQ9-02-check-env-required

- **Story:** `make check-env` require `.env` (mini)
- **Package:** `pkg-000054-20260926-epic-ids-16-req9-02-check-env-required.yaml`
- **Result:** PASS
- **Date:** 2026-09-26T12:21:29Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| AC-IDS-REQ902-01: `make check-env` requires `./.env` | PASS | t01 — [`Makefile:15-21`](../../../../../../../Makefile); fail-closed empty-dir |
| AC-IDS-REQ902-02: pattern matches post-REQ9-01 serve/dev | PASS | identical `set -a && . ./.env && set +a` vs [`Makefile:4-11`](../../../../../../../Makefile) |
| AC-IDS-REQ902-03: REQ9-01 Done evidence cited | PASS | Hard dep: pipeline REQ9-01 Meta **Status: 🟢 Done** · **Wave:** pkg-000053 · **P3 Done:** 2026-09-26T12:08:20Z ([`STORY-IDS-REQ9-01-make-env-required.md`](../STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md)); AC-IDS-REQ901-01 Pass via serve/dev required shell-source |

## Commands (live verification 2026-09-26T12:21:29Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
cd doge-identity-service && .venv/bin/python -m pytest tests/ -q -m "not live_integration"
# 456 passed, 13 deselected
rg -n 'if \[ -f \./\.env \]|set -a && \. \./\.env' doge-identity-service/Makefile
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
