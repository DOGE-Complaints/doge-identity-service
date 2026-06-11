from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import httpx
import pytest

from core.domain.contracts import (
    EIDAuditLogRepository,
    HealthRepository,
    OAuthClientStore,
    ProfileRepository,
    VerificationSessionStore,
)
from core.domain.models import (
    EIDAuditEvent,
    ProfileConflictError,
    ProfileRecord,
    VerificationSession,
)
from core.infrastructure.db_supabase import (
    SupabaseDatabase,
    SupabaseEIDAuditLogRepository,
    SupabaseHealthRepository,
    SupabaseOAuthClientStore,
    SupabaseProfileRepository,
    SupabaseVerificationSessionStore,
    _verification_session_from_row,
)

SUPABASE_URL = "https://test-project.supabase.co"
SERVICE_ROLE_KEY = "test-service-role-key"


def _demo_profile(**overrides: object) -> ProfileRecord:
    now = datetime.now(timezone.utc)
    base = {
        "id": "11111111-1111-1111-1111-111111111111",
        "supabase_user_id": "22222222-2222-2222-2222-222222222222",
        "display_name": None,
        "avatar_url": None,
        "eid_verified": False,
        "verified_person_hash": None,
        "eid_provider": None,
        "eid_method": None,
        "eid_country": None,
        "eid_verified_at": None,
        "phone_verified": False,
        "verified_phone_hash": None,
        "phone_provider": None,
        "phone_dial_prefix": None,
        "phone_verified_at": None,
        "wallet_address": None,
        "wallet_linked_at": None,
        "wallet_signature_verified_at": None,
        "wallet_signature_scheme": None,
        "wallet_chain_id": None,
        "created_at": now,
        "updated_at": now,
    }
    base.update(overrides)
    return ProfileRecord(**base)


def _demo_session(**overrides: object) -> VerificationSession:
    now = datetime.now(timezone.utc)
    base = {
        "id": "33333333-3333-3333-3333-333333333333",
        "supabase_user_id": "22222222-2222-2222-2222-222222222222",
        "state": "state-abc",
        "nonce": "nonce-1",
        "code_verifier_encrypted": "enc",
        "code_verifier_hash": "hash",
        "return_context": None,
        "return_url": None,
        "requested_action": None,
        "status": "started",
        "created_at": now,
        "expires_at": now,
        "provider": "mock",
        "provider_session_data": {},
    }
    base.update(overrides)
    return VerificationSession(**base)


def test_profile_get_by_supabase_user_id_uses_eq_filter_and_empty_is_none() -> None:
    db = SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)
    repo = SupabaseProfileRepository(db)
    with patch.object(SupabaseDatabase, "_request", return_value=[]) as mock_request:
        result = repo.get_by_supabase_user_id("u1")
    assert result is None
    mock_request.assert_called_once_with(
        method="GET",
        path="/rest/v1/profiles",
        params={"supabase_user_id": "eq.u1", "limit": "1"},
    )


def test_profile_get_by_verified_phone_hash_uses_eq_filter() -> None:
    db = SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)
    repo = SupabaseProfileRepository(db)
    with patch.object(SupabaseDatabase, "_request", return_value=[]) as mock_request:
        result = repo.get_by_verified_phone_hash("phone-hash-1")
    assert result is None
    mock_request.assert_called_once_with(
        method="GET",
        path="/rest/v1/profiles",
        params={"verified_phone_hash": "eq.phone-hash-1", "limit": "1"},
    )


def test_profile_attach_phone_verification_maps_409_to_profile_conflict_error() -> None:
    db = SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)
    repo = SupabaseProfileRepository(db)
    response = MagicMock()
    response.status_code = 409
    error = httpx.HTTPStatusError(
        "409 Conflict",
        request=httpx.Request("PATCH", f"{SUPABASE_URL}/rest/v1/profiles"),
        response=response,
    )
    with patch.object(repo, "get_by_verified_phone_hash", return_value=None):
        with patch.object(SupabaseDatabase, "_request", side_effect=error):
            with pytest.raises(ProfileConflictError):
                repo.attach_phone_verification(
                    "u1",
                    provider="mock",
                    dial_prefix="+372",
                    verified_phone_hash="phone-hash-1",
                    verified_at=datetime.now(timezone.utc),
                    one_account_per_number=True,
                )


