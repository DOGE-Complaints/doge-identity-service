# Acceptance verification — task-ids-08-01-t07-story-acceptance-verification

- **Gate:** PASS (2026-06-05)
- **Wave:** pkg-000011
- **Story:** STORY-IDS-CLEANUP-01-remove-stories-from-identity

| AC (story) | Result | Evidence |
|------------|--------|----------|
| `/ready` schema on bootstrap DB without `story_drafts` → 200 `schema:true` | PASS | `_REQUIRED_TABLES` = `profiles`, `eid_verification_sessions`, `eid_audit_events` (`db_supabase.py:315-318`); `test_required_tables_ready_iterates_identity_tables` |
| No `story_drafts`/`StoryDraft`/story-routes in code (grep=0, migration exempt) | PASS | `rg "story_drafts\|StoryDraft\|story-drafts\|submit-story" src tests --glob '!*migrations*'` → 0; migration file retained with DEPRECATED header |
| Story tests removed/rewritten; offline green | PASS | `pytest -m "not live_integration" -q` → **199 passed** |
| req-15 deprecated | PASS | `docs/requirements/15-story-authorization.md` — `DEPRECATED (2026-06)` |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
# 199 passed, 10 deselected, 1 warning

rg "story_drafts|StoryDraft|story-drafts|submit-story" src tests --glob '!*migrations*'
# (no matches)

head -3 supabase/migrations/20260527000001_create_story_drafts.sql
# DEPRECATED — identity scope removed 2026-06

head -3 docs/requirements/15-story-authorization.md
# DEPRECATED (2026-06)
```
