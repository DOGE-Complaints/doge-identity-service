# Acceptance verification — task-ids-04-02-t01-hash-secret-contract-verify

- **Gate:** PASS (2026-05-30)
- **Wave:** pkg-000005
- **Evidence:** [`src/core/security/hashing.py`](../../../../../../../src/core/security/hashing.py) — `hash_secret(plaintext, *, key)` → HMAC-SHA256 hex; `tests/test_security_hashing.py` — детерминизм
