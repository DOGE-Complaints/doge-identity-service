"""EPIC-IDS-11 STORY-IDS-OAUTH-02 — OAuth introspection + service token gate.

Gateway contract (POST /oauth/introspect):
| Field           | Type    | When active=true |
|-----------------|---------|------------------|
| active          | bool    | always           |
| sub             | string  | required         |
| phone_verified  | bool    | required         |
"""

from __future__ import annotations

import base64
import hashlib
import json
import time
from datetime import datetime, timezone
from urllib.parse import parse_qs, urlparse

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, get_api_dependencies
from core.domain.models import ProfileRecord
from tests.supabase_jwt_harness import DEFAULT_USER_ID, mint_supabase_access_token

_SERVICE_TOKEN = "test-service-api-token"
_DEMO_USER_ID = DEFAULT_USER_ID
_CLIENT_ID = "test-gpt-client"
_CLIENT_SECRET = "test-gpt-client-secret"
_REDIRECT_URI = "https://oauth.pstmn.io/v1/callback"


@pytest.fixture(autouse=True)
def _introspection_env(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("SERVICE_API_TOKEN", _SERVICE_TOKEN)
    yield
    _clear_api_dependencies_cache()


def _service_headers(*, token: str | None = _SERVICE_TOKEN) -> dict[str, str]:
    if token is None:
        return {}
    return {"Authorization": f"Bearer {token}"}


def _pkce_pair() -> tuple[str, str]:
    verifier = "test-verifier-12345678901234567890123456789012"
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
    return verifier, challenge


def _authorize_params(**overrides: str) -> dict[str, str]:
    params = {
        "response_type": "code",
        "client_id": _CLIENT_ID,
        "redirect_uri": _REDIRECT_URI,
        "scope": "profile:read stories:draft",
        "state": "csrf-state-123",
    }
    params.update(overrides)
    return params


def _issue_oauth_access_token(test_client: TestClient) -> str:
    verifier, challenge = _pkce_pair()
    authorize = test_client.get(
        "/oauth/authorize",
        params=_authorize_params(code_challenge=challenge, code_challenge_method="S256"),
        follow_redirects=False,
    )
    oauth_request_id = parse_qs(urlparse(authorize.headers["location"]).query)["oauth_request_id"][0]
    complete = test_client.post(
        "/oauth/authorize/complete",
        headers={"Authorization": f"Bearer {mint_supabase_access_token()}"},
        json={"oauth_request_id": oauth_request_id},
        follow_redirects=False,
    )
    code = parse_qs(urlparse(complete.headers["location"]).query)["code"][0]
    token_resp = test_client.post(
        "/oauth/token",
        json={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": _CLIENT_ID,
            "client_secret": _CLIENT_SECRET,
            "redirect_uri": _REDIRECT_URI,
            "code_verifier": verifier,
        },
    )
    return token_resp.json()["access_token"]


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


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _expired_oauth_access_token() -> str:
    import hmac

    secret = "test-oauth-secret-not-real"
    now = int(time.time())
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "iss": "http://localhost:8100",
        "sub": _DEMO_USER_ID,
        "aud": "doge-identity-service",
        "exp": now - 60,
        "iat": now - 120,
        "jti": "expired-jti",
        "scope": "profile:read",
        "token_type": "oauth_access",
        "client_id": _CLIENT_ID,
    }
    header_segment = _b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    payload_segment = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{header_segment}.{payload_segment}".encode()
    sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    return f"{header_segment}.{payload_segment}.{_b64url_encode(sig)}"


def test_introspect_valid_token_returns_active_with_profile_phone_verified(
    test_client: TestClient,
) -> None:
    _seed_profile(phone_verified=True)
    access_token = _issue_oauth_access_token(test_client)
    response = test_client.post(
        "/oauth/introspect",
        headers=_service_headers(),
        json={"token": access_token},
    )
    assert response.status_code == 200
    body = response.json()
    assert body == {
        "active": True,
        "sub": _DEMO_USER_ID,
        "phone_verified": True,
    }


def test_introspect_phone_verified_from_profile_not_jwt(test_client: TestClient) -> None:
    _seed_profile(phone_verified=False)
    access_token = _issue_oauth_access_token(test_client)
    response = test_client.post(
        "/oauth/introspect",
        headers=_service_headers(),
        json={"token": access_token},
    )
    assert response.status_code == 200
    assert response.json()["phone_verified"] is False


def test_introspect_invalid_user_token_returns_inactive(test_client: TestClient) -> None:
    response = test_client.post(
        "/oauth/introspect",
        headers=_service_headers(),
        json={"token": "not-a-valid-jwt"},
    )
    assert response.status_code == 200
    assert response.json() == {"active": False}


def test_introspect_expired_user_token_returns_inactive(test_client: TestClient) -> None:
    response = test_client.post(
        "/oauth/introspect",
        headers=_service_headers(),
        json={"token": _expired_oauth_access_token()},
    )
    assert response.status_code == 200
    assert response.json() == {"active": False}


def test_introspect_missing_service_token_returns_401(test_client: TestClient) -> None:
    access_token = _issue_oauth_access_token(test_client)
    response = test_client.post(
        "/oauth/introspect",
        headers=_service_headers(token=None),
        json={"token": access_token},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_introspect_invalid_service_token_returns_401(test_client: TestClient) -> None:
    access_token = _issue_oauth_access_token(test_client)
    response = test_client.post(
        "/oauth/introspect",
        headers=_service_headers(token="wrong-service-token"),
        json={"token": access_token},
    )
    assert response.status_code == 401


def test_introspect_accepts_x_service_token_header(test_client: TestClient) -> None:
    _seed_profile(phone_verified=True)
    access_token = _issue_oauth_access_token(test_client)
    response = test_client.post(
        "/oauth/introspect",
        headers={"X-Service-Token": _SERVICE_TOKEN},
        json={"token": access_token},
    )
    assert response.status_code == 200
    assert response.json()["active"] is True
