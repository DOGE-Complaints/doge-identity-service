"""EPIC-IDS-10 STORY-IDS-PV-06 — Telnyx SMS sender (offline + optional live)."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import httpx
import pytest

from core.config import ConfigError, provide_app_config
from core.phone.base import SmsErrorCode, SmsSenderError
from core.phone.registry_builder import build_sms_registry, registered_sms_provider_names
from core.phone.runtime_factory import build_sms_provider_runtime
from core.phone.telnyx.config import TelnyxSettings, validate_telnyx_config
from core.phone.telnyx.sender import TelnyxSmsSender

_API_BASE = "https://api.telnyx.com"
_MESSAGES_URL = f"{_API_BASE}/v2/messages"


def _telnyx_settings(**overrides: str) -> TelnyxSettings:
    env = {
        "TELNYX_API_KEY": "KEY_test",
        "TELNYX_API_BASE_URL": _API_BASE,
        "TELNYX_FROM": "DOGEstonia",
        "TELNYX_MESSAGING_PROFILE_ID": "profile-uuid",
        "TELNYX_MESSAGE_TYPE": "SMS",
        "TELNYX_ENCODING": "auto",
    }
    env.update(overrides)
    validate_telnyx_config(env)
    return TelnyxSettings.load(env)


def _success_payload(*, message_id: str = "msg-123", status: str = "queued") -> dict[str, object]:
    return {
        "data": {
            "id": message_id,
            "to": [{"status": status}],
            "errors": [],
        }
    }


def _error_payload(*, code: str, title: str = "Error", detail: str = "detail") -> dict[str, object]:
    return {
        "errors": [
            {
                "code": code,
                "title": title,
                "detail": detail,
            }
        ]
    }


class _MockTelnyxTransport:
    def __init__(self, handler) -> None:
        self._handler = handler
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return self._handler(request)


def _sender_with_transport(transport: _MockTelnyxTransport) -> TelnyxSmsSender:
    client = httpx.Client(transport=httpx.MockTransport(transport))
    return TelnyxSmsSender(settings=_telnyx_settings(), http_client=client)


def test_registered_sms_provider_names_includes_telnyx() -> None:
    assert "telnyx" in registered_sms_provider_names()


def test_telnyx_config_requires_api_key() -> None:
    with pytest.raises(ConfigError, match="TELNYX_API_KEY"):
        validate_telnyx_config({"TELNYX_FROM": "DOGEstonia"})


def test_telnyx_alphanumeric_from_requires_profile_id() -> None:
    with pytest.raises(ConfigError, match="TELNYX_MESSAGING_PROFILE_ID"):
        validate_telnyx_config(
            {
                "TELNYX_API_KEY": "KEY_test",
                "TELNYX_FROM": "DOGEstonia",
            }
        )


def test_telnyx_e164_from_does_not_require_profile_id() -> None:
    settings = _telnyx_settings(TELNYX_FROM="+37255555555", TELNYX_MESSAGING_PROFILE_ID="")
    assert settings.from_sender == "+37255555555"


def test_build_sms_registry_active_telnyx(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Telnyx creds only in cwd ``.env`` — no ``patch.dict(os.environ)``."""
    monkeypatch.chdir(tmp_path)
    for key in ("TELNYX_API_KEY", "TELNYX_MESSAGING_PROFILE_ID", "SMS_PROVIDER"):
        monkeypatch.delenv(key, raising=False)
    (tmp_path / ".env").write_text(
        "SMS_PROVIDER=telnyx\n"
        "TELNYX_API_KEY=KEY_test\n"
        "TELNYX_MESSAGING_PROFILE_ID=profile-uuid\n"
    )
    config = provide_app_config()
    runtime = build_sms_provider_runtime(config=config)
    registry = build_sms_registry(runtime)
    sender = registry.get_active(config)
    assert isinstance(sender, TelnyxSmsSender)


def test_telnyx_send_success_queued() -> None:
    transport = _MockTelnyxTransport(
        lambda request: httpx.Response(200, json=_success_payload(message_id="msg-queued"))
    )
    sender = _sender_with_transport(transport)

    result = sender.send(to_e164="+37251234567", text="Your code is 123456")

    assert result.accepted is True
    assert result.provider_message_id == "msg-queued"
    assert len(transport.requests) == 1
    request = transport.requests[0]
    assert request.method == "POST"
    assert str(request.url) == _MESSAGES_URL
    assert request.headers["Authorization"] == "Bearer KEY_test"
    body = json.loads(request.content.decode())
    assert body["from"] == "DOGEstonia"
    assert body["to"] == "+37251234567"
    assert body["text"] == "Your code is 123456"
    assert body["type"] == "SMS"
    assert body["messaging_profile_id"] == "profile-uuid"


