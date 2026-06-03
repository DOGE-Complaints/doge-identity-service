"""Live identity repository roundtrips (UUID4 keys, teardown DELETE)."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import pytest

from core.domain.models import EIDAuditEvent, ProfileConflictError, ProfileRecord, VerificationSession
from core.infrastructure.db_supabase import (
    SupabaseDatabase,
    SupabaseEIDAuditLogRepository,
    SupabaseProfileRepository,
    SupabaseVerificationSessionStore,
    _verification_session_from_row,
)
from tests.integration.supabase.conftest import _require_supabase_creds_from_dotenv


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _live_db() -> SupabaseDatabase:
    url, key = _require_supabase_creds_from_dotenv()
    return SupabaseDatabase.from_http(url, key)


def _delete_profile(db: SupabaseDatabase, supabase_user_id: str) -> None:
    db._request(
        method="DELETE",
        path="/rest/v1/profiles",
        params={"supabase_user_id": f"eq.{supabase_user_id}"},
    )


def _delete_session(db: SupabaseDatabase, session_id: str) -> None:
    db._request(
        method="DELETE",
        path="/rest/v1/eid_verification_sessions",
        params={"id": f"eq.{session_id}"},
    )


def _delete_audit_by_request_id(db: SupabaseDatabase, request_id: str) -> None:
    db._request(
        method="DELETE",
        path="/rest/v1/eid_audit_events",
        params={"request_id": f"eq.{request_id}"},
    )


def _get_session_by_id(db: SupabaseDatabase, session_id: str) -> VerificationSession | None:
    rows = db._request(
        method="GET",
        path="/rest/v1/eid_verification_sessions",
        params={"id": f"eq.{session_id}", "limit": "1"},
    )
    if not rows:
        return None
    row = rows[0] if isinstance(rows, list) else rows
    return _verification_session_from_row(row)


def test_profile_upsert_and_read() -> None:
    db = _live_db()
    repo = SupabaseProfileRepository(db)
    user_id = f"test-{uuid.uuid4()}"
    profile_id = str(uuid.uuid4())
    now = _utcnow()
    record = ProfileRecord(
        id=profile_id,
        supabase_user_id=user_id,
        display_name="live-roundtrip",
        avatar_url=None,
        eid_verified=False,
        verified_person_hash=None,
        eid_provider=None,
        eid_method=None,
        eid_country=None,
        eid_verified_at=None,
        wallet_address=None,
        wallet_linked_at=None,
        wallet_signature_verified_at=None,
        wallet_signature_scheme=None,
        wallet_chain_id=None,
        created_at=now,
        updated_at=now,
    )
    try:
        repo.upsert(record)
        loaded = repo.get_by_supabase_user_id(user_id)
        assert loaded is not None
        assert loaded.supabase_user_id == user_id
        assert loaded.display_name == "live-roundtrip"
        assert loaded.id == profile_id
    finally:
        _delete_profile(db, user_id)


def test_verification_session_create_and_consume() -> None:
    db = _live_db()
    store = SupabaseVerificationSessionStore(db)
    user_id = f"test-{uuid.uuid4()}"
    session_id = str(uuid.uuid4())
    state = f"test-state-{uuid.uuid4()}"
    now = _utcnow()
    session = VerificationSession(
        id=session_id,
        supabase_user_id=user_id,
        state=state,
        nonce="nonce-live",
        code_verifier_encrypted=None,
        code_verifier_hash=None,
        return_context=None,
        return_url=None,
        requested_action=None,
        status="started",
        created_at=now,
        expires_at=now + timedelta(hours=1),
        provider="mock",
        provider_session_data={},
    )
    try:
        store.create(session)
        assert store.get_by_state(state) is not None
        store.mark_consumed(session_id)
        assert store.get_by_state(state) is None
        consumed = _get_session_by_id(db, session_id)
        assert consumed is not None
        assert consumed.status == "consumed"
    finally:
        _delete_session(db, session_id)
        _delete_profile(db, user_id)


def test_eid_audit_event_append() -> None:
    db = _live_db()
    repo = SupabaseEIDAuditLogRepository(db)
    user_id = f"test-{uuid.uuid4()}"
    request_id = f"test-req-{uuid.uuid4()}"
    event_id = str(uuid.uuid4())
    event = EIDAuditEvent(
        id=event_id,
        supabase_user_id=user_id,
        event_type="eid_verification_started",
        provider="mock",
        method="smart_id",
        success=True,
        failure_reason=None,
        request_id=request_id,
        ip_hash="ip-hash-live",
        user_agent_hash="ua-hash-live",
        created_at=_utcnow(),
    )
    try:
        repo.log_event(event)
        rows = repo.list_events(supabase_user_id=user_id, limit=50)
        ids = {e.id for e in rows}
        assert event_id in ids
    finally:
        _delete_audit_by_request_id(db, request_id)


def test_partial_unique_verified_person_hash() -> None:
    db = _live_db()
    repo = SupabaseProfileRepository(db)
    user_a = f"test-{uuid.uuid4()}"
    user_b = f"test-{uuid.uuid4()}"
    person_hash = f"test-hash-{uuid.uuid4()}"
    verified_at = _utcnow()
    try:
        repo.upsert(
            ProfileRecord(
                id=str(uuid.uuid4()),
                supabase_user_id=user_a,
                display_name=None,
                avatar_url=None,
                eid_verified=False,
                verified_person_hash=None,
                eid_provider=None,
                eid_method=None,
                eid_country=None,
                eid_verified_at=None,
                wallet_address=None,
                wallet_linked_at=None,
                wallet_signature_verified_at=None,
                wallet_signature_scheme=None,
                wallet_chain_id=None,
                created_at=verified_at,
                updated_at=verified_at,
            )
        )
        repo.attach_eid_verification(
            user_a,
            provider="mock",
            country="EE",
            method="smart_id",
            verified_person_hash=person_hash,
            verified_at=verified_at,
        )
        repo.upsert(
            ProfileRecord(
                id=str(uuid.uuid4()),
                supabase_user_id=user_b,
                display_name=None,
                avatar_url=None,
                eid_verified=False,
                verified_person_hash=None,
                eid_provider=None,
                eid_method=None,
                eid_country=None,
                eid_verified_at=None,
                wallet_address=None,
                wallet_linked_at=None,
                wallet_signature_verified_at=None,
                wallet_signature_scheme=None,
                wallet_chain_id=None,
                created_at=verified_at,
                updated_at=verified_at,
            )
        )
        with pytest.raises(ProfileConflictError):
            repo.attach_eid_verification(
                user_b,
                provider="mock",
                country="EE",
                method="smart_id",
                verified_person_hash=person_hash,
                verified_at=verified_at,
            )
    finally:
        _delete_profile(db, user_a)
        _delete_profile(db, user_b)
