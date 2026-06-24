from __future__ import annotations

import pytest

from core.api.asgi_app import _clear_api_dependencies_cache
from core.api.dependencies import build_api_dependencies
from core.config.providers import provide_app_config
from core.config.schema import AppConfig
from core.infrastructure.db_supabase import (
    SupabaseAuthorizationRequestStore,
    SupabaseEIDAuditLogRepository,
    SupabaseHealthRepository,
    SupabaseOAuthClientStore,
    SupabaseOAuthTokenService,
    SupabaseProfileRepository,
    SupabaseVerificationSessionStore,
)
from core.infrastructure.providers import provide_service_factory
from core.infrastructure.repositories import (
    InMemoryAuthorizationRequestStore,
    InMemoryOAuthTokenService,
    InMemoryProfileRepository,
)
from core.infrastructure.service_factory import DefaultServiceFactory

_BASE_ENV = {
    "APP_PROFILE": "demo",
    "API_BASE_URL": "http://localhost:8100",
    "DB_BACKEND": "in_memory",
    "EID_PROVIDER": "mock",
    "CORS_ALLOWED_ORIGINS": "http://localhost:3000",
}

_SUPABASE_ENV = {
    **_BASE_ENV,
    "DB_BACKEND": "supabase",
    "SUPABASE_URL": "https://example.supabase.co",
    "SUPABASE_SERVICE_ROLE": "service-role-key",
}


def test_provide_service_factory_supabase_returns_supabase_repositories(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for key, value in _SUPABASE_ENV.items():
        monkeypatch.setenv(key, value)
    factory = provide_service_factory()
    assert isinstance(factory, DefaultServiceFactory)
    assert factory.config.db_backend == "supabase"
    assert isinstance(factory.get_profile_repository(), SupabaseProfileRepository)
    assert isinstance(
        factory.get_verification_session_store(), SupabaseVerificationSessionStore
    )
    assert isinstance(
        factory.get_eid_audit_log_repository(), SupabaseEIDAuditLogRepository
    )
    assert isinstance(factory.get_health_repository(), SupabaseHealthRepository)
    assert isinstance(factory.get_oauth_client_store(), SupabaseOAuthClientStore)
    assert isinstance(factory.get_oauth_token_service(), SupabaseOAuthTokenService)
    assert isinstance(
        factory.get_oauth_authorization_request_store(),
        SupabaseAuthorizationRequestStore,
    )


def test_backend_switch_is_env_only(monkeypatch: pytest.MonkeyPatch) -> None:
    """Story 6 AC: in_memory ↔ supabase via env without code changes."""
    for key, value in _BASE_ENV.items():
        monkeypatch.setenv(key, value)
    in_memory_factory = provide_service_factory()
    assert isinstance(in_memory_factory.get_profile_repository(), InMemoryProfileRepository)
    assert isinstance(in_memory_factory.get_oauth_token_service(), InMemoryOAuthTokenService)
    assert isinstance(
        in_memory_factory.get_oauth_authorization_request_store(),
        InMemoryAuthorizationRequestStore,
    )

    for key, value in _SUPABASE_ENV.items():
        monkeypatch.setenv(key, value)
    supabase_factory = provide_service_factory(provide_app_config())
    assert isinstance(
        supabase_factory.get_profile_repository(), SupabaseProfileRepository
    )
    assert isinstance(supabase_factory.get_oauth_token_service(), SupabaseOAuthTokenService)
    assert isinstance(
        supabase_factory.get_oauth_authorization_request_store(),
        SupabaseAuthorizationRequestStore,
    )


def test_build_api_dependencies_supabase_fills_db_checks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_api_dependencies_cache()
    for key, value in _SUPABASE_ENV.items():
        monkeypatch.setenv(key, value)
    deps = build_api_dependencies()
    assert deps.db_backend == "supabase"
    assert set(deps.db_checks) == {
        "connectivity",
        "schema",
        "columns",
        "provider_state",
        "policy_probe",
    }
    assert isinstance(deps.profile_repository, SupabaseProfileRepository)


def test_build_api_dependencies_supabase_factory_wiring(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_api_dependencies_cache()
    for key, value in _SUPABASE_ENV.items():
        monkeypatch.setenv(key, value)
    deps = build_api_dependencies()
    factory = provide_service_factory(deps.config)
    assert type(deps.profile_repository) is type(factory.get_profile_repository())
