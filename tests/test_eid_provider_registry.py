"""EPIC-IDS-06 Story 2 — eID provider registry + mock provider (offline)."""

from __future__ import annotations

import pytest

from core.config.providers import provide_app_config
from core.infrastructure.providers import provide_service_factory
from core.infrastructure.repositories import InMemoryVerificationSessionStore
from core.providers.mock.mock_provider import MockEIDProvider
from core.providers.registry import EIDProviderRegistry


def test_mock_provider_registered_by_default() -> None:
    factory = provide_service_factory()
    registry = factory.get_eid_provider_registry()
    assert "mock" in registry._providers  # noqa: SLF001 — registry contract smoke
    assert isinstance(registry.get("mock"), MockEIDProvider)


def test_get_active_returns_mock_when_eid_provider_mock() -> None:
    config = provide_app_config()
    assert config.eid_provider == "mock"
    factory = provide_service_factory(config)
    active = factory.get_eid_provider_registry().get_active(config)
    assert active.provider_name == "mock"


def test_get_unknown_provider_raises() -> None:
    store = InMemoryVerificationSessionStore()
    registry = EIDProviderRegistry({"mock": MockEIDProvider(store)})
    with pytest.raises(KeyError):
        registry.get("unknown")


def test_mock_provider_start_flow_creates_session() -> None:
    store = InMemoryVerificationSessionStore()
    registry = EIDProviderRegistry({"mock": MockEIDProvider(store)})
    config = provide_app_config()
    start = registry.get_active(config).start_flow(
        supabase_user_id="user-smoke-1",
        return_url="https://app.example/verify",
        return_context="dashboard_verification",
        requested_action="eid:verify",
    )
    assert start.session_id
    assert start.session_id in store._by_id  # noqa: SLF001 — session persisted in store
