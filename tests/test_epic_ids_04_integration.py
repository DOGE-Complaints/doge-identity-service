from __future__ import annotations

import logging
import time

import pytest
from joserfc import jwt
from joserfc.jwk import OctKey

from core.api.dependencies import build_api_dependencies
from core.api.security import SupabaseJwtBearerTokenAuth
from core.config.providers import provide_app_config
from core.config.schema import AppConfig
from core.domain.contracts import ProfileRepository
from core.infrastructure.providers import provide_service_factory
from core.infrastructure.repositories import (
    InMemoryEIDAuditLogRepository,
    InMemoryOAuthClientStore,
    InMemoryOAuthTokenService,
    InMemoryProfileRepository,
    InMemoryStoryDraftRepository,
    InMemoryVerificationSessionStore,
)
from core.infrastructure.service_factory import DefaultServiceFactory

_BASE_ENV = {
    "APP_PROFILE": "demo",
    "API_BASE_URL": "http://localhost:8100",
    "DB_BACKEND": "in_memory",
    "EID_PROVIDER": "mock",
}

_SUPABASE_ENV = {
    **_BASE_ENV,
    "DB_BACKEND": "supabase",
    "SUPABASE_URL": "https://example.supabase.co",
    "SUPABASE_SERVICE_ROLE": "service-role-key",
}


def _make_demo_jwt(*, secret: str = "test-secret-for-demo", supabase_url: str = "https://demo.local") -> str:
    now = int(time.time())
    claims = {
        "sub": "11111111-1111-1111-1111-111111111111",
        "role": "authenticated",
        "aud": "authenticated",
        "iss": f"{supabase_url.rstrip('/')}/auth/v1",
        "exp": now + 3600,
        "iat": now,
    }
    key = OctKey.import_key(secret)
    return jwt.encode({"alg": "HS256"}, claims, key)


def test_epic_section8_imports() -> None:
    from core.api.security import SupabaseJwtBearerTokenAuth as _Bearer
    from core.auth.supabase_validator import JwtValidationError, SupabaseJwtValidatorImpl
    from core.domain.contracts import (
        BearerTokenAuth,
        EIDAuditLogRepository,
        OAuthClientStore,
        OAuthTokenService,
        ProfileRepository,
        StoryDraftRepository,
        SupabaseJwtValidator,
        VerificationSessionStore,
    )
    from core.infrastructure.providers import provide_service_factory as _provide
    from core.infrastructure.repositories import InMemoryProfileRepository as _ProfileRepo
    from core.infrastructure.service_factory import DefaultServiceFactory as _Factory
    from core.providers.base import EIDProviderPort, EIDStartResult, EIDVerificationResult
    from core.providers.mock.mock_provider import MockEIDProvider
    from core.providers.registry import EIDProviderRegistry

    assert _Bearer is not None
    assert _provide is not None
    assert ProfileRepository is not None


def test_epic_section8_protocol_isinstance() -> None:
    assert isinstance(InMemoryProfileRepository(), ProfileRepository)


def test_provide_service_factory_in_memory_returns_default_factory(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for key, value in _BASE_ENV.items():
        monkeypatch.setenv(key, value)
    factory = provide_service_factory()
    assert isinstance(factory, DefaultServiceFactory)
    assert factory.config.db_backend == "in_memory"
    assert isinstance(factory.get_profile_repository(), InMemoryProfileRepository)
    assert isinstance(factory.get_verification_session_store(), InMemoryVerificationSessionStore)
    assert isinstance(factory.get_eid_audit_log_repository(), InMemoryEIDAuditLogRepository)
    assert isinstance(factory.get_oauth_client_store(), InMemoryOAuthClientStore)
    assert isinstance(factory.get_oauth_token_service(), InMemoryOAuthTokenService)
    assert isinstance(factory.get_story_draft_repository(), InMemoryStoryDraftRepository)


def test_provide_service_factory_supabase_falls_back_with_warning(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    for key, value in _SUPABASE_ENV.items():
        monkeypatch.setenv(key, value)
    config = provide_app_config()
    with caplog.at_level(logging.WARNING):
        factory = provide_service_factory(config)
    assert isinstance(factory.get_profile_repository(), InMemoryProfileRepository)
    assert any("EPIC-IDS-05" in record.message for record in caplog.records)


def test_provide_service_factory_unsupported_backend_raises() -> None:
    config = provide_app_config(_BASE_ENV)
    broken = AppConfig(**{**config.__dict__, "db_backend": "sqlite"})
    with pytest.raises(ValueError, match="Unsupported db_backend"):
        provide_service_factory(broken)


def test_build_api_dependencies_integration(monkeypatch: pytest.MonkeyPatch) -> None:
    for key, value in _BASE_ENV.items():
        monkeypatch.setenv(key, value)
    deps = build_api_dependencies()
    assert deps.profile_repository is not None
    assert deps.eid_provider_registry is not None
    assert deps.eid_provider_registry.get("mock").provider_name == "mock"
    assert type(deps.bearer_token_auth).__name__ == "SupabaseJwtBearerTokenAuth"
    assert isinstance(deps.bearer_token_auth, SupabaseJwtBearerTokenAuth)


def test_build_api_dependencies_bearer_accepts_valid_demo_jwt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for key, value in _BASE_ENV.items():
        monkeypatch.setenv(key, value)
    deps = build_api_dependencies()
    token = _make_demo_jwt()
    claims = deps.bearer_token_auth.validate({"authorization": f"Bearer {token}"})
    assert claims.supabase_user_id == "11111111-1111-1111-1111-111111111111"
