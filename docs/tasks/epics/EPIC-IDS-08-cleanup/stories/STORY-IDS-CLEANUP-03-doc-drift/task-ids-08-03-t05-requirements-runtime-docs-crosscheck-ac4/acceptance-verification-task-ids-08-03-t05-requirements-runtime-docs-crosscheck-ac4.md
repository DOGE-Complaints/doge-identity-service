# Acceptance verification — task-ids-08-03-t05-requirements-runtime-docs-crosscheck-ac4

- **Wave:** pkg-000014 · **Date:** 2026-06-02

## Grep matrix (post-fix)

| Check | Result |
|-------|--------|
| `story_drafts` in `/ready` list (runtime-docs) | PASS — removed stale gap; `db_supabase.py:287-291` lists 3 tables only |
| Story routes in `01-api.md` as live code | PASS — section replaced; CLEANUP-01 removal noted |
| `story_drafts` «в коде» in `05-data-model.md` | PASS — historical removal section |
| DOC-3 note in `02-data-bootstrap.md:33` | PASS — removed (req-08 now aligned) |
| `eid/callback` in req-02/03, `.env.example`, `07-env`, runtime-docs | PASS — grep 0 in aligned files |
| `07-env-configuration-spec.md` redirect URI | PASS — authentigate callback |

## AC/DoD

| Criterion | Result |
|-----------|--------|
| Story AC #4: no contradictions migrations/callback/story scope | PASS |
| `02-data-bootstrap.md`, `01-api.md`, `05-data-model.md` updated | PASS |
| Optional `07-env-configuration-spec.md` aligned | PASS |
| BULLRUN-PHASE-LOG + acceptance in task folder | PASS |
