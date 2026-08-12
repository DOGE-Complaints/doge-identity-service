# Acceptance verification — task-ids-08-02-t02-allowed-return-urls-e17

- **Decision:** E17 **довести** ([`owner-decisions-e17-e22.md`](../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md))

## Evidence

- `src/core/security/return_url.py` — `parse_allowed_return_urls`, `validate_return_url`, `InvalidReturnUrlError`
- `tests/test_return_url_validation.py::test_validate_return_url_rejects_foreign_domain` — PASS

## AC/DoD

| Criterion | Result |
|-----------|--------|
| Story AC #1 E17 executed | PASS |
| Story AC #2 validation + foreign domain test | PASS |
| Offline pytest (targeted module) | PASS |
