"""EPIC-IDS-11 STORY-IDS-OAUTH-01 — offline OAuth server flow tests."""

from __future__ import annotations

import base64
import hashlib
import time
from urllib.parse import parse_qs, urlparse

import pytest
from fastapi.testclient import TestClient
from joserfc import jwt
from joserfc.jwk import OctKey

from core.api.asgi_app import _clear_api_dependencies_cache, get_api_dependencies

_DEMO_JWT_SECRET = "test-secret-for-demo"
_DEMO_SUPABASE_URL = "https://demo.local"
_DEMO_USER_ID = "11111111-1111-1111-1111-111111111111"
_CLIENT_ID = "test-gpt-client"
_CLIENT_SECRET = "test-gpt-client-secret"
_REDIRECT_URI = "https://oauth.pstmn.io/v1/callback"


@pytest.fixture(autouse=True)
def _reset_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("SUPABASE_JWT_SECRET", _DEMO_JWT_SECRET)
    monkeypatch.setenv("SUPABASE_URL", _DEMO_SUPABASE_URL)
    monkeypatch.setenv("SMS_PROVIDER", "mock")
    monkeypatch.setenv("PHONE_ALLOWED_DIAL_PREFIXES", "+372")
    monkeypatch.setenv("PHONE_CODE_LENGTH", "6")
    monkeypatch.setenv("PHONE_CODE_TTL_S", "300")
    monkeypatch.setenv("PHONE_MAX_ATTEMPTS", "5")
    monkeypatch.setenv("PHONE_RESEND_COOLDOWN_S", "60")
    monkeypatch.setenv("PHONE_ONE_ACCOUNT_PER_NUMBER", "true")
    yield
    _clear_api_dependencies_cache()


def _demo_bearer_token(*, sub: str = _DEMO_USER_ID) -> str:
    now = int(time.time())
    claims = {
        "sub": sub,
        "role": "authenticated",
        "aud": "authenticated",
        "iss": f"{_DEMO_SUPABASE_URL.rstrip('/')}/auth/v1",
        "exp": now + 3600,
        "iat": now,
    }
    key = OctKey.import_key(_DEMO_JWT_SECRET)
    return jwt.encode({"alg": "HS256"}, claims, key)


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


def test_oauth_authorize_happy_path_redirects_to_spa_login(test_client: TestClient) -> None:
    response = test_client.get("/oauth/authorize", params=_authorize_params(), follow_redirects=False)
    assert response.status_code == 302
    location = response.headers["location"]
    assert location.startswith("http://localhost:3000/login?")
    query = parse_qs(urlparse(location).query)
    oauth_request_id = query["oauth_request_id"][0]
    deps = get_api_dependencies()
    assert deps.oauth_authorization_request_store is not None
    stored = deps.oauth_authorization_request_store.get(oauth_request_id)
    assert stored is not None
    assert stored.state == "csrf-state-123"
    assert stored.client_id == _CLIENT_ID


def test_oauth_authorize_invalid_client(test_client: TestClient) -> None:
    response = test_client.get(
        "/oauth/authorize",
        params=_authorize_params(client_id="unknown-client"),
    )
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "invalid_client"


def test_oauth_authorize_invalid_redirect_uri(test_client: TestClient) -> None:
    response = test_client.get(
        "/oauth/authorize",
        params=_authorize_params(redirect_uri="https://evil.example/callback"),
    )
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "invalid_redirect_uri"


def test_oauth_authorize_invalid_scope(test_client: TestClient) -> None:
    response = test_client.get(
        "/oauth/authorize",
        params=_authorize_params(scope="admin:all"),
    )
    assert response.status_code == 400
    body = response.json()
    assert body["error"] == "invalid_scope"


