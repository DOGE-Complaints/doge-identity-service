# Acceptance verification — task-ids-09-06-t04-offline-redirect-and-json-regression-tests

- **Gate:** PASS (2026-06-09)
- **Wave:** pkg-000019

| Criterion | Result |
|-----------|--------|
| Mock callback (browser) → 303 + `Location` with `return_url` and `eid_status=verified` | PASS — `test_eid_callback_redirect.py` |
| Provider error path → 303 + `eid_status=error` + `eid_error=<canonical>` | PASS — `test_eid_callback_redirect.py` |
| Unknown session / missing safe `return_url` → 400, no `Location` | PASS — `test_eid_callback_redirect.py` |
| `GET /auth/unknown-provider/callback` → `ConfigError` / 500 JSON | PASS — `test_eid_callback_redirect.py` |
| EID-01 mock flow via `Accept: application/json` → JSON 200 `status=verified` | PASS — `test_eid_verification_flow.py` |
| Story AC #5, #6 (offline part) traceability | PASS |
| Full offline suite green | PASS — 232 pytest |

```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_eid_callback_redirect.py tests/test_eid_verification_flow.py tests/test_canonical_provider_contract.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
# 232 passed
```
