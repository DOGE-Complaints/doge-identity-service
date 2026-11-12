# Backlog status audit — doge-identity-service (code-verified)

**Date:** 2026-07-09 · **Method:** `.cursor/rules/analysis.mdc` — claims cite file paths only.

## Phase 0 — Mirror (verified-state)

| Metric | Value | Evidence |
|--------|-------|----------|
| Packages | 11 | `docs/tasks/backlog-stories/*/` |
| `STORY-IDS-*.md` | 44 | `find docs/tasks/backlog-stories -name 'STORY-IDS-*.md'` |
| `DOC-IDS-*.md` | 5 | `identity-onboarding/` |
| `SPIKE-IDS-*.md` | 2 | `phone-verification/`, `eid-deferred/` |
| Orphan root stories | 0 | root: `INDEX.md`, `GAP-CLOSURE-INDEX.md` only |
| Package `INDEX.md` (before HK) | 2 | root + `story-draft-handoff/` |
| Dashboard | missing | no `identity-backlog-dashboard.md` |

### Index gaps (before → after HK)

| Package | Before | After HK |
|---------|--------|----------|
| auth-core … security-hardening | `EPIC-IDS-*.md` only | + `INDEX.md` |
| eid-deferred | `README.md` | + `INDEX.md` |
| railway-deploy | none | + `INDEX.md` |
| auth-bff | `EPIC-IDS-AUTHBFF.md` | + `INDEX.md` |
| story-draft-handoff | `INDEX.md` | aligned Status column |
| root INDEX | stale 2026-06-26 | 2026-07-09, +railway-deploy, +auth-bff |

## Epic rollup

| Epic | Old (bullrun) | Evidence | New |
|------|---------------|----------|-----|
| EPIC-IDS-07 | In Progress | AUTHCORE-01 pkg-000009 Done | **Done** (epic gate pending — audit gaps closed) |
| EPIC-IDS-08 | In Progress | CLEANUP-01/02/03 Done | **In Progress** (CLEANUP-04 open) |
| EPIC-IDS-09 | In Progress | EID-01/03…08 Done | **Done** (platform; real eID deferred) |
| EPIC-IDS-10 | In Progress | PV-01…10 Done per pkg-000022…041 | **Done** (SPIKE-08 external) |
| EPIC-IDS-11 | In Progress | OAUTH-01…04 pkg-000029…034 | **Done** |
| EPIC-IDS-12 | In Progress | SEC-01…06 Done | **In Progress** (SEC-04 open; SEC-05 ADR only) |
| EPIC-IDS-13 | In Progress | DOC-ONB-01 Done; ONB-01 open | **In Progress** |
| DEPLOY (backlog-only) | not in registry | partial deploy evidence | **In Progress** (backlog-only) |

## Open stories — verified

| Story | Old | Code evidence | New |
|-------|-----|---------------|-----|
| DEPLOY-01 | Todo | [`railpack.json:7`](../../railpack.json) startCommand; [`requirements.txt`](../../requirements.txt); [`railway.json`](../../railway.json) health only; grep `DEV_OTP_ECHO` in `src/` — **0**; run-report [`run-summary-20260707-identity-railway-502-fix.md`](../tasks/run-reports/run-summary-20260707-identity-railway-502-fix.md) | **Todo** (partial: T01/T02 partial; T04/T06 open) |
| ONB-01 | Todo | [`me_response.py:19-46`](../../src/core/api/me_response.py) — no `email` field | **Todo** |
| CLEANUP-04 | Todo | [`06-technical-scaffold.md:3`](../../docs/requirements/06-technical-scaffold.md) reference-only banner | **Todo** |
| SEC-04 | Todo | no rotation runbook in `docs/runbook/` for service_role isolation | **Todo** |
| SEC-05 | «Решено» | ADR variant B in story; [`auth-bff/`](../../docs/tasks/backlog-stories/auth-bff/) POST-MVP | **Accumulating** (ADR Done; BFF implementation deferred) |
| DOC-ONB-02…04 | Todo | doc-only; spa/product scope | **Todo** |
| PV-02,04,05,07 | Todo (stale frontmatter) | [`asgi_app.py:359-395`](../../src/core/api/asgi_app.py); [`test_phone_verification_flow.py`](../../tests/test_phone_verification_flow.py); [`test_telnyx_sms_sender.py`](../../tests/test_telnyx_sms_sender.py); bullrun pkg-000023…028 | **Done** (sync frontmatter) |
| OAUTH-04 | Todo (stale) | [`test_oauth_verify_gate.py`](../../tests/test_oauth_verify_gate.py); pkg-000034 | **Done** (sync frontmatter) |
| DOC-ONB-05 | Todo | [`01-api.md:29-35`](../../docs/runtime-docs/01-api.md) phone+OAuth+Telnyx routes | **Done** (sync frontmatter) |

## Done stories — spot-check

| Story | Evidence |
|-------|----------|
| AUTHCORE-01 | [`test_me_profile.py`](../../tests/test_me_profile.py); pkg-000009 |
| PV-01 | [`src/core/phone/`](../../src/core/phone/); pkg-000022 |
| SEC-06 | [`supabase_validator.py`](../../src/core/auth/supabase_validator.py) JWKS; no `SUPABASE_JWT_SECRET` in src; pkg-000042 |
| OAUTH-01 | [`test_oauth_server_flow.py`](../../tests/test_oauth_server_flow.py); pkg-000029 |
| CLEANUP-01 | pkg-000011 + audit pkg-000012 |
| PV-09 | [`db_supabase.py`](../../src/core/infrastructure/db_supabase.py) `SupabasePhone*`; pkg-000039 |
| PV-10 | [`test_phone_file_sms_sender.py`](../../tests/test_phone_file_sms_sender.py); pkg-000041 |

## Status changes applied

- Story frontmatter: PV-02, PV-04, PV-05, PV-07, OAUTH-04 → Done; DOC-ONB-05 → Done; SEC-05 → Accumulating (INDEX)
- [`EPIC-IDS-SEC.md`](../tasks/backlog-stories/security-hardening/EPIC-IDS-SEC.md): SEC-06 row → Done
- Package + root `INDEX.md` created/updated
- Bullrun §«Актуальная точка»: next wave + stale active pkg line fixed (cite pkg-000042 from yaml, yaml untouched)

## Conflicts resolved

| Conflict | Resolution |
|----------|------------|
| EPIC-IDS-SEC SEC-06 Todo vs story Done | EPIC synced to Done (pkg-000042 evidence) |
| PV/OAUTH story Todo vs EPIC/bullrun Done | Story frontmatter synced to Done |
| bullrun L83 pkg-000041 vs `identity-active-package.current.yaml` pkg-000042 | Bullrun line updated to cite current yaml |
| DEPLOY-01 not in registry | Added backlog-only row in Epic registry |
| auth-bff/railway-deploy missing from root INDEX | Added to root INDEX |

**Conflict-scan result:** 0 unresolved after HK.

## HK retirement (2026-07-09)

| Item | Action | Evidence |
|------|--------|----------|
| DEPLOY-01 / `railway-deploy/` package | **Retired** — removed from active backlog | Operator-validated Railway deploy; as-built SSOT: [`run-and-healthcheck.md`](../runbook/run-and-healthcheck.md); `DEV_OTP_ECHO` dropped |
| Dashboard denominator | 34→33 stories, Todo 3→2, progress 88%→91% | [`identity-backlog-dashboard.md`](../tasks/identity-backlog-dashboard.md) |
| Bullrun next | ONB-01 only | [`bullrun-launch-index.md`](../tasks/bullrun-launch-index.md) |
