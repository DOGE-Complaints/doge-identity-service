# Acceptance verification — task-ids-08-02-t04-code-verifier-encryption-key-e20

- **Decision:** E20 **убрать**

## Evidence

- `src/core/config/schema.py` — field + pilot gate + env load removed
- Grep `code_verifier_encryption` in `src/` → 0

## AC/DoD

| Criterion | Result |
|-----------|--------|
| Story AC #1 E20 executed | PASS |
| Story AC #3 grep = 0 in src | PASS |
| Offline pytest | PASS |
