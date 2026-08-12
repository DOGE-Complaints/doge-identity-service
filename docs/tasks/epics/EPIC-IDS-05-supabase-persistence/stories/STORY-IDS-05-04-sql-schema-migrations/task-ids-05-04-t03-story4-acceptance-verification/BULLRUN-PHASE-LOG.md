# BULLRUN-PHASE-LOG

- **Wave:** pkg-000006
- **Skill declared:** test-master
- **Process:** bullrun-start + run-task (P3 Execute, STORY-IDS-05-04 t03)
- **Date:** 2026-05-31

## Phases

| Phase | Status | Evidence |
|-------|--------|----------|
| Tests | Done | `tests/test_supabase_migrations_sql.py` — 9 static asserts |
| Acceptance | Done | `acceptance-verification-task-ids-05-04-t03-story4-acceptance-verification.md` |

## Verification command

```bash
cd doge-identity-service && .venv/bin/python -m pytest tests/test_supabase_migrations_sql.py -v
# 9 passed
```

## Manual live apply checklist (post-Story-4)

Apply in Supabase SQL Editor, in order:

1. `20260525000001_create_profiles.sql`
2. `20260525000002_create_eid_verification_sessions.sql`
3. `20260525000003_create_eid_audit_events.sql`
4. `20260526000001_eid_sessions_provider_abstraction.sql`
5. `20260527000001_create_story_drafts.sql`

Then verify on live project (Story 5 / EPIC-IDS-06):

- `required_tables_ready() == True`
- `required_columns_ready() == True`
- `provider_state_ready() == True`
- `service_role_policy_probe() == True`
