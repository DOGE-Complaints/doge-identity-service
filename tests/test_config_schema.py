from dataclasses import FrozenInstanceError

import pytest

from core.config import ConfigError, load_config_from_env


def test_demo_minimal_defaults() -> None:
    cfg = load_config_from_env(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "http://localhost:8100",
            "DB_BACKEND": "in_memory",
            "EID_PROVIDER": "mock",
        }
    )
    assert cfg.db_backend == "in_memory"
    assert cfg.eid_provider == "mock"
    assert cfg.request_timeout_s == 15
    assert cfg.oidc_request_timeout_s == 10
    assert cfg.port == 8100
    assert cfg.db_enabled is False


def test_supabase_backend_requires_url_and_service_role() -> None:
    with pytest.raises(ConfigError):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "http://localhost:8100",
                "DB_BACKEND": "supabase",
                "EID_PROVIDER": "mock",
            }
        )


def test_supabase_backend_sets_db_enabled_true() -> None:
    cfg = load_config_from_env(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "http://localhost:8100",
            "DB_BACKEND": "supabase",
            "EID_PROVIDER": "mock",
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_SERVICE_ROLE": "service-role",
        }
    )
    assert cfg.db_enabled is True


def test_sqlite_backend_is_forbidden() -> None:
    with pytest.raises(ConfigError):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "http://localhost:8100",
                "DB_BACKEND": "sqlite",
                "EID_PROVIDER": "mock",
            }
        )


def test_unknown_eid_provider_rejected() -> None:
    with pytest.raises(ConfigError):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "http://localhost:8100",
                "DB_BACKEND": "in_memory",
                "EID_PROVIDER": "unknown",
            }
        )


def test_eideasy_provider_requires_credentials() -> None:
    with pytest.raises(ConfigError):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "http://localhost:8100",
                "DB_BACKEND": "in_memory",
                "EID_PROVIDER": "eideasy",
            }
        )


def test_pilot_requires_secrets() -> None:
    with pytest.raises(ConfigError):
        load_config_from_env(
            {
                "APP_PROFILE": "pilot",
                "API_BASE_URL": "https://identity.dogestonia.ee",
                "DB_BACKEND": "in_memory",
                "EID_PROVIDER": "mock",
            }
        )


def test_pilot_requires_api_base_url() -> None:
    with pytest.raises(ConfigError, match="API_BASE_URL"):
        load_config_from_env(
            {
                "APP_PROFILE": "pilot",
                "DB_BACKEND": "supabase",
                "EID_PROVIDER": "mock",
                "SUPABASE_URL": "https://example.supabase.co",
                "SUPABASE_SERVICE_ROLE": "sr",
                "SUPABASE_JWT_SECRET": "jwt",
                "DATABASE_URL": "postgresql://postgres:pass@example:5432/postgres",
                "DOGESTONIA_EID_SECRET": "eid-secret",
                "OAUTH_ACCESS_TOKEN_SECRET": "oauth",
                "GPT_OAUTH_CLIENT_SECRET": "gpt-secret",
            }
        )


def test_pilot_requires_oauth_access_token_secret_explicitly() -> None:
    with pytest.raises(ConfigError, match="OAUTH_ACCESS_TOKEN_SECRET"):
        load_config_from_env(
            {
                "APP_PROFILE": "pilot",
                "API_BASE_URL": "https://identity.dogestonia.ee",
                "DB_BACKEND": "supabase",
                "EID_PROVIDER": "mock",
                "SUPABASE_URL": "https://example.supabase.co",
                "SUPABASE_SERVICE_ROLE": "sr",
                "SUPABASE_JWT_SECRET": "jwt",
                "DATABASE_URL": "postgresql://postgres:pass@example:5432/postgres",
                "DOGESTONIA_EID_SECRET": "eid-secret",
                "EID_SESSION_ENC_KEY": "2zy6gKOpxhkaNwtmufGZqYb0T88uh-tkKHC5ygQOnIM=",
                "GPT_OAUTH_CLIENT_SECRET": "gpt-secret",
            }
        )


