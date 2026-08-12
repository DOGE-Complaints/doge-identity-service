# Acceptance verification — task-ids-08-03-t01-req08-req02-migration-count-doc3

- **Wave:** pkg-000014 · **Date:** 2026-06-02

## Evidence

| Claim | Source |
|-------|--------|
| 4 operational migration files on disk | `ls supabase/migrations/202605*.sql` → 4 operational + 1 deprecated `story_drafts` |
| req-08 structure lists migration 4 | `docs/requirements/08-supabase-migrations.md:12-19` — tree + operational set note |
| req-08 §Migration 4 body | `docs/requirements/08-supabase-migrations.md:245+` — `20260526000001_eid_sessions_provider_abstraction.sql` |
| req-02 scope row aligned | `docs/requirements/02-scope-and-boundaries.md:18` — «4 operational migrations» |

## AC/DoD

| Criterion | Result |
|-----------|--------|
| Story AC #1: req-08 §structure includes migration 4 | PASS |
| Story AC #1: req-02:20 without «3 миграции» drift | PASS |
| BULLRUN-PHASE-LOG + acceptance in task folder | PASS |
