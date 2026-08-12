# Acceptance verification — task-ids-13-02-t02-confirm-email-runbook-and-me-api-docs

- **Gate:** PASS
- **Wave:** pkg-000045
- **Story:** STORY-IDS-ONB-01-email-in-me-and-supabase-confirm
- **Date:** 2026-07-24T18:57:53Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| `supabase-project-setup.md` — mandatory Confirm email + связь с `email_verified` | PASS | [`supabase-project-setup.md` §2a](../../../../../../../docs/runbook/supabase-project-setup.md) |
| `openapi.yaml` MeData: `email` nullable + `email_verified` bool (политика токен ⇒ true) | PASS | [`openapi.yaml:73-80`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) |
| `API_REFERENCE.md` §6 — те же поля | PASS | [`API_REFERENCE.md` §6](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) |
| `rg` Confirm email / `email_verified` — hits | PASS | live grep 2026-07-24T18:57:53Z |
