# Acceptance verification — task-ids-08-02-t05-idempotency-resolver-e21

- **Decision:** E21 **убрать**

## Evidence

- `src/core/api/idempotency.py` — deleted
- Grep `resolve_idempotency_key` in `src/` + `tests/` → 0

## AC/DoD

| Criterion | Result |
|-----------|--------|
| Story AC #1 E21 executed | PASS |
| Story AC #3 grep = 0 | PASS |
