"""STORY-IDS-EID-04 — provider-owned configuration (offline)."""

from __future__ import annotations

import pytest

from core.config import ConfigError, load_config_from_env
from core.providers.authentigate.config import (
    AUTHENTIGATE_CONFIG_SPEC,
    DEFAULT_AUTHENTIGATE_SCOPES,
    AuthentigateSettings,
)


def _base_env(**overrides: str) -> dict[str, str]:
    env = {
        "APP_PROFILE": "demo",
        "API_BASE_URL": "http://localhost:8100",
        "DB_BACKEND": "in_memory",
    }
    env.update(overrides)
    return env


def test_authentigate_provider_requires_client_id() -> None:
    with pytest.raises(ConfigError, match="AUTHENTIGATE_CLIENT_ID"):
        load_config_from_env(
            _base_env(
                EID_PROVIDER="authentigate",
                AUTHENTIGATE_ISSUER="https://oidc.demo.sk.ee",
                AUTHENTIGATE_CLIENT_SECRET="secret",
                AUTHENTIGATE_REDIRECT_URI="http://localhost:8100/auth/authentigate/callback",
            )
        )


def test_authentigate_settings_default_scopes_use_full_claim_urls() -> None:
    settings = AUTHENTIGATE_CONFIG_SPEC.load(
        {
            "AUTHENTIGATE_ISSUER": "https://oidc.demo.sk.ee",
            "AUTHENTIGATE_CLIENT_ID": "client",
            "AUTHENTIGATE_CLIENT_SECRET": "secret",
            "AUTHENTIGATE_REDIRECT_URI": "http://localhost:8100/auth/authentigate/callback",
        }
    )
    assert isinstance(settings, AuthentigateSettings)
    assert settings.scopes == DEFAULT_AUTHENTIGATE_SCOPES
    assert "https://id.authentigate.eu/claims/" in settings.scopes


def test_authentigate_settings_derives_discovery_url_from_issuer() -> None:
    settings = AuthentigateSettings.load(
        {
            "AUTHENTIGATE_ISSUER": "https://oidc.demo.sk.ee",
            "AUTHENTIGATE_CLIENT_ID": "client",
            "AUTHENTIGATE_CLIENT_SECRET": "secret",
            "AUTHENTIGATE_REDIRECT_URI": "http://localhost:8100/auth/authentigate/callback",
        }
    )
    assert settings.discovery_url == "https://oidc.demo.sk.ee/.well-known/openid-configuration"


def test_schema_has_no_provider_specific_ifs() -> None:
    import inspect

    from core.config import schema as schema_module

    source = inspect.getsource(schema_module.load_config_from_env)
    assert 'eid_provider == "eideasy"' not in source
    assert 'eid_provider == "authentigate"' not in source
    assert '"mock", "eideasy", "authentigate"' not in source
    assert "registered_eid_provider_names" in source
