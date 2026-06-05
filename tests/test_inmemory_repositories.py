from __future__ import annotations

import ast
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from core.config.schema import AppConfig, DeploymentProfile
from core.domain.contracts import (
    EIDAuditLogRepository,
    HealthRepository,
    OAuthClientStore,
    OAuthTokenService,
    ProfileRepository,
    VerificationSessionStore,
)
from core.domain.models import VerificationSession
from core.infrastructure.repositories import (
    InMemoryEIDAuditLogRepository,
    InMemoryHealthRepository,
    InMemoryOAuthClientStore,
    InMemoryOAuthTokenService,
    InMemoryProfileRepository,
    InMemoryVerificationSessionStore,
)
from core.security.hashing import hash_secret


REPOSITORIES_PATH = (
    Path(__file__).resolve().parents[1] / "src" / "core" / "infrastructure" / "repositories.py"
)
FORBIDDEN_IMPORT_PREFIXES = ("httpx", "fastapi", "joserfc")


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


def test_inmemory_profile_repository_satisfies_protocol() -> None:
    assert isinstance(InMemoryProfileRepository(), ProfileRepository)


def test_inmemory_verification_session_store_satisfies_protocol() -> None:
    assert isinstance(InMemoryVerificationSessionStore(), VerificationSessionStore)


def test_inmemory_health_repository_satisfies_protocol() -> None:
    assert isinstance(InMemoryHealthRepository(), HealthRepository)


def test_inmemory_eid_audit_log_repository_satisfies_protocol() -> None:
    assert isinstance(InMemoryEIDAuditLogRepository(), EIDAuditLogRepository)


def test_inmemory_oauth_client_store_satisfies_protocol() -> None:
    store = InMemoryOAuthClientStore.from_config(_demo_config())
    assert isinstance(store, OAuthClientStore)


def test_inmemory_oauth_token_service_satisfies_protocol() -> None:
    service = InMemoryOAuthTokenService(config=_demo_config())
    assert isinstance(service, OAuthTokenService)


def test_attach_eid_verification_enforces_unique_verified_person_hash() -> None:
    repo = InMemoryProfileRepository()
    verified_at = datetime.now(timezone.utc)
    repo.attach_eid_verification(
        user_id="u1",
        provider="mock",
        country="EE",
        method="smart_id",
        verified_person_hash="h",
        verified_at=verified_at,
    )
    with pytest.raises(RuntimeError):
        repo.attach_eid_verification(
            user_id="u2",
            provider="mock",
            country="EE",
            method="smart_id",
            verified_person_hash="h",
            verified_at=verified_at,
        )


def test_verification_session_store_unknown_state_returns_none() -> None:
    assert InMemoryVerificationSessionStore().get_by_state("unknown") is None


def test_hash_secret_import_and_determinism() -> None:
    assert hash_secret("demo", key="demo-key") == hash_secret("demo", key="demo-key")


def test_oauth_client_store_from_config_uses_demo_fallbacks() -> None:
    store = InMemoryOAuthClientStore.from_config(_demo_config())
    client = store.get_client("test-gpt-client")
    assert client is not None
    assert client.scopes == ["profile:read", "stories:draft", "stories:create"]
    assert client.client_secret_hash == hash_secret("demo", key="demo-key")


def test_inmemory_oauth_token_service_skips_client_secret_validation() -> None:
    config = _demo_config()
    service = InMemoryOAuthTokenService(config=config)
    code = service.issue_authorization_code(
        supabase_user_id="user-1",
        client_id="gpt-client",
        scopes=["profile:read"],
        redirect_uri="http://localhost/callback",
    )
    token = service.issue_access_token(
        code=code,
        client_id="gpt-client",
        client_secret="wrong-secret",
        redirect_uri="http://localhost/callback",
    )
    assert isinstance(token, str)
    assert token


def test_verification_session_mark_consumed_is_idempotent() -> None:
    now = datetime.now(timezone.utc)
    session = VerificationSession(
        id="sess-1",
        supabase_user_id="user-1",
        state="state-1",
        nonce=None,
        code_verifier_encrypted=None,
        code_verifier_hash=None,
        return_context=None,
        return_url=None,
        requested_action=None,
        status="started",
        created_at=now,
        expires_at=now + timedelta(minutes=10),
        provider="mock",
        provider_session_data={},
    )
    store = InMemoryVerificationSessionStore()
    store.create(session)
    store.mark_consumed("sess-1")
    store.mark_consumed("sess-1")
    assert store.get_by_state("state-1") is None


def test_inmemory_repositories_have_no_forbidden_imports() -> None:
    tree = ast.parse(REPOSITORIES_PATH.read_text(encoding="utf-8"), filename=str(REPOSITORIES_PATH))
    violations: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_name = alias.name
                if any(
                    module_name == prefix or module_name.startswith(f"{prefix}.")
                    for prefix in FORBIDDEN_IMPORT_PREFIXES
                ):
                    violations.append(f"import {module_name}")
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            module_name = node.module
            if any(
                module_name == prefix or module_name.startswith(f"{prefix}.")
                for prefix in FORBIDDEN_IMPORT_PREFIXES
            ):
                violations.append(f"from {module_name} import ...")
    assert violations == []
