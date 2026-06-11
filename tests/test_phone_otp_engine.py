from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from core.config.providers import provide_app_config
from core.infrastructure.repositories import InMemoryPhoneVerificationSessionStore
from core.phone.base import SmsErrorCode, SmsSenderError
from core.phone.otp_engine import create_phone_verification_session, verify_phone_code
from core.security.hashing import hash_secret


def _config():
    return provide_app_config(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "http://localhost:8100",
            "DB_BACKEND": "in_memory",
            "EID_PROVIDER": "mock",
            "SMS_PROVIDER": "mock",
            "DOGESTONIA_EID_SECRET": "otp-test-secret",
        }
    )


def test_create_returns_plaintext_code_and_stores_hash_only() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    config = _config()
    now = datetime(2026, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    session, code = create_phone_verification_session(
        store=store,
        config=config,
        supabase_user_id="user-1",
        e164="+37255555555",
        dial_prefix="+372",
        provider="mock",
        now=now,
    )
    assert len(code) == config.phone_code_length
    assert code.isdigit()
    assert session.code_hash == hash_secret(code, key=config.eid_secret)
    assert session.code_hash != code
    assert session.status == "started"
    assert session.attempts == 0


def test_verify_success_returns_subject_hash_without_provider_prefix() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    config = _config()
    now = datetime(2026, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    e164 = "+37255555555"
    session, code = create_phone_verification_session(
        store=store,
        config=config,
        supabase_user_id="user-1",
        e164=e164,
        dial_prefix="+372",
        provider="mock",
        now=now,
    )
    result = verify_phone_code(
        store=store,
        config=config,
        session_id=session.id,
        submitted_code=code,
        e164=e164,
        now=now,
    )
    assert result.subject_hash == hash_secret(e164, key=config.eid_secret)
    assert ":" not in result.subject_hash
    assert store.get_by_id(session.id) is not None
    assert store.get_by_id(session.id).status == "consumed"


def test_verify_mismatch_increments_attempts() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    config = _config()
    now = datetime(2026, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    session, _code = create_phone_verification_session(
        store=store,
        config=config,
        supabase_user_id="user-1",
        e164="+37255555555",
        dial_prefix="+372",
        provider="mock",
        now=now,
    )
    with pytest.raises(SmsSenderError) as exc_info:
        verify_phone_code(
            store=store,
            config=config,
            session_id=session.id,
            submitted_code="000000",
            e164="+37255555555",
            now=now,
        )
    assert exc_info.value.code is SmsErrorCode.CODE_MISMATCH
    updated = store.get_by_id(session.id)
    assert updated is not None
    assert updated.attempts == 1


def test_verify_too_many_attempts() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    config = _config()
    now = datetime(2026, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    session, _code = create_phone_verification_session(
        store=store,
        config=config,
        supabase_user_id="user-1",
        e164="+37255555555",
        dial_prefix="+372",
        provider="mock",
        now=now,
    )
    for _ in range(config.phone_max_attempts - 1):
        with pytest.raises(SmsSenderError) as exc_info:
            verify_phone_code(
                store=store,
                config=config,
                session_id=session.id,
                submitted_code="000000",
                e164="+37255555555",
                now=now,
            )
        assert exc_info.value.code is SmsErrorCode.CODE_MISMATCH

    with pytest.raises(SmsSenderError) as exc_info:
        verify_phone_code(
            store=store,
            config=config,
            session_id=session.id,
            submitted_code="000000",
            e164="+37255555555",
            now=now,
        )
    assert exc_info.value.code is SmsErrorCode.TOO_MANY_ATTEMPTS
    assert store.get_by_id(session.id) is not None
    assert store.get_by_id(session.id).status == "failed"


def test_verify_expired_code() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    config = _config()
    started = datetime(2026, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    session, code = create_phone_verification_session(
        store=store,
        config=config,
        supabase_user_id="user-1",
        e164="+37255555555",
        dial_prefix="+372",
        provider="mock",
        now=started,
    )
    later = started + timedelta(seconds=config.phone_code_ttl_s + 1)
    with pytest.raises(SmsSenderError) as exc_info:
        verify_phone_code(
            store=store,
            config=config,
            session_id=session.id,
            submitted_code=code,
            e164="+37255555555",
            now=later,
        )
    assert exc_info.value.code is SmsErrorCode.CODE_EXPIRED
    assert store.get_by_id(session.id) is not None
    assert store.get_by_id(session.id).status == "expired"


def test_repeat_create_invalidates_previous_session() -> None:
    store = InMemoryPhoneVerificationSessionStore()
    config = _config()
    now = datetime(2026, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    first, first_code = create_phone_verification_session(
        store=store,
        config=config,
        supabase_user_id="user-1",
        e164="+37255555555",
        dial_prefix="+372",
        provider="mock",
        now=now,
    )
    _second, _second_code = create_phone_verification_session(
        store=store,
        config=config,
        supabase_user_id="user-1",
        e164="+37255556666",
        dial_prefix="+372",
        provider="mock",
        now=now + timedelta(seconds=1),
    )
    assert store.get_by_id(first.id) is not None
    assert store.get_by_id(first.id).status == "failed"
    with pytest.raises(SmsSenderError):
        verify_phone_code(
            store=store,
            config=config,
            session_id=first.id,
            submitted_code=first_code,
            e164="+37255555555",
            now=now + timedelta(seconds=1),
        )


def test_plaintext_code_not_logged(caplog: pytest.LogCaptureFixture) -> None:
    store = InMemoryPhoneVerificationSessionStore()
    config = _config()
    now = datetime(2026, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    _session, code = create_phone_verification_session(
        store=store,
        config=config,
        supabase_user_id="user-1",
        e164="+37255555555",
        dial_prefix="+372",
        provider="mock",
        now=now,
    )
    assert code not in caplog.text
