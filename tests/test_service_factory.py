from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from core.api.security import SupabaseJwtBearerTokenAuth
from core.application.factory import ServiceFactory
from core.config.schema import AppConfig, DeploymentProfile
from core.domain.models import UserClaims
from core.infrastructure.repositories import (
    InMemoryEIDAuditLogRepository,
    InMemoryHealthRepository,
    InMemoryOAuthClientStore,
    InMemoryOAuthTokenService,
    InMemoryProfileRepository,
    InMemoryVerificationSessionStore,
)
from core.infrastructure.service_factory import DefaultServiceFactory
from core.providers.registry import EIDProviderRegistry


class _StubSupabaseJwtValidator:
    def validate(self, token: str) -> UserClaims:
        del token
        return UserClaims(supabase_user_id="stub-user", email=None, role="authenticated")


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
        "eid_session_enc_key": "2zy6gKOpxhkaNwtmufGZqYb0T88uh-tkKHC5ygQOnIM=",
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
        "sms_provider": "mock",
        "phone_allowed_dial_prefixes": ("+372",),
        "phone_code_length": 6,
        "phone_code_ttl_s": 300,
        "phone_max_attempts": 5,
        "phone_resend_cooldown_s": 60,
        "phone_one_account_per_number": True,
    }
    base.update(overrides)
    return AppConfig(**base)


def _build_factory(config: AppConfig | None = None) -> DefaultServiceFactory:
    resolved = config or _demo_config()
    return DefaultServiceFactory(
        config=resolved,
        health_repository=InMemoryHealthRepository(),
        profile_repository=InMemoryProfileRepository(),
        verification_session_store=InMemoryVerificationSessionStore(),
        eid_audit_log_repository=InMemoryEIDAuditLogRepository(),
        oauth_client_store=InMemoryOAuthClientStore.from_config(resolved),
        oauth_token_service=InMemoryOAuthTokenService(config=resolved),
        supabase_jwt_validator=_StubSupabaseJwtValidator(),
        bearer_token_auth=SupabaseJwtBearerTokenAuth(validator=_StubSupabaseJwtValidator()),
        eid_provider_registry=EIDProviderRegistry({}),
    )


def test_default_service_factory_returns_config() -> None:
    config = _demo_config(api_base_url="http://example.test")
    factory = _build_factory(config)
    assert factory.config is config


def test_get_profile_repository_returns_same_instance() -> None:
    factory = _build_factory()
    assert factory.get_profile_repository() is factory.get_profile_repository()


def test_default_service_factory_is_frozen() -> None:
    factory = _build_factory()
    with pytest.raises(FrozenInstanceError):
        factory.something = "x"  # type: ignore[attr-defined]


def test_default_service_factory_satisfies_service_factory_protocol() -> None:
    factory = _build_factory()
    assert isinstance(factory, ServiceFactory)


def test_get_methods_return_same_instances() -> None:
    factory = _build_factory()
    assert factory.get_health_repository() is factory.get_health_repository()
    assert factory.get_verification_session_store() is factory.get_verification_session_store()
    assert factory.get_eid_audit_log_repository() is factory.get_eid_audit_log_repository()
    assert factory.get_oauth_client_store() is factory.get_oauth_client_store()
    assert factory.get_oauth_token_service() is factory.get_oauth_token_service()
    assert factory.get_supabase_jwt_validator() is factory.get_supabase_jwt_validator()
    assert factory.get_bearer_token_auth() is factory.get_bearer_token_auth()
    assert factory.get_eid_provider_registry() is factory.get_eid_provider_registry()
