"""EPIC-IDS-09 STORY-IDS-EID-06 — callback redirect render and JSON negotiate (offline)."""

from __future__ import annotations

import time
from unittest.mock import patch

import pytest
from joserfc import jwt
from joserfc.jwk import OctKey

from core.api.asgi_app import _clear_api_dependencies_cache, get_api_dependencies
from core.providers.base import EIDProviderError, EidErrorCode
from core.providers.mock.mock_provider import MockEIDProvider

_DEMO_JWT_SECRET = "test-secret-for-demo"
_DEMO_SUPABASE_URL = "https://demo.local"
_DEMO_USER_ID = "11111111-1111-1111-1111-111111111111"
_RETURN_URL = "https://dogestonia.ee/verify"
_JSON_ACCEPT = {"Accept": "application/json"}


@pytest.fixture(autouse=True)
def _reset_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("ALLOWED_RETURN_URLS", _RETURN_URL)
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


def _start_payload(**overrides: object) -> dict[str, str]:
    payload = {
        "return_url": _RETURN_URL,
        "return_context": "dashboard_verification",
        "requested_action": "eid:verify",
    }
    payload.update(overrides)
    return payload


def _start_and_get_callback_url(test_client) -> str:
    token = _demo_bearer_token()
    start = test_client.post(
        "/auth/eid/start",
        headers={"Authorization": f"Bearer {token}"},
        json=_start_payload(),
    )
    assert start.status_code == 200
    return start.json()["data"]["redirect_url"]


def test_mock_callback_browser_redirects_with_verified_marker(test_client) -> None:
    redirect_url = _start_and_get_callback_url(test_client)
    callback = test_client.get(redirect_url, follow_redirects=False)
    assert callback.status_code == 303
    location = callback.headers["location"]
    assert location.startswith(_RETURN_URL)
    assert "eid_status=verified" in location


def test_mock_callback_json_variant_returns_verified_envelope(test_client) -> None:
    redirect_url = _start_and_get_callback_url(test_client)
    callback = test_client.get(redirect_url, headers=_JSON_ACCEPT)
    assert callback.status_code == 200
    assert callback.json()["data"]["status"] == "verified"


def test_mock_callback_provider_error_redirects_with_canonical_marker(
    test_client,
) -> None:
    redirect_url = _start_and_get_callback_url(test_client)
    with patch.object(
        MockEIDProvider,
        "handle_callback",
        side_effect=EIDProviderError(
            "cancelled",
            code=EidErrorCode.USER_CANCELLED,
        ),
    ):
        callback = test_client.get(redirect_url, follow_redirects=False)
    assert callback.status_code == 303
    location = callback.headers["location"]
    assert "eid_status=error" in location
    assert "eid_error=USER_CANCELLED" in location


def test_unknown_session_callback_returns_400_without_redirect(test_client) -> None:
    callback = test_client.get(
        "/auth/mock/callback?session_id=00000000-0000-0000-0000-000000000000",
        follow_redirects=False,
    )
    assert callback.status_code == 400
    assert "location" not in callback.headers
    assert callback.json()["error"]["code"] == "invalid_or_consumed_state"


def test_unregistered_provider_callback_raises_config_error(test_client) -> None:
    response = test_client.get("/auth/eideasy/callback?state=unused")
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "CONFIG_ERROR"
    assert "eideasy" in response.json()["error"]["message"]


def test_dynamic_callback_route_resolves_mock_provider(test_client) -> None:
    paths = {getattr(route, "path", None) for route in test_client.app.routes}
    assert "/auth/{provider}/callback" in paths
    assert "/auth/mock/callback" not in paths
    assert "/auth/eideasy/callback" not in paths


def test_handle_auth_eid_callback_returns_outcome_type() -> None:
    from core.api.eid_callback import EidCallbackOutcome
    from core.api.handlers import handle_auth_eid_callback
    from core.security.audit_context import AuditHashes

    deps = get_api_dependencies()
    empty_audit = AuditHashes(ip_hash=None, user_agent_hash=None)
    outcome = handle_auth_eid_callback(
        deps,
        provider_name="mock",
        raw_params={"session_id": "missing"},
        trace_id="trace-test",
        audit=empty_audit,
    )
    assert isinstance(outcome, EidCallbackOutcome)
    assert outcome.outcome == "failed"
