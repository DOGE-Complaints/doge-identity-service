# Acceptance verification — task-ids-07-02-t02-me-api-docs-created-at-account-status

- **Gate:** PASS
- **Wave:** pkg-000044
- **Story:** STORY-IDS-AUTHCORE-02-me-account-fields

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| openapi `MeData` created_at + account_status | PASS | [`openapi.yaml:84-91`](../../../../../../../docs/runtime-docs/api-reference/openapi.yaml) |
| API_REFERENCE §6 example + MVP note | PASS | [`API_REFERENCE.md:79-98`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) |
| rg hits both docs | PASS | live rg `account_status\|created_at` |
