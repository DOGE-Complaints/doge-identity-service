# Acceptance verification — task-ids-02-01-t02-idempotency-key-resolver

- **Gate:** PASS
- **Wave:** `pkg-000003`
- **Verified:** 2026-05-29

## Evidence

- `src/core/api/idempotency.py` — `resolve_idempotency_key` с case-insensitive поиском заголовка.
- `tests/test_api_envelope.py::test_resolve_idempotency_key_*` — lowercase, mixed case, missing.
- `cd doge-identity-service && .venv/bin/python -m pytest tests/test_api_envelope.py -q` → **8 passed**.

## AC mapping

| AC | Result |
|----|--------|
| `resolve_idempotency_key({"idempotency-key":"K"}) == "K"` | PASS |
| Поиск ключа нечувствителен к регистру | PASS |
