# Acceptance verification — task-ids-08-03-t06-story-acceptance-verification

- **Story:** STORY-IDS-CLEANUP-03-doc-drift
- **Wave:** pkg-000014 · **Date:** 2026-06-02

## Story AC

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | req-08/req-02 reflect 4 migrations | PASS | t01 artifact; `req-08:12-19`, `req-02:18`; `20260526000001` on disk |
| 2 | `.env.example` redirect URI matches route | PASS | t02 artifact; `.env.example:51` + `asgi_app.py:209` |
| 3 | req-15 deprecated; req-02/03 gateway→identity | PASS | t03–t04 artifacts; `req-15:3,5`; Flow B gateway-direct |
| 4 | requirements ↔ runtime-docs aligned | PASS | t05 artifact; grep matrix — no stale story_drafts/`eid/callback` drift |

## Verification commands

```bash
cd doge-identity-service
grep -n "provider_abstraction\|20260526000001" docs/requirements/08-supabase-migrations.md
grep AUTHENTIGATE_REDIRECT_URI .env.example
head -6 docs/requirements/15-story-authorization.md | grep -i deprecated
grep -rn "eid/callback" docs/runtime-docs/ docs/requirements/02-scope-and-boundaries.md docs/requirements/03-architecture-formula.md .env.example docs/requirements/07-env-configuration-spec.md
grep story_drafts src/   # expect 0
```

## Wave closure

- Tasks t01–t06: 🟢 Done
- Story status: 🟢 Done
- pkg-000014: docs-only wave complete (no pytest gate required)
