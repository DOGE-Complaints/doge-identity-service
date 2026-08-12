# Acceptance verification — task-ids-06-05-t02-story5-acceptance-verification

- **Gate:** PASS (2026-06-02)
- **Wave:** pkg-000008
- **Evidence:** smoke 5 passed @ `IDENTITY_URL=http://localhost:8100`; offline 193 passed; smoke excluded from default collection

| AC (epic L267–270) | Result |
|--------------------|--------|
| `IDENTITY_URL=… pytest tests/smoke/ -v` PASSED при `make serve` | PASS — 5 passed in 0.19s (uvicorn :8100) |
| Smoke НЕ в `pytest tests/ -q` | PASS — `tests/test_smoke_collection_contract.py`; `collect_ignore = ["smoke"]` |
| `IDENTITY_URL=https://identity.dogestonia.ee pytest tests/smoke/` | **Operator** — Railway deploy check (not run in CI sandbox) |
