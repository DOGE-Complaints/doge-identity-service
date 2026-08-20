"""EPIC-IDS-14 STORY-IDS-SMSPM-04 — SMSPM delivery webhook (offline)."""

from __future__ import annotations

import dataclasses
import re
from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, get_api_dependencies
from core.domain.models import PhoneVerificationSession
from core.phone.mock.mock_sender import MockSmsSender
from core.security.hashing import hash_secret
from tests.supabase_jwt_harness import DEFAULT_USER_ID, mint_supabase_access_token

_WEBHOOK_SECRET = "smspm-test-shared-secret"
_WEBHOOK_PATH = f"/webhooks/smspm/delivery/{_WEBHOOK_SECRET}"
_MESSAGE_ID = "smspm-msg-0001"
_USER_ID = DEFAULT_USER_ID
_EE_PHONE = "+37255555555"


@pytest.fixture
def webhook_secret(monkeypatch: pytest.MonkeyPatch) -> str:
    monkeypatch.setenv("SMSPM_WEBHOOK_SHARED_SECRET", _WEBHOOK_SECRET)
    _clear_api_dependencies_cache()
    yield _WEBHOOK_SECRET
    _clear_api_dependencies_cache()


@pytest.fixture(autouse=True)
def _reset_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("SMS_PROVIDER", "mock")
    monkeypatch.setenv("PHONE_ALLOWED_DIAL_PREFIXES", "+372")
    yield
    _clear_api_dependencies_cache()


def _seed_session(*, message_id: str = _MESSAGE_ID) -> PhoneVerificationSession:
    deps = get_api_dependencies()
    assert deps.phone_verification_session_store is not None
    now = datetime(2026, 8, 20, 12, 0, 0, tzinfo=timezone.utc)
    session = PhoneVerificationSession(
        id="sess-smspm-webhook-1",
        supabase_user_id=_USER_ID,
        phone_hash=hash_secret(_EE_PHONE, key="test-key"),
        dial_prefix="+372",
        code_hash="hash",
        status="started",
        attempts=0,
        created_at=now,
        expires_at=now,
        provider="smspm",
        provider_message_id=message_id,
        delivery_status=None,
        delivery_updated_at=None,
    )
    deps.phone_verification_session_store.create(session)
    return session


def test_valid_secret_updates_delivery_status(
    test_client: TestClient,
    webhook_secret: str,
) -> None:
    del webhook_secret
    _seed_session()

    response = test_client.get(
        _WEBHOOK_PATH,
        params={"id": _MESSAGE_ID, "status": "delivered", "toNumber": "37255555555"},
    )

    assert response.status_code == 200
    assert response.text == "OK"
    assert response.headers["content-type"].startswith("text/plain")
    deps = get_api_dependencies()
    session = deps.phone_verification_session_store.get_by_provider_message_id(_MESSAGE_ID)
    assert session is not None
    assert session.delivery_status == "delivered"


def test_bad_secret_returns_401_and_session_unchanged(
    test_client: TestClient,
    webhook_secret: str,
) -> None:
    del webhook_secret
    _seed_session()

    response = test_client.get(
        "/webhooks/smspm/delivery/wrong-secret",
        params={"id": _MESSAGE_ID, "status": "delivered", "toNumber": "37255555555"},
    )

    assert response.status_code == 401
    deps = get_api_dependencies()
    session = deps.phone_verification_session_store.get_by_provider_message_id(_MESSAGE_ID)
    assert session is not None
    assert session.delivery_status is None


def test_missing_secret_config_returns_503(test_client: TestClient) -> None:
    response = test_client.get(
        _WEBHOOK_PATH,
        params={"id": _MESSAGE_ID, "status": "delivered"},
    )
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "CONFIG_ERROR"


def test_idempotent_replay_does_not_regress_final_status(
    test_client: TestClient,
    webhook_secret: str,
) -> None:
    del webhook_secret
    _seed_session()

    first = test_client.get(
        _WEBHOOK_PATH,
        params={"id": _MESSAGE_ID, "status": "delivered"},
    )
    replay = test_client.get(
        _WEBHOOK_PATH,
        params={"id": _MESSAGE_ID, "status": "submitted"},
    )

    assert first.status_code == 200
    assert first.text == "OK"
    assert replay.status_code == 200
    assert replay.text == "OK"
    deps = get_api_dependencies()
    session = deps.phone_verification_session_store.get_by_provider_message_id(_MESSAGE_ID)
    assert session is not None
    assert session.delivery_status == "delivered"


def test_submitted_maps_to_sent(
    test_client: TestClient,
    webhook_secret: str,
) -> None:
    del webhook_secret
    _seed_session()
    response = test_client.get(
        _WEBHOOK_PATH,
        params={"id": _MESSAGE_ID, "status": "submitted"},
    )
    assert response.status_code == 200
    deps = get_api_dependencies()
    session = deps.phone_verification_session_store.get_by_provider_message_id(_MESSAGE_ID)
    assert session is not None
    assert session.delivery_status == "sent"


def test_delivery_audit_logged_without_pii(
    test_client: TestClient,
    webhook_secret: str,
) -> None:
    del webhook_secret
    _seed_session()
    response = test_client.get(
        _WEBHOOK_PATH,
        params={"id": _MESSAGE_ID, "status": "delivered", "toNumber": "37255555555"},
    )
    assert response.status_code == 200

    deps = get_api_dependencies()
    assert deps.phone_audit_log_repository is not None
    events = deps.phone_audit_log_repository.list_events(event_type="smspm_delivery_status_updated")
    assert events
    event = events[-1]
    assert event.success is True
    assert event.provider == "smspm"
    blob = f"{event.failure_reason}{event.event_type}{event.provider}{event.request_id}"
    assert "+372" not in blob
    assert "37255555555" not in blob
    assert "toNumber" not in blob
    assert not re.search(r"\b\d{6}\b", blob or "")


def test_confirm_succeeds_when_delivery_status_failed(test_client: TestClient) -> None:
    token = mint_supabase_access_token()
    request = test_client.post(
        "/auth/phone/request",
        headers={"Authorization": f"Bearer {token}"},
        json={"phone": _EE_PHONE},
    )
    assert request.status_code == 200

    deps = get_api_dependencies()
    assert deps.sms_sender_registry is not None
    sender = deps.sms_sender_registry.get_active(deps.config)
    assert isinstance(sender, MockSmsSender)
    match = re.search(r"(\d{6})", sender.sent_messages[-1][1])
    assert match is not None
    code = match.group(1)

    store = deps.phone_verification_session_store
    assert store is not None
    session = store.get_active_by_user(_USER_ID, now=datetime.now(timezone.utc))
    assert session is not None
    store.replace(dataclasses.replace(session, delivery_status="failed"))

    confirm = test_client.post(
        "/auth/phone/confirm",
        headers={"Authorization": f"Bearer {token}"},
        json={"phone": _EE_PHONE, "code": code},
    )
    assert confirm.status_code == 200
    assert confirm.json()["data"]["status"] == "verified"
