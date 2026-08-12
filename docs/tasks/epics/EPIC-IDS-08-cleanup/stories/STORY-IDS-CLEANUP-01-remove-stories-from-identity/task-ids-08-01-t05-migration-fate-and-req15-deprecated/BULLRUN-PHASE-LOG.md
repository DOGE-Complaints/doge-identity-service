# BULLRUN-PHASE-LOG

- **Wave:** pkg-000011
- **Process:** P3 Execute STORY-IDS-CLEANUP-01 t05
- **Date:** 2026-06-05

| Phase | Status | Evidence |
|-------|--------|----------|
| Decision | Done | Migration **retained** on disk with `DEPRECATED — identity scope removed 2026-06` header |
| Implement | Done | `supabase/migrations/20260527000001_create_story_drafts.sql` header comment |
| Docs | Done | `docs/requirements/15-story-authorization.md` — `DEPRECATED (2026-06)` banner |

**Rationale:** AC #2 allows historical migration file; new identity deployments use bootstrap without `story_drafts`.
