"""EPIC-IDS-06 Story 2 — bootstrap / config smoke (offline, no network)."""

from __future__ import annotations

import os

import pytest

from core.config import ConfigError, load_config_from_env, provide_app_config


def test_core_imports() -> None:
    import core.api.asgi_app  # noqa: F401
    import core.api.dependencies  # noqa: F401
    import core.config  # noqa: F401
    import core.domain.contracts  # noqa: F401
    import core.providers.base  # noqa: F401
    import core.security.hashing  # noqa: F401


def test_app_config_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DB_BACKEND", "in_memory")
    monkeypatch.setenv("EID_PROVIDER", "mock")
    config = provide_app_config()
    assert config.db_backend == "in_memory"
    assert config.eid_provider == "mock"


def test_config_fail_fast_on_invalid_backend(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "http://localhost:8100")
    monkeypatch.setenv("DB_BACKEND", "postgres")
    monkeypatch.setenv("EID_PROVIDER", "mock")
    with pytest.raises(ConfigError):
        load_config_from_env(dict(os.environ))


def test_config_fail_fast_on_pilot_without_secrets(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_PROFILE", "pilot")
    monkeypatch.setenv("API_BASE_URL", "https://identity.dogestonia.ee")
    monkeypatch.setenv("DB_BACKEND", "in_memory")
    monkeypatch.setenv("EID_PROVIDER", "mock")
    monkeypatch.delenv("OAUTH_ACCESS_TOKEN_SECRET", raising=False)
    with pytest.raises(ConfigError):
        load_config_from_env(dict(os.environ))


def test_config_fail_fast_on_pilot_empty_eid_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_PROFILE", "pilot")
    monkeypatch.setenv("API_BASE_URL", "https://identity.dogestonia.ee")
    monkeypatch.setenv("DB_BACKEND", "supabase")
    monkeypatch.setenv("EID_PROVIDER", "mock")
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "sr")
    monkeypatch.setenv("SUPABASE_JWT_SECRET", "jwt")
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/db")
    monkeypatch.setenv("DOGESTONIA_EID_SECRET", "")
    monkeypatch.setenv("CODE_VERIFIER_ENCRYPTION_KEY", "enc-key")
    monkeypatch.setenv("OAUTH_ACCESS_TOKEN_SECRET", "oauth")
    monkeypatch.setenv("GPT_OAUTH_CLIENT_SECRET", "gpt")
    with pytest.raises(ConfigError):
        load_config_from_env(dict(os.environ))


def test_config_fail_fast_on_unknown_eid_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "http://localhost:8100")
    monkeypatch.setenv("DB_BACKEND", "in_memory")
    monkeypatch.setenv("EID_PROVIDER", "xyz")
    with pytest.raises(ConfigError):
        load_config_from_env(dict(os.environ))
