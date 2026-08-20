"""EPIC-IDS-14 STORY-IDS-SMSPM-02 — SMSPM SMS sender (offline + optional live)."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

import httpx
import pytest

from core.config import provide_app_config
from core.phone.base import SmsErrorCode, SmsSenderError
from core.phone.registry_builder import build_sms_registry, registered_sms_provider_names
from core.phone.runtime_factory import build_sms_provider_runtime
from core.phone.smspm.config import SmspmSettings, validate_smspm_config
from core.phone.smspm.sender import SmspmSmsSender

_API_BASE = "https://api.smspm.com"


def _smspm_settings(**overrides: str) -> SmspmSettings:
    env = {
        "SMSPM_HASH": "hash-test",
        "SMSPM_TOKEN": "token-test",
        "SMSPM_FROM": "DOGEstonia",
        "SMSPM_API_BASE_URL": _API_BASE,
    }
    env.update(overrides)
    validate_smspm_config(env)
    return SmspmSettings.load(env)


def _success_payload(*, message_id: str = "msg-123", to_number: str = "37251234567") -> dict[str, object]:
    return {
        "messages": [
            {
                "id": message_id,
                "toNumber": to_number,
                "status": "Added to queue",
            }
        ]
    }


def _error_payload(*, error: str) -> dict[str, object]:
    return {"error": error}


class _MockSmspmTransport:
    def __init__(self, handler) -> None:
        self._handler = handler
        self.requests: list[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return self._handler(request)


def _sender_with_transport(
    transport: _MockSmspmTransport,
    *,
    settings: SmspmSettings | None = None,
) -> SmspmSmsSender:
    client = httpx.Client(transport=httpx.MockTransport(transport))
    return SmspmSmsSender(settings=settings or _smspm_settings(), http_client=client)


def test_registered_sms_provider_names_includes_smspm() -> None:
    assert "smspm" in registered_sms_provider_names()


def test_build_sms_registry_active_smspm(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.chdir(tmp_path)
    for key in ("SMSPM_HASH", "SMSPM_TOKEN", "SMSPM_FROM", "SMS_PROVIDER"):
        monkeypatch.delenv(key, raising=False)
    (tmp_path / ".env").write_text(
        "SMS_PROVIDER=smspm\n"
        "SMSPM_HASH=hash-test\n"
        "SMSPM_TOKEN=token-test\n"
        "SMSPM_FROM=DOGEstonia\n"
    )
    config = provide_app_config()
    runtime = build_sms_provider_runtime(config=config)
    try:
        registry = build_sms_registry(runtime)
        sender = registry.get_active(config)
        assert isinstance(sender, SmspmSmsSender)
        assert sender.provider_name == "smspm"
    finally:
        if runtime.http_client is not None:
            runtime.http_client.close()


def test_smspm_send_success_queued() -> None:
    transport = _MockSmspmTransport(
        lambda request: httpx.Response(200, json=_success_payload(message_id="msg-queued"))
    )
    sender = _sender_with_transport(transport)

    result = sender.send(to_e164="+37251234567", text="Your code is 123456")

    assert result.accepted is True
    assert result.provider_message_id == "msg-queued"
    assert len(transport.requests) == 1
    request = transport.requests[0]
    assert request.method == "POST"
    assert str(request.url) == _API_BASE
    assert "Authorization" not in request.headers
    assert "Bearer" not in request.headers.get("Authorization", "")
    body = json.loads(request.content.decode())
    assert body["hash"] == "hash-test"
    assert body["token"] == "token-test"
    assert body["toNumber"] == "37251234567"
    assert body["fromNumber"] == "DOGEstonia"
    assert body["text"] == "Your code is 123456"
    assert "report" not in body
    assert "smsId" not in body


def test_smspm_send_optional_sms_id() -> None:
    transport = _MockSmspmTransport(
        lambda _: httpx.Response(200, json=_success_payload(message_id="msg-smsid"))
    )
    sender = _sender_with_transport(transport)

    result = sender.send(to_e164="+37251234567", text="code", sms_id="session-uuid")

    assert result.accepted is True
    body = json.loads(transport.requests[0].content.decode())
    assert body["smsId"] == "session-uuid"
    assert "report" not in body


def test_smspm_send_maps_401_to_send_failed() -> None:
    transport = _MockSmspmTransport(
        lambda _: httpx.Response(401, json=_error_payload(error="Unauthorized"))
    )
    sender = _sender_with_transport(transport)

    with pytest.raises(SmsSenderError) as exc_info:
        sender.send(to_e164="+37251234567", text="code")

    assert exc_info.value.code == SmsErrorCode.SEND_FAILED


def test_smspm_send_maps_invalid_phone() -> None:
    transport = _MockSmspmTransport(
        lambda _: httpx.Response(400, json=_error_payload(error="Invalid phone number: 123"))
    )
    sender = _sender_with_transport(transport)

    with pytest.raises(SmsSenderError) as exc_info:
        sender.send(to_e164="+37251234567", text="code")

    assert exc_info.value.code == SmsErrorCode.INVALID_PHONE


def test_smspm_send_maps_provider_unavailable_on_5xx() -> None:
    transport = _MockSmspmTransport(
        lambda _: httpx.Response(500, json=_error_payload(error="Internal server error"))
    )
    sender = _sender_with_transport(transport)

    with pytest.raises(SmsSenderError) as exc_info:
        sender.send(to_e164="+37251234567", text="code")

    assert exc_info.value.code == SmsErrorCode.PROVIDER_UNAVAILABLE


def test_smspm_send_maps_timeout_to_provider_unavailable() -> None:
    def _raise_timeout(_request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("timed out")

    transport = _MockSmspmTransport(_raise_timeout)
    sender = _sender_with_transport(transport)

    with pytest.raises(SmsSenderError) as exc_info:
        sender.send(to_e164="+37251234567", text="code")

    assert exc_info.value.code == SmsErrorCode.PROVIDER_UNAVAILABLE


def test_smspm_send_maps_other_4xx_to_send_failed() -> None:
    transport = _MockSmspmTransport(
        lambda _: httpx.Response(400, json=_error_payload(error="Hash is required"))
    )
    sender = _sender_with_transport(transport)

    with pytest.raises(SmsSenderError) as exc_info:
        sender.send(to_e164="+37251234567", text="code")

    assert exc_info.value.code == SmsErrorCode.SEND_FAILED


def test_smspm_send_missing_message_id_maps_unknown() -> None:
    transport = _MockSmspmTransport(
        lambda _: httpx.Response(
            200,
            json={"messages": [{"toNumber": "37251234567", "status": "Added to queue"}]},
        )
    )
    sender = _sender_with_transport(transport)

    with pytest.raises(SmsSenderError) as exc_info:
        sender.send(to_e164="+37251234567", text="code")

    assert exc_info.value.code == SmsErrorCode.UNKNOWN


def test_smspm_send_does_not_log_secrets_otp_or_msisdn(caplog: pytest.LogCaptureFixture) -> None:
    settings = _smspm_settings(SMSPM_HASH="secret-hash-xyz", SMSPM_TOKEN="secret-token-xyz")
    transport = _MockSmspmTransport(
        lambda _: httpx.Response(
            400,
            json=_error_payload(error="Invalid phone number: 37251234567"),
        )
    )
    sender = _sender_with_transport(transport, settings=settings)
    otp_text = "Your DOGEstonia verification code is 654321"

    with caplog.at_level(logging.WARNING, logger="core.phone.smspm.errors"):
        with pytest.raises(SmsSenderError):
            sender.send(to_e164="+37251234567", text=otp_text)

    joined = " ".join(caplog.messages)
    assert "secret-hash-xyz" not in joined
    assert "secret-token-xyz" not in joined
    assert "654321" not in joined
    assert "+37251234567" not in joined
    assert "37251234567" not in joined


@pytest.mark.live_integration
def test_smspm_live_send_skips_without_credentials() -> None:
    if not os.environ.get("SMSPM_HASH"):
        pytest.skip("SMSPM_HASH not set")
    if not os.environ.get("SMSPM_TOKEN"):
        pytest.skip("SMSPM_TOKEN not set")
    if not os.environ.get("SMSPM_FROM"):
        pytest.skip("SMSPM_FROM not set")
