# BULLRUN-PHASE-LOG

- **Wave:** pkg-000012
- **Process:** P3 Execute STORY-IDS-CLEANUP-01 t08 (audit F1)
- **Date:** 2026-06-05

| Phase | Status | Evidence |
|-------|--------|----------|
| Implement | Done | Runbook §3 — operational migrations 1–4 only; story_drafts → Historical blockquote |
| Verify | Done | `test_runbook_marks_story_drafts_migration_historical` PASS |

**Decision:** align runbook with migration DEPRECATED header + bootstrap (no story_drafts on new deployments).
