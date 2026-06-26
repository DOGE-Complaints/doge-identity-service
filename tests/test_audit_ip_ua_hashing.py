"""SEC-02 — audit IP/UA hashing tests."""

from __future__ import annotations

import time

import pytest
from fastapi import Request
from fastapi.testclient import TestClient
from joserfc import jwt
from joserfc.jwk import OctKey

from core.api.asgi_app import _clear_api_dependencies_cache, get_api_dependencies
from core.security.audit_context import audit_hashes_from_request, hash_audit_value
from core.security.hashing import hash_secret

_DEMO_JWT_SECRET = "test-secret-for-demo"
_DEMO_SUPABASE_URL = "https://demo.local"
_DEMO_USER_ID = "11111111-1111-1111-1111-111111111111"
_EE_PHONE = "+37255555555"
_RETURN_URL = "https://dogestonia.ee/verify"
_TEST_UA = "DogestoniaTestAgent/1.0"
_EID_HASH_KEY = "test-eid-hash-secret-not-real"


@pytest.fixture(autouse=True)
def _reset_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("ALLOWED_RETURN_URLS", _RETURN_URL)
    monkeypatch.setenv("SMS_PROVIDER", "mock")
    monkeypatch.setenv("PHONE_ALLOWED_DIAL_PREFIXES", "+372")
    monkeypatch.setenv("PHONE_RESEND_COOLDOWN_S", "0")
    monkeypatch.setenv("DOGESTONIA_EID_SECRET", _EID_HASH_KEY)
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


def test_hash_audit_value_uses_hmac_sha256() -> None:
    digest = hash_audit_value("203.0.113.1", key="secret-key")
    assert digest == hash_secret("203.0.113.1", key="secret-key")
    assert digest is not None
    assert len(digest) == 64


def test_audit_hashes_from_request_hashes_ip_and_ua() -> None:
    scope = {
        "type": "http",
        "headers": [(b"user-agent", _TEST_UA.encode())],
        "client": ("198.51.100.42", 12345),
    }
    request = Request(scope)
    hashes = audit_hashes_from_request(
        request,
        hashing_key=_EID_HASH_KEY,
        trusted_proxy_count=0,
    )
    assert hashes.ip_hash == hash_secret("198.51.100.42", key=_EID_HASH_KEY)
    assert hashes.user_agent_hash == hash_secret(_TEST_UA, key=_EID_HASH_KEY)


def test_eid_start_audit_records_hashed_ip_ua_not_raw(
    test_client: TestClient,
) -> None:
    token = _demo_bearer_token()
    response = test_client.post(
        "/auth/eid/start",
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": _TEST_UA,
        },
        json={
            "return_url": _RETURN_URL,
            "return_context": "dashboard_verification",
            "requested_action": "eid:verify",
        },
    )
    assert response.status_code == 200

    deps = get_api_dependencies()
    assert deps.eid_audit_log_repository is not None
    events = deps.eid_audit_log_repository.list_events(
        supabase_user_id=_DEMO_USER_ID,
        event_type="eid_verification_started",
    )
    assert len(events) == 1
    event = events[0]
    assert event.ip_hash is not None
    assert event.user_agent_hash is not None
    assert event.ip_hash != "testclient"
    assert event.user_agent_hash != _TEST_UA
    serialized = f"{event.ip_hash}|{event.user_agent_hash}"
    assert "testclient" not in serialized
    assert _TEST_UA not in serialized


def test_phone_request_audit_records_hashed_ip_ua_not_raw(
    test_client: TestClient,
) -> None:
    from tests.test_phone_verification_flow import _mock_sender

    token = _demo_bearer_token()
    response = test_client.post(
        "/auth/phone/request",
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": _TEST_UA,
        },
        json={"phone": _EE_PHONE},
    )
    assert response.status_code == 200
    _mock_sender()

    deps = get_api_dependencies()
    assert deps.phone_audit_log_repository is not None
    events = deps.phone_audit_log_repository.list_events(supabase_user_id=_DEMO_USER_ID)
    success = [e for e in events if e.event_type == "phone_verification_requested"]
    assert len(success) == 1
    event = success[0]
    assert event.ip_hash is not None
    assert event.user_agent_hash is not None
    assert event.ip_hash != "testclient"
    assert event.user_agent_hash != _TEST_UA
    assert _EE_PHONE not in f"{event.ip_hash}|{event.user_agent_hash}"
    assert _TEST_UA not in f"{event.ip_hash}|{event.user_agent_hash}"
