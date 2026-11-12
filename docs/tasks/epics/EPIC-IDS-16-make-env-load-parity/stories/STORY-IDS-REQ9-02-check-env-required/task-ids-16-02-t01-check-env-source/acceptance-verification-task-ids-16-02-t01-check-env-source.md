# Acceptance verification — task-ids-16-02-t01-check-env-source

- **Gate:** PASS
- **Wave:** pkg-000054
- **Story:** STORY-IDS-REQ9-02-check-env-required
- **Date:** 2026-09-26T12:21:29Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| `check-env` without `if [ -f ./.env ]` | PASS | [`Makefile:15-21`](../../../../../../../Makefile) — `set -a && . ./.env && set +a && \` |
| Pattern matches serve/dev | PASS | Same stanza as [`Makefile:4-11`](../../../../../../../Makefile) |
| Fail closed if `.env` absent | PASS | empty-dir `make check-env` → `/bin/sh: ./.env: No such file or directory` · Error 1 |
| Printed keys unchanged | PASS | APP_PROFILE/PORT/SUPABASE_*/AUTHENTIGATE_ISSUER/EID_PROVIDER |
| serve/dev/runbook untouched this task | PASS | only `check-env` + header comment |
| Comment not optional | PASS | `# Diagnostic print — same required shell-source… (REQ9-02); not optional.` |
