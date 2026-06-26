"""EPIC-IDS-10 STORY-IDS-PV-05 — mock phone verification flow (offline e2e)."""

from __future__ import annotations

import re
import time
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient
from joserfc import jwt
from joserfc.jwk import OctKey

from core.api.asgi_app import _clear_api_dependencies_cache, create_app, get_api_dependencies
from core.config.providers import provide_app_config
from core.phone.base import SmsErrorCode
from core.phone.mock.mock_sender import MockSmsSender

_DEMO_JWT_SECRET = "test-secret-for-demo"
_DEMO_SUPABASE_URL = "https://demo.local"
_DEMO_USER_ID = "11111111-1111-1111-1111-111111111111"
_OTHER_USER_ID = "22222222-2222-2222-2222-222222222222"
_EE_PHONE = "+37255555555"
_US_PHONE = "+15555555555"


@pytest.fixture(autouse=True)
def _reset_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("SMS_PROVIDER", "mock")
    monkeypatch.setenv("PHONE_ALLOWED_DIAL_PREFIXES", "+372")
    monkeypatch.setenv("PHONE_RESEND_COOLDOWN_S", "60")
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


def _mock_sender() -> MockSmsSender:
    deps = get_api_dependencies()
    assert deps.sms_sender_registry is not None
    sender = deps.sms_sender_registry.get_active(deps.config)
    assert isinstance(sender, MockSmsSender)
    return sender


def _extract_code(text: str) -> str:
    match = re.search(r"(\d{6})", text)
    assert match is not None
    return match.group(1)


def _request_phone(test_client: TestClient, *, token: str, phone: str) -> dict:
    response = test_client.post(
        "/auth/phone/request",
        headers={"Authorization": f"Bearer {token}"},
        json={"phone": phone},
    )
    return response


def test_phone_request_creates_session_sends_sms_and_returns_expires_at(
    test_client: TestClient,
) -> None:
    token = _demo_bearer_token()
    response = _request_phone(test_client, token=token, phone=_EE_PHONE)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["sent"] is True
    assert data["expires_at"].endswith("Z")

    deps = get_api_dependencies()
    assert deps.phone_verification_session_store is not None
    session = deps.phone_verification_session_store.get_active_by_user(
        _DEMO_USER_ID,
        now=datetime.now(timezone.utc),
    )
    assert session is not None
    assert session.status == "started"
    assert session.provider_message_id is not None
    assert session.provider_message_id.startswith("mock-")

    sender = _mock_sender()
    assert len(sender.sent_messages) == 1
    assert sender.sent_messages[0][0] == _EE_PHONE

    assert deps.phone_audit_log_repository is not None
    events = deps.phone_audit_log_repository.list_events(
        supabase_user_id=_DEMO_USER_ID,
        event_type="phone_verification_requested",
    )
    assert len(events) == 1
    assert events[0].success is True
    assert events[0].failure_reason is None
    for event in deps.phone_audit_log_repository.list_events(supabase_user_id=_DEMO_USER_ID):
        blob = f"{event.failure_reason}{event.event_type}{event.provider}"
        assert _EE_PHONE not in blob
        assert not re.search(r"\b\d{6}\b", blob or "")


def test_phone_request_country_not_allowed(test_client: TestClient) -> None:
    token = _demo_bearer_token()
    response = _request_phone(test_client, token=token, phone=_US_PHONE)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == SmsErrorCode.COUNTRY_NOT_ALLOWED.value


def test_phone_request_rate_limited_before_cooldown(test_client: TestClient) -> None:
    token = _demo_bearer_token()
    first = _request_phone(test_client, token=token, phone=_EE_PHONE)
    assert first.status_code == 200

    second = _request_phone(test_client, token=token, phone=_EE_PHONE)
    assert second.status_code == 400
    assert second.json()["error"]["code"] == SmsErrorCode.RATE_LIMITED.value


