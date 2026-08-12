# Acceptance verification — task-ids-13-02-t05-audit-f2-email-verified-oauth-semantics-docs

- **Gate:** PASS
- **Wave:** override `epic_ids_13_onb_01_audit_2026_07_24`
- **Story:** STORY-IDS-ONB-01-email-in-me-and-supabase-confirm (audit F2)
- **Date:** 2026-07-24T20:44:05Z
- **Package:** pkg-000045 unchanged (immutable default)

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| openapi `MeData.email` / `email_verified` — OAuth/`email=null` caveat | PASS | [`openapi.yaml:73-86`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) |
| API_REFERENCE §6 Email fields — same caveat | PASS | [`API_REFERENCE.md:84`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) |
| rg OAuth / `email_verified` / `null` hits both docs | PASS | live rg 2026-07-24T20:44:05Z (`email=null`, `email != null`, OAuth/GPT) |
| No me_response / security / tests / migrations change in this wave | PASS | docs-only; runtime untouched this P6 |

## Commands (live verification 2026-07-24)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
cd doge-identity-service
rg -n 'email_verified|OAuth|email=null|email != null' \
  docs/runtime-docs/api-reference/openapi.yaml \
  docs/runtime-docs/api-reference/API_REFERENCE.md
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
