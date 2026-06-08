"""STORY-IDS-EID-03 — provider plugin backbone (offline)."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from core.config.schema import AppConfig, ConfigError
from core.config.providers import provide_app_config
from core.infrastructure.providers import provide_service_factory
from core.infrastructure.repositories import InMemoryVerificationSessionStore
from core.providers.descriptor import ProviderNotRegisteredError
from core.providers.mock.descriptor import MOCK_EID_DESCRIPTOR
from core.providers.mock.mock_provider import MockEIDProvider
from core.providers.registry import EIDProviderRegistry
from core.providers.registry_builder import build_registry
from core.providers.runtime_factory import build_provider_runtime


def _demo_runtime(*, eid_provider: str = "mock"):
    config = provide_app_config()
    store = InMemoryVerificationSessionStore()
    demo = AppConfig(**{**config.__dict__, "eid_provider": eid_provider, "db_backend": "in_memory"})
    return build_provider_runtime(config=demo, session_store=store)


def test_build_registry_registers_mock_via_descriptor() -> None:
    runtime = _demo_runtime()
    registry = build_registry(runtime)
    assert registry.registered_names == frozenset({"mock"})
    assert isinstance(registry.get("mock"), MockEIDProvider)


def test_mock_descriptor_builds_provider() -> None:
    runtime = _demo_runtime()
    provider = MOCK_EID_DESCRIPTOR.build(runtime)
    assert provider.provider_name == "mock"


def test_build_registry_does_not_create_httpx_in_mock_mode() -> None:
    runtime = _demo_runtime(eid_provider="mock")
    assert runtime.http_client is None
    with patch("core.providers.runtime_factory.httpx.Client") as mock_client:
        build_registry(runtime)
        mock_client.assert_not_called()


def test_build_provider_runtime_creates_httpx_for_non_mock_active() -> None:
    store = InMemoryVerificationSessionStore()
    config = provide_app_config()
    non_mock = AppConfig(**{**config.__dict__, "eid_provider": "eideasy"})
    with patch("core.providers.runtime_factory.httpx.Client") as mock_client:
        sentinel = object()
        mock_client.return_value = sentinel
        runtime = build_provider_runtime(config=non_mock, session_store=store)
        mock_client.assert_called_once_with(timeout=float(non_mock.oidc_request_timeout_s))
        assert runtime.http_client is sentinel


def test_factory_path_uses_descriptor_registry() -> None:
    factory = provide_service_factory()
    registry = factory.get_eid_provider_registry()
    assert registry.registered_names == frozenset({"mock"})


def test_get_unknown_provider_raises_config_error_with_available_list() -> None:
    store = InMemoryVerificationSessionStore()
    registry = EIDProviderRegistry({"mock": MockEIDProvider(store)})
    with pytest.raises(ProviderNotRegisteredError) as exc_info:
        registry.get("eideasy")
    message = str(exc_info.value)
    assert "доступны" in message
    assert "mock" in message
    assert isinstance(exc_info.value, ConfigError)


def test_get_active_missing_provider_raises_provider_not_registered() -> None:
    registry = EIDProviderRegistry({})
    config = provide_app_config()
    missing = AppConfig(**{**config.__dict__, "eid_provider": "eideasy"})
    with pytest.raises(ProviderNotRegisteredError):
        registry.get_active(missing)
