from __future__ import annotations

import uuid

from core.api.envelope import (
    build_error_envelope,
    build_success_envelope,
    ensure_trace_id,
)


def test_build_success_envelope_shape() -> None:
    assert build_success_envelope({"status": "ok"}) == {"data": {"status": "ok"}}


def test_build_error_envelope_includes_trace_id() -> None:
    payload = build_error_envelope(
        "NOT_FOUND",
        "missing",
        trace_id="abc",
        status_code=404,
    )
    assert payload["error"]["trace_id"] == "abc"
    assert payload == {
        "error": {"code": "NOT_FOUND", "message": "missing", "trace_id": "abc"},
    }


def test_build_error_envelope_without_trace_id() -> None:
    assert build_error_envelope("BAD_REQUEST", "invalid") == {
        "error": {"code": "BAD_REQUEST", "message": "invalid"},
    }


def test_ensure_trace_id_generates_uuid4_when_missing() -> None:
    generated = ensure_trace_id(None)
    uuid.UUID(generated)


def test_ensure_trace_id_preserves_incoming() -> None:
    assert ensure_trace_id("  my-trace  ") == "my-trace"
