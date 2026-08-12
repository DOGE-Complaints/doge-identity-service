# Acceptance verification — task-ids-08-02-t07-story-acceptance-verification

- **Story:** STORY-IDS-CLEANUP-02-placeholders-hardening
- **Wave:** pkg-000013 · **Date:** 2026-06-02

## Story AC

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | Owner decisions + execution | PASS | `owner-decisions-e17-e22.md`; t02–t06 artifacts |
| 2 | ALLOWED_RETURN_URLS validation + foreign domain test | PASS | `src/core/security/return_url.py`; `tests/test_return_url_validation.py` |
| 3 | Removed placeholders grep = 0 | PASS | StubBearerTokenAuth, resolve_idempotency_key, code_verifier_encryption, core.audit/oauth/profiles — 0 in src/tests |
| 4 | Offline green | PASS | `pytest -m "not live_integration" -q` → **204 passed** |

## Verification command

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```
