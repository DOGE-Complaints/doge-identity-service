from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone

from core.phone.telnyx.delivery_ingest import (
    CANONICAL_DELIVERY_STATUSES,
    apply_delivery_update,
)

_STATUS_MAP: dict[str, str] = {
    "queued": "queued",
    "submitted": "sent",
    "sent": "sent",
    "delivered": "delivered",
    "failed": "failed",
}


@dataclass(frozen=True)
class SmspmDeliveryEvent:
    provider_message_id: str
    delivery_status: str
    occurred_at: datetime


def parse_smspm_delivery_query(query: Mapping[str, str]) -> SmspmDeliveryEvent:
    """Parse SMSPM GET callback query. Do not store ``toNumber``."""
    message_id = (query.get("id") or "").strip()
    if not message_id:
        raise ValueError("missing message id")

    raw_status = (query.get("status") or "").strip().lower()
    if not raw_status:
        raise ValueError("missing status")

    mapped = _STATUS_MAP.get(raw_status)
    if mapped is None or mapped not in CANONICAL_DELIVERY_STATUSES:
        raise ValueError(f"unsupported delivery status: {raw_status}")

    return SmspmDeliveryEvent(
        provider_message_id=message_id,
        delivery_status=mapped,
        occurred_at=datetime.now(timezone.utc),
    )


__all__ = [
    "SmspmDeliveryEvent",
    "apply_delivery_update",
    "parse_smspm_delivery_query",
]
