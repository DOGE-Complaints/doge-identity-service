"""EPIC-IDS-10 STORY-IDS-PV-07 — Telnyx delivery webhook (offline)."""

from __future__ import annotations

import base64
import json
import re
from datetime import datetime, timezone

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, get_api_dependencies
from core.domain.models import PhoneVerificationSession
from core.security.hashing import hash_secret

_WEBHOOK_PATH = "/webhooks/telnyx/messaging"
_MESSAGE_ID = "telnyx-msg-0001"
_USER_ID = "11111111-1111-1111-1111-111111111111"


@pytest.fixture
def webhook_keys(monkeypatch: pytest.MonkeyPatch) -> tuple[Ed25519PrivateKey, str]:
    private_key = Ed25519PrivateKey.generate()
    public_key = base64.b64encode(private_key.public_key().public_bytes_raw()).decode("ascii")
    monkeypatch.setenv("TELNYX_WEBHOOK_PUBLIC_KEY", public_key)
    _clear_api_dependencies_cache()
    yield private_key, public_key
    _clear_api_dependencies_cache()


@pytest.fixture(autouse=True)
def _reset_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("SMS_PROVIDER", "mock")
    yield
    _clear_api_dependencies_cache()


def _sign_request(
    *,
    body: bytes,
    private_key: Ed25519PrivateKey,
    timestamp: str = "1700000000",
) -> dict[str, str]:
    signed_payload = f"{timestamp}|".encode("utf-8") + body
    signature = private_key.sign(signed_payload)
    return {
        "telnyx-timestamp": timestamp,
        "telnyx-signature-ed25519": base64.b64encode(signature).decode("ascii"),
        "content-type": "application/json",
    }


def _telnyx_payload(*, event_type: str, message_id: str = _MESSAGE_ID) -> dict:
    return {
        "data": {
            "event_type": event_type,
            "occurred_at": "2026-06-11T12:05:00.000000Z",
            "payload": {"id": message_id, "to": [{"status": event_type.split(".")[-1]}]},
        }
    }


def _seed_session(*, message_id: str = _MESSAGE_ID) -> PhoneVerificationSession:
    deps = get_api_dependencies()
    assert deps.phone_verification_session_store is not None
    now = datetime(2026, 6, 11, 12, 0, 0, tzinfo=timezone.utc)
    session = PhoneVerificationSession(
        id="sess-webhook-1",
        supabase_user_id=_USER_ID,
        phone_hash=hash_secret("+37255555555", key="test-key"),
        dial_prefix="+372",
        code_hash="hash",
        status="started",
        attempts=0,
        created_at=now,
        expires_at=now,
        provider="telnyx",
        provider_message_id=message_id,
        delivery_status=None,
        delivery_updated_at=None,
    )
    deps.phone_verification_session_store.create(session)
    return session


def test_valid_signed_webhook_updates_delivery_status(
    test_client: TestClient,
    webhook_keys: tuple[Ed25519PrivateKey, str],
) -> None:
    private_key, _ = webhook_keys
    _seed_session()
    body = json.dumps(_telnyx_payload(event_type="message.sent")).encode("utf-8")
    headers = _sign_request(body=body, private_key=private_key)

    response = test_client.post(_WEBHOOK_PATH, content=body, headers=headers)

    assert response.status_code == 204
    deps = get_api_dependencies()
    session = deps.phone_verification_session_store.get_by_provider_message_id(_MESSAGE_ID)
    assert session is not None
    assert session.delivery_status == "sent"


def test_invalid_signature_rejected_and_session_unchanged(
    test_client: TestClient,
    webhook_keys: tuple[Ed25519PrivateKey, str],
) -> None:
    _seed_session()
    body = json.dumps(_telnyx_payload(event_type="message.sent")).encode("utf-8")

    response = test_client.post(
        _WEBHOOK_PATH,
        content=body,
        headers={
            "telnyx-timestamp": "1700000000",
            "telnyx-signature-ed25519": base64.b64encode(b"bad-signature").decode("ascii"),
            "content-type": "application/json",
        },
    )

    assert response.status_code == 401
    deps = get_api_dependencies()
    session = deps.phone_verification_session_store.get_by_provider_message_id(_MESSAGE_ID)
    assert session is not None
    assert session.delivery_status is None


def test_idempotent_replay_does_not_regress_final_status(
    test_client: TestClient,
    webhook_keys: tuple[Ed25519PrivateKey, str],
) -> None:
    private_key, _ = webhook_keys
    _seed_session()
    delivered_body = json.dumps(_telnyx_payload(event_type="message.delivered")).encode("utf-8")
    sent_body = json.dumps(_telnyx_payload(event_type="message.sent")).encode("utf-8")

    first = test_client.post(
        _WEBHOOK_PATH,
        content=delivered_body,
        headers=_sign_request(body=delivered_body, private_key=private_key, timestamp="1700000001"),
    )
    replay = test_client.post(
        _WEBHOOK_PATH,
        content=sent_body,
        headers=_sign_request(body=sent_body, private_key=private_key, timestamp="1700000002"),
    )

    assert first.status_code == 204
    assert replay.status_code == 204
    deps = get_api_dependencies()
    session = deps.phone_verification_session_store.get_by_provider_message_id(_MESSAGE_ID)
    assert session is not None
    assert session.delivery_status == "delivered"


def test_message_finalized_failed_maps_to_failed(
    test_client: TestClient,
    webhook_keys: tuple[Ed25519PrivateKey, str],
) -> None:
    private_key, _ = webhook_keys
    _seed_session()
    payload = {
        "data": {
            "event_type": "message.finalized",
            "occurred_at": "2026-06-11T12:06:00.000000Z",
            "payload": {
                "id": _MESSAGE_ID,
                "errors": [{"code": "40008", "title": "Undeliverable"}],
            },
        }
    }
    body = json.dumps(payload).encode("utf-8")
    response = test_client.post(
        _WEBHOOK_PATH,
        content=body,
        headers=_sign_request(body=body, private_key=private_key),
    )

    assert response.status_code == 204
    deps = get_api_dependencies()
    session = deps.phone_verification_session_store.get_by_provider_message_id(_MESSAGE_ID)
    assert session is not None
    assert session.delivery_status == "failed"


def test_delivery_audit_logged_without_pii(
    test_client: TestClient,
    webhook_keys: tuple[Ed25519PrivateKey, str],
) -> None:
    private_key, _ = webhook_keys
    _seed_session()
    body = json.dumps(_telnyx_payload(event_type="message.delivered")).encode("utf-8")
    response = test_client.post(
        _WEBHOOK_PATH,
        content=body,
        headers=_sign_request(body=body, private_key=private_key),
    )
    assert response.status_code == 204

    deps = get_api_dependencies()
    assert deps.phone_audit_log_repository is not None
    events = deps.phone_audit_log_repository.list_events(event_type="telnyx_delivery_status_updated")
    assert events
    event = events[-1]
    assert event.success is True
    assert event.provider == "telnyx"
    blob = f"{event.failure_reason}{event.event_type}{event.provider}"
    assert "+372" not in blob
    assert not re.search(r"\b\d{6}\b", blob or "")
