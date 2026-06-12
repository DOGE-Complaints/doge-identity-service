from __future__ import annotations

from datetime import datetime, timedelta, timezone

from core.domain.models import PhoneVerificationSession
from core.infrastructure.repositories import InMemoryPhoneVerificationSessionStore
from core.security.hashing import hash_secret


def _session(
    *,
    session_id: str = "sess-1",
    user_id: str = "user-1",
    status: str = "started",
    attempts: int = 0,
    created_at: datetime | None = None,
    expires_at: datetime | None = None,
) -> PhoneVerificationSession:
    now = datetime(2026, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    created = created_at or now
    expires = expires_at or (created + timedelta(minutes=5))
    return PhoneVerificationSession(
        id=session_id,
        supabase_user_id=user_id,
        phone_hash=hash_secret("+37255555555", key="test-key"),
        dial_prefix="+372",
        code_hash="hash",
        status=status,
        attempts=attempts,
        created_at=created,
        expires_at=expires,
        provider="mock",
        provider_message_id=None,
        delivery_status=None,
        delivery_updated_at=None,
    )


def test_create_and_get_by_id() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    session = _session()
    store.create(session)
    assert store.get_by_id("sess-1") == session


def test_get_active_by_user_returns_latest_started() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    now = datetime(2026, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    older = _session(session_id="old", created_at=now - timedelta(minutes=2))
    newer = _session(session_id="new", created_at=now)
    store.create(older)
    store.create(newer)
    active = store.get_active_by_user("user-1", now=now)
    assert active is not None
    assert active.id == "new"


def test_mark_consumed_and_mark_failed() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    session = _session()
    store.create(session)
    store.mark_consumed("sess-1")
    assert store.get_by_id("sess-1") is not None
    assert store.get_by_id("sess-1").status == "consumed"
    store.create(_session(session_id="sess-2"))
    store.mark_failed("sess-2", "test")
    assert store.get_by_id("sess-2") is not None
    assert store.get_by_id("sess-2").status == "failed"


def test_expire_pending_marks_started_past_expiry() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    now = datetime(2026, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    expired = _session(
        session_id="expired",
        expires_at=now - timedelta(seconds=1),
    )
    store.create(expired)
    count = store.expire_pending(now)
    assert count == 1
    assert store.get_by_id("expired") is not None
    assert store.get_by_id("expired").status == "expired"


def test_replace_updates_attempts() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    session = _session(attempts=2)
    store.create(session)
    updated = _session(attempts=3)
    store.replace(updated)
    assert store.get_by_id("sess-1") is not None
    assert store.get_by_id("sess-1").attempts == 3


def test_get_by_provider_message_id() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    session = _session(session_id="sess-msg")
    with_message = PhoneVerificationSession(
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
        provider_message_id="msg-abc-123",
        delivery_status=None,
        delivery_updated_at=None,
    )
    store.create(with_message)
    assert store.get_by_provider_message_id("msg-abc-123") == with_message
    assert store.get_by_provider_message_id("missing") is None
