# Acceptance verification — task-ids-09-05-t04-offline-contract-tests

- **Gate:** PASS (2026-06-09)
- **Wave:** pkg-000018

| Criterion | Result |
|-----------|--------|
| `USER_CANCELLED` → audit `failure_reason` canonical | PASS — `test_callback_eid_provider_error_records_canonical_code_in_audit` |
| Unexpected `Exception` → `UNKNOWN` | PASS — `test_callback_unexpected_exception_records_unknown` |
| Cross-provider dedup unit test | PASS — `test_same_subject_hash_different_providers_same_verified_person_hash` |
| Offline suite green | PASS — 225 pytest |

```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_canonical_provider_contract.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
# 225 passed, 10 deselected
```