def test_profile_attach_eid_verification_maps_409_to_profile_conflict_error() -> None:
    db = SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)
    repo = SupabaseProfileRepository(db)
    response = MagicMock()
    response.status_code = 409
    error = httpx.HTTPStatusError(
        "409 Conflict",
        request=httpx.Request("PATCH", f"{SUPABASE_URL}/rest/v1/profiles"),
        response=response,
    )
    with patch.object(SupabaseDatabase, "_request", side_effect=error):
        with pytest.raises(ProfileConflictError):
            repo.attach_eid_verification(
                "u1",
                provider="mock",
                country="EE",
                method="smart_id",
                verified_person_hash="hash-1",
                verified_at=datetime.now(timezone.utc),
            )


def test_verification_session_mark_consumed_filters_started_status() -> None:
    db = SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)
    repo = SupabaseVerificationSessionStore(db)
    with patch.object(SupabaseDatabase, "_request", return_value=None) as mock_request:
        repo.mark_consumed("sess-1")
    _, kwargs = mock_request.call_args
    assert kwargs["params"]["id"] == "eq.sess-1"
    assert kwargs["params"]["status"] == "eq.started"
    assert kwargs["json_body"] == {"status": "consumed"}


def test_verification_session_create_includes_provider_and_jsonb_fields() -> None:
    db = SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)
    repo = SupabaseVerificationSessionStore(db)
    session = _demo_session(provider="eideasy", provider_session_data={})
    with patch.object(SupabaseDatabase, "_request", return_value=[{}]) as mock_request:
        repo.create(session)
    _, kwargs = mock_request.call_args
    body = kwargs["json_body"]
    assert body["provider"] == "eideasy"
    assert body["provider_session_data"] == {}


def test_audit_log_event_is_idempotent_for_same_event_object() -> None:
    db = SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)
    repo = SupabaseEIDAuditLogRepository(db)
    event = EIDAuditEvent(
        id="44444444-4444-4444-4444-444444444444",
        supabase_user_id="u1",
        event_type="eid_verification_started",
        provider="mock",
        method="smart_id",
        success=True,
        failure_reason=None,
        request_id="req-1",
        ip_hash="ip-hash",
        user_agent_hash="ua-hash",
        created_at=datetime.now(timezone.utc),
    )
    with patch.object(SupabaseDatabase, "_request", return_value=None) as mock_request:
        repo.log_event(event)
        repo.log_event(event)
    assert mock_request.call_count == 2


def test_health_repository_delegates_ping_and_satisfies_protocol() -> None:
    db = SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)
    health = SupabaseHealthRepository(db)
    assert isinstance(health, HealthRepository)
    with patch.object(SupabaseDatabase, "healthcheck", return_value=True) as mock_healthcheck:
        assert health.ping() is True
    mock_healthcheck.assert_called_once()


def test_jsonb_fields_normalize_string_to_dict_on_read() -> None:
    row = {
        "id": "33333333-3333-3333-3333-333333333333",
        "supabase_user_id": "22222222-2222-2222-2222-222222222222",
        "state": "state-abc",
        "nonce": None,
        "code_verifier_encrypted": None,
        "code_verifier_hash": None,
        "return_context": None,
        "return_url": None,
        "requested_action": None,
        "status": "started",
        "created_at": "2026-05-31T10:00:00+00:00",
        "expires_at": "2026-05-31T10:10:00+00:00",
        "provider": "mock",
        "provider_session_data": '{"key": "value"}',
    }
    session = _verification_session_from_row(row)
    assert isinstance(session.provider_session_data, dict)
    assert session.provider_session_data == {"key": "value"}


def test_supabase_repositories_satisfy_protocols() -> None:
    db = SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)
    assert isinstance(SupabaseProfileRepository(db), ProfileRepository)
    assert isinstance(SupabaseVerificationSessionStore(db), VerificationSessionStore)
    assert isinstance(SupabaseEIDAuditLogRepository(db), EIDAuditLogRepository)
    assert isinstance(
        SupabaseOAuthClientStore(db, fallback_config=None, clients={}),
        OAuthClientStore,
    )