def test_phone_request_after_cooldown_invalidates_previous_code(
    test_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PHONE_RESEND_COOLDOWN_S", "0")
    _clear_api_dependencies_cache()

    token = _demo_bearer_token()
    first = _request_phone(test_client, token=token, phone=_EE_PHONE)
    assert first.status_code == 200
    first_code = _extract_code(_mock_sender().sent_messages[-1][1])

    second = _request_phone(test_client, token=token, phone=_EE_PHONE)
    assert second.status_code == 200

    confirm_old = test_client.post(
        "/auth/phone/confirm",
        headers={"Authorization": f"Bearer {token}"},
        json={"phone": _EE_PHONE, "code": first_code},
    )
    assert confirm_old.status_code == 400
    assert confirm_old.json()["error"]["code"] == SmsErrorCode.CODE_MISMATCH.value


def test_phone_confirm_full_flow_sets_phone_verified(test_client: TestClient) -> None:
    token = _demo_bearer_token()
    request = _request_phone(test_client, token=token, phone=_EE_PHONE)
    assert request.status_code == 200

    code = _extract_code(_mock_sender().sent_messages[-1][1])
    confirm = test_client.post(
        "/auth/phone/confirm",
        headers={"Authorization": f"Bearer {token}"},
        json={"phone": _EE_PHONE, "code": code},
    )
    assert confirm.status_code == 200
    assert confirm.json()["data"]["status"] == "verified"

    me = test_client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    data = me.json()["data"]
    assert data["phone_verified"] is True
    assert data["phone_verified_at"]
    assert data["phone_provider"] == "mock"
    assert data["phone_dial_prefix"] == "+372"


def test_phone_confirm_wrong_code_returns_code_mismatch(test_client: TestClient) -> None:
    token = _demo_bearer_token()
    assert _request_phone(test_client, token=token, phone=_EE_PHONE).status_code == 200

    confirm = test_client.post(
        "/auth/phone/confirm",
        headers={"Authorization": f"Bearer {token}"},
        json={"phone": _EE_PHONE, "code": "000000"},
    )
    assert confirm.status_code == 400
    assert confirm.json()["error"]["code"] == SmsErrorCode.CODE_MISMATCH.value


def test_phone_confirm_expired_code(test_client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PHONE_CODE_TTL_S", "1")
    _clear_api_dependencies_cache()

    token = _demo_bearer_token()
    assert _request_phone(test_client, token=token, phone=_EE_PHONE).status_code == 200
    code = _extract_code(_mock_sender().sent_messages[-1][1])

    time.sleep(1.1)

    confirm = test_client.post(
        "/auth/phone/confirm",
        headers={"Authorization": f"Bearer {token}"},
        json={"phone": _EE_PHONE, "code": code},
    )
    assert confirm.status_code == 400
    assert confirm.json()["error"]["code"] == SmsErrorCode.CODE_EXPIRED.value


def test_phone_confirm_too_many_attempts(
    test_client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PHONE_MAX_ATTEMPTS", "2")
    _clear_api_dependencies_cache()

    token = _demo_bearer_token()
    assert _request_phone(test_client, token=token, phone=_EE_PHONE).status_code == 200

    for _ in range(2):
        response = test_client.post(
            "/auth/phone/confirm",
            headers={"Authorization": f"Bearer {token}"},
            json={"phone": _EE_PHONE, "code": "000000"},
        )
        assert response.status_code == 400

    final = test_client.post(
        "/auth/phone/confirm",
        headers={"Authorization": f"Bearer {token}"},
        json={"phone": _EE_PHONE, "code": "000000"},
    )
    assert final.status_code == 400
    assert final.json()["error"]["code"] == SmsErrorCode.TOO_MANY_ATTEMPTS.value


def test_phone_confirm_duplicate_number_returns_409(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PHONE_RESEND_COOLDOWN_S", "0")
    _clear_api_dependencies_cache()
    app = create_app(provide_app_config())
    with TestClient(app) as test_client:
        first_token = _demo_bearer_token(sub=_DEMO_USER_ID)
        assert _request_phone(test_client, token=first_token, phone=_EE_PHONE).status_code == 200
        first_code = _extract_code(_mock_sender().sent_messages[-1][1])
        assert (
            test_client.post(
                "/auth/phone/confirm",
                headers={"Authorization": f"Bearer {first_token}"},
                json={"phone": _EE_PHONE, "code": first_code},
            ).status_code
            == 200
        )

        second_token = _demo_bearer_token(sub=_OTHER_USER_ID)
        assert _request_phone(test_client, token=second_token, phone=_EE_PHONE).status_code == 200
        second_code = _extract_code(_mock_sender().sent_messages[-1][1])
        conflict = test_client.post(
            "/auth/phone/confirm",
            headers={"Authorization": f"Bearer {second_token}"},
            json={"phone": _EE_PHONE, "code": second_code},
        )
        assert conflict.status_code == 409
        assert conflict.json()["error"]["code"] == "profile_conflict"


def test_phone_audit_events_contain_no_pii(test_client: TestClient) -> None:
    token = _demo_bearer_token()
    request = _request_phone(test_client, token=token, phone=_EE_PHONE)
    code = _extract_code(_mock_sender().sent_messages[-1][1])

    test_client.post(
        "/auth/phone/confirm",
        headers={"Authorization": f"Bearer {token}"},
        json={"phone": _EE_PHONE, "code": "000000"},
    )
    test_client.post(
        "/auth/phone/confirm",
        headers={"Authorization": f"Bearer {token}"},
        json={"phone": _EE_PHONE, "code": code},
    )

    deps = get_api_dependencies()
    assert deps.phone_audit_log_repository is not None
    for event in deps.phone_audit_log_repository.list_events(supabase_user_id=_DEMO_USER_ID):
        serialized = (
            f"{event.event_type}|{event.provider}|{event.failure_reason}|"
            f"{event.request_id}|{event.success}|{event.ip_hash}|{event.user_agent_hash}"
        )
        assert _EE_PHONE not in serialized
        assert code not in serialized
        if event.event_type == "phone_verification_requested":
            assert event.ip_hash is not None
            assert event.user_agent_hash is not None
            assert "testclient" not in serialized
