# Acceptance verification — task-ids-12-06-t10-audit-f2-live-integration-jwks-only-cleanup

- **Gate:** PASS
- **Date:** 2026-07-04T11:23:18Z
- **Wave:** override epic_ids_12_sec_06_audit_2026_07_04
- **Finding:** F2 (live integration JWT secret rudiment + stale validator API)

| AC (task) | Result | Evidence |
|-----------|--------|----------|
| Live conftest without JWT secret gate | PASS | `_require_supabase_jwt_validation_url_from_dotenv` |
| Live sanity JWKS-only validator | PASS | `test_supabase_jwt_live_sanity.py` + `JwksCache` |
| Runbook/env/doc-test synced | PASS | `.env.example`, `supabase-project-setup.md`, `test_supabase_runbook_docs.py` |
| CI workflow without SUPABASE_JWT_SECRET | PASS | `integration-live.yml` |
| Offline pytest green | PASS | 398 passed, 12 deselected |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -q -m "not live_integration"
```