def test_telnyx_send_maps_country_not_allowed() -> None:
    transport = _MockTelnyxTransport(
        lambda _: httpx.Response(403, json=_error_payload(code="40309"))
    )
    sender = _sender_with_transport(transport)

    with pytest.raises(SmsSenderError) as exc_info:
        sender.send(to_e164="+37251234567", text="code")

    assert exc_info.value.code == SmsErrorCode.COUNTRY_NOT_ALLOWED


def test_telnyx_send_maps_rate_limited() -> None:
    transport = _MockTelnyxTransport(
        lambda _: httpx.Response(429, json=_error_payload(code="10011"))
    )
    sender = _sender_with_transport(transport)

    with pytest.raises(SmsSenderError) as exc_info:
        sender.send(to_e164="+37251234567", text="code")

    assert exc_info.value.code == SmsErrorCode.RATE_LIMITED


def test_telnyx_send_maps_provider_unavailable_on_5xx() -> None:
    transport = _MockTelnyxTransport(lambda _: httpx.Response(503, json=_error_payload(code="99999")))
    sender = _sender_with_transport(transport)

    with pytest.raises(SmsSenderError) as exc_info:
        sender.send(to_e164="+37251234567", text="code")

    assert exc_info.value.code == SmsErrorCode.PROVIDER_UNAVAILABLE


def test_telnyx_send_maps_invalid_phone() -> None:
    transport = _MockTelnyxTransport(
        lambda _: httpx.Response(400, json=_error_payload(code="40310"))
    )
    sender = _sender_with_transport(transport)

    with pytest.raises(SmsSenderError) as exc_info:
        sender.send(to_e164="+37251234567", text="code")

    assert exc_info.value.code == SmsErrorCode.INVALID_PHONE


def test_telnyx_send_maps_send_failed() -> None:
    transport = _MockTelnyxTransport(
        lambda _: httpx.Response(400, json=_error_payload(code="40305"))
    )
    sender = _sender_with_transport(transport)

    with pytest.raises(SmsSenderError) as exc_info:
        sender.send(to_e164="+37251234567", text="code")

    assert exc_info.value.code == SmsErrorCode.SEND_FAILED


def test_telnyx_send_missing_data_id_maps_unknown() -> None:
    transport = _MockTelnyxTransport(
        lambda _: httpx.Response(200, json={"data": {"to": [{"status": "queued"}]}})
    )
    sender = _sender_with_transport(transport)

    with pytest.raises(SmsSenderError) as exc_info:
        sender.send(to_e164="+37251234567", text="code")

    assert exc_info.value.code == SmsErrorCode.UNKNOWN


def test_telnyx_send_parses_errors_array_fields() -> None:
    transport = _MockTelnyxTransport(
        lambda _: httpx.Response(
            400,
            json={
                "errors": [
                    {
                        "code": "40318",
                        "title": "Queue full",
                        "detail": "Try again later",
                    }
                ]
            },
        )
    )
    sender = _sender_with_transport(transport)

    with pytest.raises(SmsSenderError) as exc_info:
        sender.send(to_e164="+37251234567", text="code")

    assert exc_info.value.code == SmsErrorCode.RATE_LIMITED


def test_telnyx_send_does_not_log_otp_text(caplog: pytest.LogCaptureFixture) -> None:
    transport = _MockTelnyxTransport(
        lambda _: httpx.Response(400, json=_error_payload(code="40305"))
    )
    sender = _sender_with_transport(transport)
    otp_text = "Your DOGEstonia verification code is 654321"

    with caplog.at_level(logging.WARNING, logger="core.phone.telnyx.errors"):
        with pytest.raises(SmsSenderError):
            sender.send(to_e164="+37251234567", text=otp_text)

    joined = " ".join(caplog.messages)
    assert "654321" not in joined
    assert "+37251234567" not in joined


@pytest.mark.live_integration
def test_telnyx_live_send_skips_without_credentials() -> None:
    if not os.environ.get("TELNYX_API_KEY"):
        pytest.skip("TELNYX_API_KEY not set")
    if not os.environ.get("TELNYX_MESSAGING_PROFILE_ID"):
        pytest.skip("TELNYX_MESSAGING_PROFILE_ID not set")
