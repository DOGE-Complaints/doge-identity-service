# Acceptance verification — task-ids-12-06-t09-audit-f1-jwks-httpx-client-lifespan-close

- **Gate:** PASS
- **Date:** 2026-07-04T11:22:42Z
- **Wave:** override epic_ids_12_sec_06_audit_2026_07_04
- **Finding:** F1 (JWKS httpx client not closed on shutdown)

| AC (task) | Result | Evidence |
|-----------|--------|----------|
| Client ref on shutdown | PASS | `ApiDependencies.jwks_http_client`; `DefaultServiceFactory.jwks_http_client` |
| `_lifespan` calls `close()` | PASS | `asgi_app.py` after `yield` |
| Offline pytest green | PASS | 398 passed, 12 deselected |
| No SEC-06 grep regression | PASS | `src/` grep secret empty |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -q -m "not live_integration"
```
