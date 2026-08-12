# Acceptance verification — task-ids-08-03-t04-req02-req03-gateway-direction-sync

- **Wave:** pkg-000014 · **Date:** 2026-06-02

## Evidence

| Claim | Source |
|-------|--------|
| Story rows removed from MVP scope | `req-02` — no Story authorization / Story drafts rows; added to «не входит» |
| eID callback path factual | `req-02:13`, `req-03:37,83` — `/auth/authentigate/callback` |
| Layer 3 without story routes | `req-03:37-38` — OAuth + eID only |
| Flow B gateway-direct | `req-03:93-116` — GPT → gateway `/intake/stories`; identity does not forward |
| Code: no story routes | `grep story src/` = 0 |

## AC/DoD

| Criterion | Result |
|-----------|--------|
| Story AC #3: req-02 MVP scope — stories not in identity | PASS |
| Story AC #3: req-03 Layer 3 + Flow B gateway-direct | PASS |
| Cross-ref `09-gateway-expectations.md` | PASS |
| BULLRUN-PHASE-LOG + acceptance in task folder | PASS |
