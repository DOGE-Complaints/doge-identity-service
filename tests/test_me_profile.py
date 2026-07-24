"""EPIC-IDS-07 STORY-IDS-AUTHCORE-01 — GET /me profile and eid_verified."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, get_api_dependencies
from core.domain.models import ProfileRecord
from tests.supabase_jwt_harness import DEFAULT_USER_ID, mint_supabase_access_token

_DEMO_USER_ID = DEFAULT_USER_ID


@pytest.fixture(autouse=True)
def _reset_deps() -> None:
    _clear_api_dependencies_cache()
    yield
    _clear_api_dependencies_cache()


def _seed_profile(
    *,
    supabase_user_id: str = _DEMO_USER_ID,
    eid_verified: bool = True,
    display_name: str | None = "Test User",
) -> ProfileRecord:
    now = datetime.now(timezone.utc)
    record = ProfileRecord(
        id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        supabase_user_id=supabase_user_id,
        display_name=display_name,
        avatar_url="https://example.com/avatar.png",
        eid_verified=eid_verified,
        verified_person_hash="hash-demo" if eid_verified else None,
        eid_provider="mock" if eid_verified else None,
        eid_method="smart_id" if eid_verified else None,
        eid_country="EE" if eid_verified else None,
        eid_verified_at=now if eid_verified else None,
        phone_verified=False,
        verified_phone_hash=None,
        phone_provider=None,
        phone_dial_prefix=None,
        phone_verified_at=None,
        wallet_address=None,
        wallet_linked_at=None,
        wallet_signature_verified_at=None,
        wallet_signature_scheme=None,
        wallet_chain_id=None,
        created_at=now,
        updated_at=now,
    )
    repo = get_api_dependencies().profile_repository
    assert repo is not None
    return repo.upsert(record)


def test_me_without_auth_returns_401(test_client: TestClient) -> None:
    response = test_client.get("/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_me_with_valid_jwt_and_profile_returns_200_envelope(
    test_client: TestClient,
) -> None:
    _seed_profile()
    token = mint_supabase_access_token()
    response = test_client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    data = body["data"]
    assert data["supabase_user_id"] == _DEMO_USER_ID
    assert data["eid_verified"] is True
    assert data["role"] == "authenticated"
    assert data["display_name"] == "Test User"
    assert data["avatar_url"] == "https://example.com/avatar.png"
    assert data["eid_provider"] == "mock"
    assert data["eid_verified_at"] is not None
    assert data["account_status"] == "active"
    assert data["created_at"] is not None
    # ISO from ProfileRecord.created_at via _format_datetime
    assert "T" in data["created_at"]


def test_me_with_phone_verified_profile_returns_phone_fields(
    test_client: TestClient,
) -> None:
    now = datetime.now(timezone.utc)
    repo = get_api_dependencies().profile_repository
    assert repo is not None
    repo.upsert(
        ProfileRecord(
            id="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            supabase_user_id=_DEMO_USER_ID,
            display_name="Phone User",
            avatar_url=None,
            eid_verified=False,
            verified_person_hash=None,
            eid_provider=None,
            eid_method=None,
            eid_country=None,
            eid_verified_at=None,
            phone_verified=True,
            verified_phone_hash="secret-phone-hash",
            phone_provider="mock",
            phone_dial_prefix="+372",
            phone_verified_at=now,
            wallet_address=None,
            wallet_linked_at=None,
            wallet_signature_verified_at=None,
            wallet_signature_scheme=None,
            wallet_chain_id=None,
            created_at=now,
            updated_at=now,
        )
    )
    token = mint_supabase_access_token()
    response = test_client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["phone_verified"] is True
    assert data["phone_provider"] == "mock"
    assert data["phone_dial_prefix"] == "+372"
    assert data["phone_verified_at"] is not None
    assert "verified_phone_hash" not in data


def test_me_missing_profile_returns_200_not_verified_no_db_write(
    test_client: TestClient,
) -> None:
    """t01 decision: synthetic 200, eid_verified=false, no upsert on GET /me."""
    token = mint_supabase_access_token()
    response = test_client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["supabase_user_id"] == _DEMO_USER_ID
    assert data["eid_verified"] is False
    assert data["role"] == "authenticated"
    assert data["display_name"] is None
    assert data["avatar_url"] is None
    assert data["phone_verified"] is False
    assert data["phone_provider"] is None
    assert data["phone_dial_prefix"] is None
    assert data["phone_verified_at"] is None
    assert data["created_at"] is None
    assert data["account_status"] == "active"

    repo = get_api_dependencies().profile_repository
    assert repo is not None
    assert repo.get_by_supabase_user_id(_DEMO_USER_ID) is None


def test_me_response_uses_envelope_shape(test_client: TestClient) -> None:
    token = mint_supabase_access_token()
    response = test_client.get("/me", headers={"Authorization": f"Bearer {token}"})
    payload = response.json()
    assert set(payload.keys()) == {"data"}
    assert isinstance(payload["data"], dict)
