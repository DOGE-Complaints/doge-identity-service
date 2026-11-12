# Acceptance verification — task-ids-16-01-t02-env-example-runbook

- **Gate:** PASS
- **Wave:** pkg-000053
- **Story:** STORY-IDS-REQ9-01-make-env-required
- **Date:** 2026-09-26T12:08:20Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| `SERVICE_API_TOKEN` unchanged in `.env.example` | PASS | [`.env.example:137`](../../../../../../../.env.example) `SERVICE_API_TOKEN=`; no Makefile rename |
| `API_BASE_URL` / `PORT` names stay + documented | PASS | [`.env.example:8-12`](../../../../../../../.env.example) stable-names comment + `PORT`/`API_BASE_URL`; [`Makefile:3`](../../../../../../../Makefile) comment |
| Runbook Make section required `./.env` | PASS | [`run-and-healthcheck.md:37`](../../../../../../runbook/run-and-healthcheck.md), table `:45-46`; no «подхватывает» for Make start |
