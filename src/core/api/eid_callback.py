"""eID callback domain outcome (transport-agnostic)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from core.api.envelope import build_error_envelope, build_success_envelope
from core.providers.base import EidErrorCode

EidCallbackOutcomeKind = Literal["verified", "already_verified", "failed"]


@dataclass(frozen=True)
class EidCallbackOutcome:
    outcome: EidCallbackOutcomeKind
    return_url: str | None
    error_code: EidErrorCode | None
    json_status: int
    envelope_code: str = "ok"
    envelope_message: str = ""
    envelope_data: dict[str, object] | None = None


def build_callback_json_envelope(
    outcome: EidCallbackOutcome,
    *,
    trace_id: str,
) -> tuple[dict, int]:
    if outcome.outcome == "verified":
        payload: dict[str, object] = {"status": "verified"}
        if outcome.return_url:
            payload["return_url"] = outcome.return_url
        return build_success_envelope(payload), outcome.json_status

    if outcome.outcome == "already_verified":
        return (
            build_success_envelope({"status": "already_consumed"}),
            outcome.json_status,
        )

    body = build_error_envelope(
        outcome.envelope_code,
        outcome.envelope_message,
        trace_id=trace_id,
    )
    if outcome.error_code is not None:
        body["error"]["eid_error_code"] = outcome.error_code.value
    return body, outcome.json_status


def append_eid_redirect_query(outcome: EidCallbackOutcome, return_url: str) -> str:
    if outcome.outcome in {"verified", "already_verified"}:
        marker = "eid_status=verified"
    else:
        marker = "eid_status=error"
        if outcome.error_code is not None:
            marker = f"{marker}&eid_error={outcome.error_code.value}"
    separator = "&" if "?" in return_url else "?"
    return f"{return_url}{separator}{marker}"


def has_safe_redirect_target(outcome: EidCallbackOutcome) -> bool:
    return bool(outcome.return_url and outcome.return_url.strip())
