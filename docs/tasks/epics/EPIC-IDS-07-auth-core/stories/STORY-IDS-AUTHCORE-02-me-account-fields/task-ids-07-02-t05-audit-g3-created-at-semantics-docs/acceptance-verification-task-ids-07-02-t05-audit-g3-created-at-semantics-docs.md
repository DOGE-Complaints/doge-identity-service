# Acceptance verification — task-ids-07-02-t05-audit-g3-created-at-semantics-docs

- **Gate:** PASS
- **Wave:** override `epic_ids_07_authcore_02_audit_2026_07_24`
- **Story:** STORY-IDS-AUTHCORE-02-me-account-fields (audit G3)
- **Date:** 2026-07-24T14:05:39Z
- **Package:** pkg-000044 unchanged (immutable default)

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| openapi `MeData.created_at` — first verification, not Auth registration | PASS | [`openapi.yaml:84-90`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) |
| API_REFERENCE §6 D-CAB-2 caveat | PASS | [`API_REFERENCE.md:83`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) |
| rg semantics hits both docs | PASS | live rg: `first verification`, `registration`/`signup`, `первой верификации`, `регистрации` |
| No me_response / tests / migrations change | PASS | docs-only wave |

## Commands (live verification 2026-07-24)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
cd doge-identity-service
rg -n 'first verification|registration|signup|первой верификации|регистрации|Account Created' \
  docs/runtime-docs/api-reference/openapi.yaml \
  docs/runtime-docs/api-reference/API_REFERENCE.md
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
