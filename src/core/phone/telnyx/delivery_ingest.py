from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from datetime import datetime, timezone

from core.domain.contracts import PhoneVerificationSessionStore
from core.domain.models import PhoneVerificationSession

CANONICAL_DELIVERY_STATUSES = frozenset(
    {"queued", "sent", "delivered", "failed", "gw_timeout", "dlr_timeout"}
)
FINAL_DELIVERY_STATUSES = frozenset({"delivered", "failed", "gw_timeout", "dlr_timeout"})

_STATUS_RANK: dict[str | None, int] = {
    None: -1,
    "queued": 0,
    "sent": 1,
    "delivered": 2,
    "failed": 3,
    "gw_timeout": 3,
    "dlr_timeout": 3,
}


@dataclass(frozen=True)
class TelnyxDeliveryEvent:
    event_type: str
    provider_message_id: str
    delivery_status: str
    occurred_at: datetime


@dataclass(frozen=True)
class DeliveryUpdateResult:
    outcome: str
    session: PhoneVerificationSession | None = None


def parse_telnyx_messaging_webhook(payload: dict) -> TelnyxDeliveryEvent:
    data = payload.get("data")
    if not isinstance(data, dict):
        raise ValueError("missing data")

    event_type = data.get("event_type")
    if not isinstance(event_type, str) or not event_type:
        raise ValueError("missing event_type")

    inner = data.get("payload")
    if not isinstance(inner, dict):
        raise ValueError("missing payload")

    message_id = inner.get("id")
    if not isinstance(message_id, str) or not message_id:
        raise ValueError("missing message id")

    occurred_raw = data.get("occurred_at") or inner.get("received_at")
    occurred_at = _parse_occurred_at(occurred_raw)
    delivery_status = _map_event_to_delivery_status(event_type, inner)
    if delivery_status not in CANONICAL_DELIVERY_STATUSES:
        raise ValueError(f"unsupported delivery status: {delivery_status}")

    return TelnyxDeliveryEvent(
        event_type=event_type,
        provider_message_id=message_id,
        delivery_status=delivery_status,
        occurred_at=occurred_at,
    )


def apply_delivery_update(
    store: PhoneVerificationSessionStore,
    *,
    provider_message_id: str,
    new_status: str,
    occurred_at: datetime,
) -> DeliveryUpdateResult:
    session = store.get_by_provider_message_id(provider_message_id)
    if session is None:
        return DeliveryUpdateResult(outcome="not_found")

    current_status = session.delivery_status
    if current_status == new_status:
        return DeliveryUpdateResult(outcome="noop", session=session)

    if current_status in FINAL_DELIVERY_STATUSES:
        return DeliveryUpdateResult(outcome="noop", session=session)

    current_rank = _STATUS_RANK.get(current_status, -1)
    new_rank = _STATUS_RANK.get(new_status, -1)
    if new_rank < current_rank:
        return DeliveryUpdateResult(outcome="noop", session=session)

    updated = dataclasses.replace(
        session,
        delivery_status=new_status,
        delivery_updated_at=occurred_at,
    )
    store.replace(updated)
    return DeliveryUpdateResult(outcome="updated", session=updated)


def _parse_occurred_at(value: object) -> datetime:
    if isinstance(value, str) and value:
        normalized = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(normalized)
        except ValueError:
            pass
    return datetime.now(timezone.utc)


def _map_event_to_delivery_status(event_type: str, payload: dict) -> str:
    if event_type == "message.sent":
        return _status_from_to(payload) or "sent"
    if event_type == "message.delivered":
        return "delivered"
    if event_type == "message.finalized":
        return _status_from_finalized(payload)
    raise ValueError(f"unsupported event_type: {event_type}")


def _status_from_to(payload: dict) -> str | None:
    to_list = payload.get("to")
    if not isinstance(to_list, list) or not to_list:
        return None
    first = to_list[0]
    if not isinstance(first, dict):
        return None
    status = first.get("status")
    if not isinstance(status, str) or not status:
        return None
    return _normalize_telnyx_status(status)


def _status_from_finalized(payload: dict) -> str:
    status = _status_from_to(payload)
    if status is not None:
        return status
    errors = payload.get("errors")
    if isinstance(errors, list) and errors:
        return "failed"
    return "failed"


def _normalize_telnyx_status(raw: str) -> str:
    normalized = raw.strip().lower()
    mapping = {
        "queued": "queued",
        "sending": "sent",
        "sent": "sent",
        "delivered": "delivered",
        "delivery_failed": "failed",
        "failed": "failed",
        "sending_failed": "failed",
        "gw_timeout": "gw_timeout",
        "dlr_timeout": "dlr_timeout",
    }
    return mapping.get(normalized, "failed")
