"""EPIC-IDS-11 STORY-IDS-OAUTH-04 — offline OAuth verify-gate tests."""

from __future__ import annotations

from datetime import datetime, timezone
from urllib.parse import parse_qs, urlparse

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, get_api_dependencies
from core.domain.models import ProfileRecord
from core.oauth.verification_required import (
    VERIFICATION_REQUIRED_ERROR,
    VERIFICATION_REQUIRED_HTTP_STATUS,
)
from tests.supabase_jwt_harness import DEFAULT_USER_ID, mint_supabase_access_token
from tests.test_oauth_server_flow import _authorize_params

_DEMO_USER_ID = DEFAULT_USER_ID

_RETURN_CONTEXT = "gpt-submit-session-abc123"


@pytest.fixture(autouse=True)
def _reset_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("SMS_PROVIDER", "mock")
    monkeypatch.setenv("PHONE_ALLOWED_DIAL_PREFIXES", "+372")
    monkeypatch.setenv("PHONE_CODE_LENGTH", "6")
    monkeypatch.setenv("PHONE_CODE_TTL_S", "300")
    monkeypatch.setenv("PHONE_MAX_ATTEMPTS", "5")
    monkeypatch.setenv("PHONE_RESEND_COOLDOWN_S", "60")
    monkeypatch.setenv("PHONE_ONE_ACCOUNT_PER_NUMBER", "true")
    yield
    _clear_api_dependencies_cache()


def _relay_authorize_params(**overrides: str) -> dict[str, str]:
    params = _authorize_params(
        requested_action="stories:submit",
        return_context=_RETURN_CONTEXT,
    )
    params.update(overrides)
    return params


def _seed_profile(*, phone_verified: bool) -> None:
    now = datetime.now(timezone.utc)
    repo = get_api_dependencies().profile_repository
    assert repo is not None
    repo.upsert(
        ProfileRecord(
            id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            supabase_user_id=_DEMO_USER_ID,
            display_name="Test User",
            avatar_url=None,
            eid_verified=False,
            verified_person_hash=None,
            eid_provider=None,
            eid_method=None,
            eid_country=None,
            eid_verified_at=None,
            phone_verified=phone_verified,
            verified_phone_hash="phone-hash" if phone_verified else None,
            phone_provider="mock" if phone_verified else None,
            phone_dial_prefix="+372" if phone_verified else None,
            phone_verified_at=now if phone_verified else None,
            wallet_address=None,
            wallet_linked_at=None,
            wallet_signature_verified_at=None,
            wallet_signature_scheme=None,
            wallet_chain_id=None,
            created_at=now,
            updated_at=now,
        )
    )


def _authorize_and_get_request_id(test_client: TestClient) -> str:
    response = test_client.get(
        "/oauth/authorize",
        params=_relay_authorize_params(),
        follow_redirects=False,
    )
    assert response.status_code == 302
    return parse_qs(urlparse(response.headers["location"]).query)["oauth_request_id"][0]


def test_oauth_authorize_relay_persists_requested_action_and_return_context(
    test_client: TestClient,
) -> None:
    oauth_request_id = _authorize_and_get_request_id(test_client)
    deps = get_api_dependencies()
    assert deps.oauth_authorization_request_store is not None
    stored = deps.oauth_authorization_request_store.get(oauth_request_id)
    assert stored is not None
    assert stored.requested_action == "stories:submit"
    assert stored.return_context == _RETURN_CONTEXT


def test_oauth_authorize_rejects_invalid_requested_action(test_client: TestClient) -> None:
    response = test_client.get(
        "/oauth/authorize",
        params=_relay_authorize_params(requested_action="admin:destroy"),
    )
    assert response.status_code == 400
    assert response.json()["error"] == "invalid_request"


def test_oauth_complete_unverified_stories_submit_returns_verification_required(
    test_client: TestClient,
) -> None:
    _seed_profile(phone_verified=False)
    oauth_request_id = _authorize_and_get_request_id(test_client)

    complete = test_client.post(
        "/oauth/authorize/complete",
        headers={"Authorization": f"Bearer {mint_supabase_access_token()}"},
        json={"oauth_request_id": oauth_request_id},
    )
    assert complete.status_code == VERIFICATION_REQUIRED_HTTP_STATUS
    body = complete.json()
    assert body["error"] == VERIFICATION_REQUIRED_ERROR
    assert isinstance(body["reason"], str)
    assert body["verify_url"].startswith("http://localhost:3000/verify")
    assert f"context={_RETURN_CONTEXT}" in body["verify_url"]

    deps = get_api_dependencies()
    assert deps.oauth_authorization_request_store is not None
    assert deps.oauth_authorization_request_store.get(oauth_request_id) is not None


def test_oauth_complete_verified_stories_submit_issues_code(test_client: TestClient) -> None:
    _seed_profile(phone_verified=True)
    oauth_request_id = _authorize_and_get_request_id(test_client)

    complete = test_client.post(
        "/oauth/authorize/complete",
        headers={"Authorization": f"Bearer {mint_supabase_access_token()}"},
        json={"oauth_request_id": oauth_request_id},
        follow_redirects=False,
    )
    assert complete.status_code == 302
    callback_query = parse_qs(urlparse(complete.headers["location"]).query)
    assert "code" in callback_query
    assert callback_query["state"] == ["csrf-state-123"]


def test_oauth_complete_without_verify_requiring_action_issues_code(
    test_client: TestClient,
) -> None:
    _seed_profile(phone_verified=False)
    authorize = test_client.get(
        "/oauth/authorize",
        params=_authorize_params(),
        follow_redirects=False,
    )
    oauth_request_id = parse_qs(urlparse(authorize.headers["location"]).query)["oauth_request_id"][0]

    complete = test_client.post(
        "/oauth/authorize/complete",
        headers={"Authorization": f"Bearer {mint_supabase_access_token()}"},
        json={"oauth_request_id": oauth_request_id},
        follow_redirects=False,
    )
    assert complete.status_code == 302
    assert "code" in parse_qs(urlparse(complete.headers["location"]).query)


def test_verification_required_separate_from_sms_error_http_mapping(
    test_client: TestClient,
) -> None:
    assert VERIFICATION_REQUIRED_HTTP_STATUS == 403

    _seed_profile(phone_verified=False)
    oauth_request_id = _authorize_and_get_request_id(test_client)
    verify_need = test_client.post(
        "/oauth/authorize/complete",
        headers={"Authorization": f"Bearer {mint_supabase_access_token()}"},
        json={"oauth_request_id": oauth_request_id},
    )
    assert verify_need.status_code == 403
    assert verify_need.json()["error"] == VERIFICATION_REQUIRED_ERROR

    otp_request = test_client.post(
        "/auth/phone/request",
        headers={"Authorization": f"Bearer {mint_supabase_access_token()}"},
        json={"phone": "not-a-phone"},
    )
    assert otp_request.status_code == 400
    assert otp_request.json()["error"] != VERIFICATION_REQUIRED_ERROR
