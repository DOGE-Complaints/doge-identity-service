from __future__ import annotations

from datetime import datetime, timezone

from core.domain.models import PhoneVerificationSession
from core.infrastructure.repositories import InMemoryPhoneVerificationSessionStore
from core.phone.telnyx.delivery_ingest import apply_delivery_update, parse_telnyx_messaging_webhook
from core.security.hashing import hash_secret


def _session(*, message_id: str, delivery_status: str | None = None) -> PhoneVerificationSession:
    now = datetime(2026, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    return PhoneVerificationSession(
        id="sess-1",
        supabase_user_id="user-1",
        phone_hash=hash_secret("+37255555555", key="test-key"),
        dial_prefix="+372",
        code_hash="hash",
        status="started",
        attempts=0,
        created_at=now,
        expires_at=now,
        provider="telnyx",
        provider_message_id=message_id,
        delivery_status=delivery_status,
        delivery_updated_at=None,
    )


def _payload(*, event_type: str, message_id: str, to_status: str | None = None) -> dict:
    inner: dict = {"id": message_id}
    if to_status is not None:
        inner["to"] = [{"status": to_status}]
    return {
        "data": {
            "event_type": event_type,
            "occurred_at": "2026-06-11T12:01:00.000000Z",
            "payload": inner,
        }
    }


def test_parse_message_sent_maps_to_sent() -> None:
    event = parse_telnyx_messaging_webhook(_payload(event_type="message.sent", message_id="m1"))
    assert event.delivery_status == "sent"
    assert event.provider_message_id == "m1"


def test_parse_message_delivered_maps_to_delivered() -> None:
    event = parse_telnyx_messaging_webhook(_payload(event_type="message.delivered", message_id="m2"))
    assert event.delivery_status == "delivered"


def test_parse_message_finalized_failed_maps_to_failed() -> None:
    payload = {
        "data": {
            "event_type": "message.finalized",
            "occurred_at": "2026-06-11T12:02:00.000000Z",
            "payload": {
                "id": "m3",
                "errors": [{"code": "40008", "title": "Undeliverable"}],
            },
        }
    }
    event = parse_telnyx_messaging_webhook(payload)
    assert event.delivery_status == "failed"


def test_apply_delivery_update_updates_session() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    session = _session(message_id="m4")
    store.create(session)
    occurred = datetime(2026, 6, 11, 12, 3, 0, tzinfo=timezone.utc)

    result = apply_delivery_update(
        store,
        provider_message_id="m4",
        new_status="sent",
        occurred_at=occurred,
    )

    assert result.outcome == "updated"
    updated = store.get_by_id("sess-1")
    assert updated is not None
    assert updated.delivery_status == "sent"
    assert updated.delivery_updated_at == occurred


def test_apply_delivery_update_idempotent_replay() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    occurred = datetime(2026, 6, 11, 12, 4, 0, tzinfo=timezone.utc)
    session = _session(message_id="m5", delivery_status="delivered")
    session = PhoneVerificationSession(
        id=session.id,
        supabase_user_id=session.supabase_user_id,
        phone_hash=session.phone_hash,
        dial_prefix=session.dial_prefix,
        code_hash=session.code_hash,
        status=session.status,
        attempts=session.attempts,
        created_at=session.created_at,
        expires_at=session.expires_at,
        provider=session.provider,
        provider_message_id=session.provider_message_id,
        delivery_status="delivered",
        delivery_updated_at=occurred,
    )
    store.create(session)

    result = apply_delivery_update(
        store,
        provider_message_id="m5",
        new_status="sent",
        occurred_at=occurred,
    )

    assert result.outcome == "noop"
    assert store.get_by_id("sess-1").delivery_status == "delivered"


def test_apply_delivery_update_unknown_message_id_is_noop() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    result = apply_delivery_update(
        store,
        provider_message_id="missing",
        new_status="sent",
        occurred_at=datetime.now(timezone.utc),
    )
    assert result.outcome == "not_found"
