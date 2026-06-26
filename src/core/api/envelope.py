from __future__ import annotations

import uuid


def build_success_envelope(data: dict) -> dict:
    return {"data": data}


def build_error_envelope(
    code: str,
    message: str,
    trace_id: str | None = None,
    status_code: int = 400,
) -> dict:
    del status_code  # reserved for HTTP handlers; envelope shape is status-agnostic
    err: dict = {"code": code, "message": message}
    if trace_id:
        err["trace_id"] = trace_id
    return {"error": err}


def build_rate_limit_envelope(
    retry_after_s: int,
    *,
    trace_id: str | None = None,
) -> dict:
    err: dict = {
        "code": "rate_limit_exceeded",
        "message": "Rate limit exceeded.",
        "retry_after": retry_after_s,
    }
    if trace_id:
        err["trace_id"] = trace_id
    return {"error": err}


def ensure_trace_id(incoming: str | None) -> str:
    if incoming and incoming.strip():
        return incoming.strip()
    return str(uuid.uuid4())
