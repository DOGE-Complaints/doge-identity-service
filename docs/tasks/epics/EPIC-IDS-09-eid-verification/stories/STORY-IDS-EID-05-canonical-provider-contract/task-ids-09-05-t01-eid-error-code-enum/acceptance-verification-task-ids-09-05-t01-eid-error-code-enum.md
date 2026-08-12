# Acceptance verification — task-ids-09-05-t01-eid-error-code-enum

- **Gate:** PASS (2026-06-09)
- **Wave:** pkg-000018

| Criterion | Result |
|-----------|--------|
| `EidErrorCode` StrEnum (9 values verbatim) | PASS — `src/core/providers/base.py` |
| `EIDProviderError(code: EidErrorCode)` default `UNKNOWN` | PASS — `base.py` |
| Export from `core.providers` | PASS — `__init__.py` |
| Offline regression | PASS — `pytest -m "not live_integration" -q` |
