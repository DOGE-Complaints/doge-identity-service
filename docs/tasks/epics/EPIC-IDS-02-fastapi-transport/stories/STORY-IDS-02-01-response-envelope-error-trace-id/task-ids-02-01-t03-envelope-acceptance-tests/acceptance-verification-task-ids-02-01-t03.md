# Acceptance verification — task-ids-02-01-t03-envelope-acceptance-tests

- **Gate:** PASS
- **Wave:** `pkg-000003`
- **Verified:** 2026-05-29

## Evidence

- `tests/test_api_envelope.py` — 8 тестов: success envelope, error + trace_id, UUID из `ensure_trace_id(None)`, idempotency resolver (3 варианта).
- `cd doge-identity-service && .venv/bin/python -m pytest tests/ -q -m "not live_integration"` → **22 passed** (полный suite без live).

## AC mapping

| AC | Result |
|----|--------|
| Тесты `build_success_envelope` | PASS |
| Тесты `build_error_envelope` + `trace_id` | PASS |
| UUID формат `ensure_trace_id(None)` | PASS |
| Тесты `resolve_idempotency_key` | PASS |