def test_oauth_full_flow_with_pkce(test_client: TestClient) -> None:
    verifier, challenge = _pkce_pair()
    authorize = test_client.get(
        "/oauth/authorize",
        params=_authorize_params(code_challenge=challenge, code_challenge_method="S256"),
        follow_redirects=False,
    )
    assert authorize.status_code == 302
    oauth_request_id = parse_qs(urlparse(authorize.headers["location"]).query)["oauth_request_id"][0]

    complete = test_client.post(
        "/oauth/authorize/complete",
        headers={"Authorization": f"Bearer {_demo_bearer_token()}"},
        json={"oauth_request_id": oauth_request_id},
        follow_redirects=False,
    )
    assert complete.status_code == 302
    callback_query = parse_qs(urlparse(complete.headers["location"]).query)
    assert callback_query["state"] == ["csrf-state-123"]
    code = callback_query["code"][0]

    token = test_client.post(
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
    assert token.status_code == 200
    token_body = token.json()
    assert token_body["token_type"] == "Bearer"
    assert token_body["access_token"]

    deps = get_api_dependencies()
    assert deps.oauth_token_service is not None
    claims = deps.oauth_token_service.validate_access_token(token_body["access_token"])
    assert claims.sub == _DEMO_USER_ID


def test_oauth_token_rejects_wrong_client_secret(test_client: TestClient) -> None:
    authorize = test_client.get(
        "/oauth/authorize",
        params=_authorize_params(),
        follow_redirects=False,
    )
    oauth_request_id = parse_qs(urlparse(authorize.headers["location"]).query)["oauth_request_id"][0]
    complete = test_client.post(
        "/oauth/authorize/complete",
        headers={"Authorization": f"Bearer {_demo_bearer_token()}"},
        json={"oauth_request_id": oauth_request_id},
        follow_redirects=False,
    )
    code = parse_qs(urlparse(complete.headers["location"]).query)["code"][0]
    response = test_client.post(
        "/oauth/token",
        json={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": _CLIENT_ID,
            "client_secret": "wrong-secret",
            "redirect_uri": _REDIRECT_URI,
        },
    )
    assert response.status_code == 401
    assert response.json()["error"] == "invalid_client"


def test_oauth_token_rejects_reused_code(test_client: TestClient) -> None:
    authorize = test_client.get("/oauth/authorize", params=_authorize_params(), follow_redirects=False)
    oauth_request_id = parse_qs(urlparse(authorize.headers["location"]).query)["oauth_request_id"][0]
    complete = test_client.post(
        "/oauth/authorize/complete",
        headers={"Authorization": f"Bearer {_demo_bearer_token()}"},
        json={"oauth_request_id": oauth_request_id},
        follow_redirects=False,
    )
    code = parse_qs(urlparse(complete.headers["location"]).query)["code"][0]
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": _CLIENT_ID,
        "client_secret": _CLIENT_SECRET,
        "redirect_uri": _REDIRECT_URI,
    }
    first = test_client.post("/oauth/token", json=payload)
    assert first.status_code == 200
    second = test_client.post("/oauth/token", json=payload)
    assert second.status_code == 400
    assert second.json()["error"] == "invalid_grant"


def test_oauth_token_pkce_mismatch(test_client: TestClient) -> None:
    verifier, challenge = _pkce_pair()
    authorize = test_client.get(
        "/oauth/authorize",
        params=_authorize_params(code_challenge=challenge, code_challenge_method="S256"),
        follow_redirects=False,
    )
    oauth_request_id = parse_qs(urlparse(authorize.headers["location"]).query)["oauth_request_id"][0]
    complete = test_client.post(
        "/oauth/authorize/complete",
        headers={"Authorization": f"Bearer {_demo_bearer_token()}"},
        json={"oauth_request_id": oauth_request_id},
        follow_redirects=False,
    )
    code = parse_qs(urlparse(complete.headers["location"]).query)["code"][0]
    response = test_client.post(
        "/oauth/token",
        json={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": _CLIENT_ID,
            "client_secret": _CLIENT_SECRET,
            "redirect_uri": _REDIRECT_URI,
            "code_verifier": "wrong-verifier",
        },
    )
    assert response.status_code == 400
    assert response.json()["error"] == "invalid_grant"


def test_me_accepts_oauth_access_token(test_client: TestClient) -> None:
    authorize = test_client.get("/oauth/authorize", params=_authorize_params(), follow_redirects=False)
    oauth_request_id = parse_qs(urlparse(authorize.headers["location"]).query)["oauth_request_id"][0]
    complete = test_client.post(
        "/oauth/authorize/complete",
        headers={"Authorization": f"Bearer {_demo_bearer_token()}"},
        json={"oauth_request_id": oauth_request_id},
        follow_redirects=False,
    )
    code = parse_qs(urlparse(complete.headers["location"]).query)["code"][0]
    token = test_client.post(
        "/oauth/token",
        json={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": _CLIENT_ID,
            "client_secret": _CLIENT_SECRET,
            "redirect_uri": _REDIRECT_URI,
        },
    )
    access_token = token.json()["access_token"]
    me = test_client.get("/me", headers={"Authorization": f"Bearer {access_token}"})
    assert me.status_code == 200
    assert me.json()["data"]["supabase_user_id"] == _DEMO_USER_ID


def test_oauth_rfc_error_shape(test_client: TestClient) -> None:
    response = test_client.get(
        "/oauth/authorize",
        params=_authorize_params(client_id="missing"),
    )
    body = response.json()
    assert set(body.keys()) == {"error", "error_description"}
    assert isinstance(body["error"], str)
    assert isinstance(body["error_description"], str)
