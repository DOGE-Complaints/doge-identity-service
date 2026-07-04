"""EPIC-IDS-12 STORY-IDS-SEC-01 — HTTP rate limiting (offline)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache
from core.phone.telnyx.errors import SmsErrorCode
from tests.supabase_jwt_harness import DEFAULT_USER_ID, mint_supabase_access_token
from tests.test_phone_verification_flow import _EE_PHONE, _request_phone

_DEMO_USER_ID = DEFAULT_USER_ID
_RETURN_URL = "https://dogestonia.ee/verify"


@pytest.fixture(autouse=True)
def _rate_limit_env(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("ALLOWED_RETURN_URLS", _RETURN_URL)
    monkeypatch.setenv("RATE_LIMIT_EID_START_REQUESTS", "2")
    monkeypatch.setenv("RATE_LIMIT_EID_START_WINDOW_S", "600")
    monkeypatch.setenv("RATE_LIMIT_CALLBACK_REQUESTS", "2")
    monkeypatch.setenv("RATE_LIMIT_CALLBACK_WINDOW_S", "600")
    monkeypatch.setenv("RATE_LIMIT_PHONE_REQUEST_REQUESTS", "10")
    monkeypatch.setenv("RATE_LIMIT_PHONE_REQUEST_WINDOW_S", "600")
    yield
    _clear_api_dependencies_cache()


def _eid_start_payload() -> dict[str, str]:
    return {
        "return_url": _RETURN_URL,
        "return_context": "dashboard_verification",
        "requested_action": "eid:verify",
    }


def _post_eid_start(test_client: TestClient, *, token: str | None = None) -> object:
    headers = {"Authorization": f"Bearer {token or mint_supabase_access_token()}"}
    return test_client.post(
        "/auth/eid/start",
        headers=headers,
        json=_eid_start_payload(),
    )


def test_eid_start_rate_limit_returns_429_with_retry_after(
    test_client: TestClient,
) -> None:
    assert _post_eid_start(test_client).status_code == 200
    assert _post_eid_start(test_client).status_code == 200

    limited = _post_eid_start(test_client)
    assert limited.status_code == 429
    assert limited.headers.get("retry-after") is not None
    body = limited.json()
    assert body["error"]["code"] == "rate_limit_exceeded"
    assert isinstance(body["error"]["retry_after"], int)
    assert body["error"]["retry_after"] >= 1


def test_callback_rate_limit_per_ip_returns_429(test_client: TestClient) -> None:
    unknown_session = "00000000-0000-0000-0000-000000000000"
    path = f"/auth/mock/callback?session_id={unknown_session}"

    assert test_client.get(path).status_code == 400
    assert test_client.get(path).status_code == 400

    limited = test_client.get(path)
    assert limited.status_code == 429
    assert limited.json()["error"]["code"] == "rate_limit_exceeded"
    assert "retry_after" in limited.json()["error"]


def test_callback_rate_limit_ignores_spoofed_x_forwarded_for(
    test_client: TestClient,
) -> None:
    unknown_session = "00000000-0000-0000-0000-000000000000"
    path = f"/auth/mock/callback?session_id={unknown_session}"

    assert test_client.get(path, headers={"X-Forwarded-For": "1.1.1.1"}).status_code == 400
    assert test_client.get(path, headers={"X-Forwarded-For": "2.2.2.2"}).status_code == 400

    limited = test_client.get(path, headers={"X-Forwarded-For": "3.3.3.3"})
    assert limited.status_code == 429
    assert limited.json()["error"]["code"] == "rate_limit_exceeded"


def test_phone_otp_cooldown_still_domain_400_not_http_429(
    test_client: TestClient,
) -> None:
    token = mint_supabase_access_token()
    assert _request_phone(test_client, token=token, phone=_EE_PHONE).status_code == 200

    second = _request_phone(test_client, token=token, phone=_EE_PHONE)
    assert second.status_code == 400
    assert second.json()["error"]["code"] == SmsErrorCode.RATE_LIMITED.value
    assert "retry_after" not in second.json()["error"]


def test_phone_request_rate_limit_returns_429_with_retry_after(
    test_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("RATE_LIMIT_PHONE_REQUEST_REQUESTS", "2")
    monkeypatch.setenv("RATE_LIMIT_PHONE_REQUEST_WINDOW_S", "600")
    monkeypatch.setenv("PHONE_RESEND_COOLDOWN_S", "0")

    token = mint_supabase_access_token()
    phones = ("+37255555556", "+37255555557", "+37255555558")

    assert _request_phone(test_client, token=token, phone=phones[0]).status_code == 200
    assert _request_phone(test_client, token=token, phone=phones[1]).status_code == 200

    limited = _request_phone(test_client, token=token, phone=phones[2])
    assert limited.status_code == 429
    assert limited.headers.get("retry-after") is not None
    body = limited.json()
    assert body["error"]["code"] == "rate_limit_exceeded"
    assert isinstance(body["error"]["retry_after"], int)
    assert body["error"]["retry_after"] >= 1
