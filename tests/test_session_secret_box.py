"""EPIC-IDS-09 STORY-IDS-EID-08 — SessionSecretBox for PKCE session secrets (offline)."""

from __future__ import annotations

import pytest

from core.config import ConfigError, load_config_from_env
from core.config.providers import provide_app_config
from core.config.schema import AppConfig, _DEMO_EID_SESSION_ENC_KEY
from core.infrastructure.repositories import InMemoryVerificationSessionStore
from core.providers.runtime_factory import build_provider_runtime
from core.security.session_secret import (
    FernetSessionSecretBox,
    SessionSecretError,
    build_session_secret_box,
)

_PILOT_BASE = {
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
    "SERVICE_API_TOKEN": "service-api-token",
}


def _valid_fernet_key() -> str:
    from cryptography.fernet import Fernet

    return Fernet.generate_key().decode("utf-8")


def test_fernet_session_secret_box_round_trip() -> None:
    key = _valid_fernet_key()
    box = build_session_secret_box(encryption_key=key)
    plaintext = "pkce-code-verifier-abc123"
    token = box.seal(plaintext)
    assert box.open(token) == plaintext
    assert token != plaintext


def test_fernet_session_secret_box_rejects_tampered_token() -> None:
    box = build_session_secret_box(encryption_key=_valid_fernet_key())
    token = box.seal("secret")
    with pytest.raises(SessionSecretError):
        box.open(token[:-1] + ("x" if token[-1] != "x" else "y"))


def test_build_session_secret_box_does_not_use_eid_secret() -> None:
    enc_key = _valid_fernet_key()
    box = build_session_secret_box(encryption_key=enc_key)
    token = box.seal("verifier")
    other = build_session_secret_box(encryption_key=_valid_fernet_key())
    with pytest.raises(SessionSecretError):
        other.open(token)


def test_demo_profile_uses_ephemeral_default_when_env_unset() -> None:
    cfg = load_config_from_env(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "http://localhost:8100",
            "DB_BACKEND": "in_memory",
            "EID_PROVIDER": "mock",
        }
    )
    assert cfg.eid_session_enc_key == _DEMO_EID_SESSION_ENC_KEY


def test_pilot_missing_eid_session_enc_key_raises_config_error() -> None:
    env = dict(_PILOT_BASE)
    env["EID_SESSION_ENC_KEY"] = ""
    with pytest.raises(ConfigError, match="EID_SESSION_ENC_KEY"):
        load_config_from_env(env)


def test_pilot_accepts_explicit_eid_session_enc_key() -> None:
    env = dict(_PILOT_BASE)
    env["EID_SESSION_ENC_KEY"] = _valid_fernet_key()
    cfg = load_config_from_env(env)
    assert cfg.eid_session_enc_key == env["EID_SESSION_ENC_KEY"]


def test_build_provider_runtime_wires_secret_box() -> None:
    store = InMemoryVerificationSessionStore()
    config = provide_app_config()
    runtime = build_provider_runtime(config=config, session_store=store)
    assert runtime.secret_box is not None
    assert isinstance(runtime.secret_box, FernetSessionSecretBox)


def test_runtime_secret_box_uses_eid_session_enc_key_not_eid_secret() -> None:
    store = InMemoryVerificationSessionStore()
    base = provide_app_config()
    enc_key = _valid_fernet_key()
    config = AppConfig(**{**base.__dict__, "eid_session_enc_key": enc_key, "eid_secret": "hmac-only"})
    runtime = build_provider_runtime(config=config, session_store=store)
    assert runtime.secret_box is not None
    token = runtime.secret_box.seal("verifier")
    direct = build_session_secret_box(encryption_key=enc_key)
    assert direct.open(token) == "verifier"
    wrong = build_session_secret_box(encryption_key=_valid_fernet_key())
    with pytest.raises(SessionSecretError):
        wrong.open(token)
