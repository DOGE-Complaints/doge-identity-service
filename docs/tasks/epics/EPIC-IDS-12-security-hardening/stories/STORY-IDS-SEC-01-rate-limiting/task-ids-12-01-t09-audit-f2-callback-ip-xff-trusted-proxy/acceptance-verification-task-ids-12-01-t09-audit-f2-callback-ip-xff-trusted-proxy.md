# Acceptance verification — task-ids-12-01-t09-audit-f2-callback-ip-xff-trusted-proxy

- **Gate:** PASS
- **Date:** 2026-06-26
- **Wave:** override epic_ids_12_sec_01_audit_2026_06_26
- **Finding:** F2 (XFF spoof bypass)

| AC (task) | Result | Evidence |
|-----------|--------|----------|
| Trusted proxy via config | PASS | `schema.py` `RATE_LIMIT_TRUSTED_PROXY_COUNT`; `_client_ip` in `rate_limit_dependency.py` |
| Default ignores XFF | PASS | `TRUSTED_PROXY_COUNT=0` → `request.client.host` |
| Spoof XFF no bypass | PASS | `test_callback_rate_limit_ignores_spoofed_x_forwarded_for` |
| 04-security §8 note | PASS | `04-security.md` §8 deployment contract |
| Regression tests green | PASS | `tests/test_rate_limiting.py` |

```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_rate_limiting.py -m "not live_integration" -q
```
