# Acceptance verification — task-ids-09-05-t03-canonical-subject-hash-contract

- **Gate:** PASS (2026-06-09)
- **Wave:** pkg-000018

| Criterion | Result |
|-----------|--------|
| `EIDVerificationResult` contract doc (provider-agnostic `subject_hash`) | PASS — `base.py` dataclass docstring |
| `06-eid-providers.md` identity rule + formula | PASS — F12 + `EidErrorCode` sections |
| Mock without `mock-` prefix | PASS — `mock_provider.py` |
| `handlers.py` formula unchanged | PASS — `country:subject_hash` only |
