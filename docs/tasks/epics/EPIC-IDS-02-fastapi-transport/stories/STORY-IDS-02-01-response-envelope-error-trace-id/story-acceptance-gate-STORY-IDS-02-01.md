# Story acceptance gate — STORY-IDS-02-01

- Story: `STORY-IDS-02-01-response-envelope-error-trace-id`
- Gate status: **PASS** (implementation + automated checks; коммиты — по политике оператора)
- Scope: tasks t01–t03, `pkg-000003`

## Epic AC (EPIC-IDS-02 §Story 1)

| Criterion | Result | Evidence |
|-----------|--------|----------|
| `build_success_envelope({"status": "ok"})` | PASS | `tests/test_api_envelope.py::test_build_success_envelope_shape` |
| `build_error_envelope(..., trace_id="abc")` | PASS | `tests/test_api_envelope.py::test_build_error_envelope_includes_trace_id` |
| `ensure_trace_id(None)` → UUID4 | PASS | `tests/test_api_envelope.py::test_ensure_trace_id_generates_uuid4_when_missing` |
| `resolve_idempotency_key` case-insensitive | PASS | `tests/test_api_envelope.py::test_resolve_idempotency_key_*` |

## Task reports

- [t01 acceptance](./task-ids-02-01-t01-envelope-core/acceptance-verification-task-ids-02-01-t01.md)
- [t02 acceptance](./task-ids-02-01-t02-idempotency-key-resolver/acceptance-verification-task-ids-02-01-t02.md)
- [t03 acceptance](./task-ids-02-01-t03-envelope-acceptance-tests/acceptance-verification-task-ids-02-01-t03.md)

## Verify

`python3 docs/methodology/builder-queue/builder_resolve_queue.py --project identity --verify` → `ok 14 paths`
