from __future__ import annotations

import inspect

import pytest

from core.config.schema import AppConfig, ConfigError, DeploymentProfile
from core.infrastructure.repositories import InMemoryVerificationSessionStore
from core.providers.base import EIDProviderPort
from core.providers.mock.mock_provider import MockEIDProvider
from core.providers.registry import EIDProviderRegistry


def _demo_config(**overrides: object) -> AppConfig:
    base = {
        "profile": DeploymentProfile.DEMO,
        "port": 8100,
        "api_base_url": "http://localhost:8100",
        "log_level": "INFO",
        "log_format": "text",
        "request_timeout_s": 15,
        "oidc_request_timeout_s": 10,
        "supabase_url": "",
        "supabase_service_role": "",
        "supabase_jwt_secret": "",
        "database_url": "",
        "authentigate_issuer": "",
        "authentigate_client_id": "",
        "authentigate_client_secret": "",
        "authentigate_redirect_uri": "",
        "authentigate_scopes": "",
        "eid_secret": "",
        "node_id": "test-node",
        "oauth_access_token_secret": "demo-key",
        "oauth_access_token_ttl_s": 3600,
        "oauth_authorization_code_ttl_s": 300,
        "gpt_oauth_client_id": "",
        "gpt_oauth_client_secret": "",
        "gpt_oauth_redirect_uri": "",
        "eid_provider": "mock",
        "eideasy_env": "sandbox",
        "eideasy_base_url": "",
        "eideasy_client_id": "",
        "eideasy_client_secret": "",
        "eideasy_redirect_uri": "",
        "eideasy_allowed_methods": "",
        "eideasy_default_country": "EE",
        "eideasy_allowed_countries": "EE",
        "db_backend": "in_memory",
        "db_enabled": False,
        "cors_allowed_origins": "*",
        "allowed_return_urls": "",
    }
    base.update(overrides)
    return AppConfig(**base)


def test_mock_eid_provider_satisfies_port() -> None:
    store = InMemoryVerificationSessionStore()
    assert isinstance(MockEIDProvider(store), EIDProviderPort)


def test_registry_get_mock_provider() -> None:
    store = InMemoryVerificationSessionStore()
    registry = EIDProviderRegistry({"mock": MockEIDProvider(store)})
    assert registry.get("mock").provider_name == "mock"


def test_registry_get_active_missing_provider_raises_config_error() -> None:
    registry = EIDProviderRegistry({})
    config = _demo_config(eid_provider="eideasy")
    with pytest.raises(ConfigError) as exc_info:
        registry.get_active(config)
    assert "доступны" in str(exc_info.value)


def test_registry_is_not_lru_cached() -> None:
    assert "lru_cache" not in inspect.getsource(EIDProviderRegistry)


def test_mock_provider_identity() -> None:
    store = InMemoryVerificationSessionStore()
    provider = MockEIDProvider(store)
    assert provider.provider_name == "mock"
    assert provider.callback_path == "/auth/mock/callback"


def test_mock_flow_works_without_external_credentials() -> None:
    store = InMemoryVerificationSessionStore()
    provider = MockEIDProvider(store)
    registry = EIDProviderRegistry({"mock": provider})
    config = _demo_config(
        eid_provider="mock",
        eideasy_client_id="",
        eideasy_client_secret="",
        authentigate_client_id="",
        authentigate_client_secret="",
    )
    active = registry.get_active(config)
    start = active.start_flow(
        supabase_user_id="user-1",
        return_url="https://app.example/verify",
        return_context="dashboard_verification",
        requested_action="eid:verify",
    )
    assert start.session_id in start.redirect_url
    assert start.redirect_url.startswith("/auth/mock/callback?session_id=")
    assert start.session_id in store._by_id  # noqa: SLF001 — verify session persisted

    result = active.handle_callback(raw_params={"session_id": start.session_id})
    assert result.provider == "mock"
    assert result.country == "EE"
    assert result.login_method == "mock"
    assert result.subject_hash.startswith("mock-")
