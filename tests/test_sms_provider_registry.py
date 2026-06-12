"""EPIC-IDS-10 STORY-IDS-PV-01 — SMS provider registry + mock sender (offline)."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from core.config.providers import provide_app_config
from core.phone.descriptor import SmsProviderNotRegisteredError
from core.phone.mock.mock_sender import MockSmsSender
from core.phone.registry import SmsSenderRegistry
from core.phone.registry_builder import build_sms_registry, registered_sms_provider_names
from core.phone.runtime import SmsProviderRuntime


def _runtime() -> SmsProviderRuntime:
    return SmsProviderRuntime(config=provide_app_config(), http_client=None, settings={})


def test_registered_sms_provider_names_includes_mock() -> None:
    assert "mock" in registered_sms_provider_names()


def test_build_sms_registry_registers_mock() -> None:
    registry = build_sms_registry(_runtime())
    assert "mock" in registry.registered_names
    assert isinstance(registry.get("mock"), MockSmsSender)


def test_get_unknown_provider_raises_guard_error() -> None:
    registry = SmsSenderRegistry({"mock": MockSmsSender()})
    with pytest.raises(SmsProviderNotRegisteredError, match="доступны: mock"):
        registry.get("unknown")


def test_get_active_unknown_provider_raises_guard_error() -> None:
    registry = build_sms_registry(_runtime())
    config = SimpleNamespace(sms_provider="unknown")
    with pytest.raises(SmsProviderNotRegisteredError, match="доступны: mock"):
        registry.get_active(config)


def test_mock_send_accepts_and_captures_message() -> None:
    sender = MockSmsSender()
    result = sender.send(to_e164="+37255555555", text="123456")
    assert result.accepted is True
    assert result.provider_message_id is not None
    assert result.provider_message_id.startswith("mock-")
    assert sender.sent_messages == [("+37255555555", "123456")]


def test_build_sms_registry_mock_send_via_registry() -> None:
    registry = build_sms_registry(_runtime())
    result = registry.get("mock").send(to_e164="+37255555555", text="654321")
    assert result.accepted is True
    mock = registry.get("mock")
    assert isinstance(mock, MockSmsSender)
    assert mock.sent_messages == [("+37255555555", "654321")]