def test_pilot_requires_service_api_token() -> None:
    with pytest.raises(ConfigError, match="SERVICE_API_TOKEN"):
        load_config_from_env(
            {
                "APP_PROFILE": "pilot",
                "API_BASE_URL": "https://identity.dogestonia.ee",
                "DB_BACKEND": "supabase",
                "EID_PROVIDER": "mock",
                "SUPABASE_URL": "https://example.supabase.co",
                "SUPABASE_SERVICE_ROLE": "sr",
                "SUPABASE_JWT_SECRET": "jwt",
                "DATABASE_URL": "postgresql://postgres:pass@example:5432/postgres",
                "DOGESTONIA_EID_SECRET": "eid-secret",
                "EID_SESSION_ENC_KEY": "2zy6gKOpxhkaNwtmufGZqYb0T88uh-tkKHC5ygQOnIM=",
                "OAUTH_ACCESS_TOKEN_SECRET": "oauth",
                "GPT_OAUTH_CLIENT_SECRET": "gpt-secret",
            }
        )


def test_pilot_empty_eid_secret_rejected() -> None:
    with pytest.raises(ConfigError):
        load_config_from_env(
            {
                "APP_PROFILE": "pilot",
                "API_BASE_URL": "https://identity.dogestonia.ee",
                "DB_BACKEND": "supabase",
                "EID_PROVIDER": "mock",
                "SUPABASE_URL": "https://example.supabase.co",
                "SUPABASE_SERVICE_ROLE": "sr",
                "SUPABASE_JWT_SECRET": "jwt",
                "DATABASE_URL": "postgresql://postgres:pass@example:5432/postgres",
                "DOGESTONIA_EID_SECRET": "",
                "EID_SESSION_ENC_KEY": "2zy6gKOpxhkaNwtmufGZqYb0T88uh-tkKHC5ygQOnIM=",
                "OAUTH_ACCESS_TOKEN_SECRET": "oauth",
                "GPT_OAUTH_CLIENT_SECRET": "gpt-secret",
                "SERVICE_API_TOKEN": "service-api-token",
            }
        )


def test_pilot_empty_eid_session_enc_key_rejected() -> None:
    with pytest.raises(ConfigError, match="EID_SESSION_ENC_KEY"):
        load_config_from_env(
            {
                "APP_PROFILE": "pilot",
                "API_BASE_URL": "https://identity.dogestonia.ee",
                "DB_BACKEND": "supabase",
                "EID_PROVIDER": "mock",
                "SUPABASE_URL": "https://example.supabase.co",
                "SUPABASE_SERVICE_ROLE": "sr",
                "SUPABASE_JWT_SECRET": "jwt",
                "DATABASE_URL": "postgresql://postgres:pass@example:5432/postgres",
                "DOGESTONIA_EID_SECRET": "eid-secret",
                "EID_SESSION_ENC_KEY": "",
                "OAUTH_ACCESS_TOKEN_SECRET": "oauth",
                "GPT_OAUTH_CLIENT_SECRET": "gpt-secret",
                "SERVICE_API_TOKEN": "service-api-token",
            }
        )


def test_service_api_token_defaults_empty() -> None:
    cfg = load_config_from_env(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "http://localhost:8100",
            "DB_BACKEND": "in_memory",
            "EID_PROVIDER": "mock",
        }
    )
    assert cfg.service_api_token == ""


def test_service_api_token_from_env() -> None:
    cfg = load_config_from_env(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "http://localhost:8100",
            "DB_BACKEND": "in_memory",
            "EID_PROVIDER": "mock",
            "SERVICE_API_TOKEN": "svc-secret-token",
        }
    )
    assert cfg.service_api_token == "svc-secret-token"


def test_config_is_frozen() -> None:
    cfg = load_config_from_env(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "http://localhost:8100",
            "DB_BACKEND": "in_memory",
            "EID_PROVIDER": "mock",
            "DOGESTONIA_EID_SECRET": "secret",
        }
    )
    with pytest.raises(FrozenInstanceError):
        cfg.eid_secret = "changed"  # type: ignore[misc]
