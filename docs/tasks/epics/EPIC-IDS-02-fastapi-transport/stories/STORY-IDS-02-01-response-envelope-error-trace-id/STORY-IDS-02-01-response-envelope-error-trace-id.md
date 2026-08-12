# STORY-IDS-02-01: Response envelope, error types и trace-id

## Meta
- Key: `STORY-IDS-02-01-response-envelope-error-trace-id`
- Parent Epic: [`../../../EPIC-IDS-02-fastapi-transport.md`](../../../EPIC-IDS-02-fastapi-transport.md)
- Type: Technical Story (HTTP Transport)
- Status: Done
- Decision Ref: [`../../../../requirements/16-security-privacy-observability.md`](../../../../requirements/16-security-privacy-observability.md)

## Story Goal
Зафиксировать единый response envelope и trace-id propagation для success/error ответов, плюс resolver для `Idempotency-Key`.

## AC / DoD (из EPIC-IDS-02)
- [x] `build_success_envelope({"status": "ok"}) == {"data": {"status": "ok"}}`
- [x] `build_error_envelope(..., trace_id="abc", status_code=404)["error"]["trace_id"] == "abc"`
- [x] `ensure_trace_id(None)` возвращает валидный UUID4
- [x] `resolve_idempotency_key({"idempotency-key": "K"}) == "K"` (case-insensitive)

## Story gate
- [story-acceptance-gate-STORY-IDS-02-01.md](./story-acceptance-gate-STORY-IDS-02-01.md) — **PASS** (2026-05-29)

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-02-01-t01-envelope-core`](./task-ids-02-01-t01-envelope-core/README.md) | pkg-000003 |
| 2 | [`task-ids-02-01-t02-idempotency-key-resolver`](./task-ids-02-01-t02-idempotency-key-resolver/README.md) | pkg-000003 |
| 3 | [`task-ids-02-01-t03-envelope-acceptance-tests`](./task-ids-02-01-t03-envelope-acceptance-tests/README.md) | pkg-000003 |
