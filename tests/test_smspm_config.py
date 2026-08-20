"""EPIC-IDS-14 STORY-IDS-SMSPM-01 — SMSPM provider config + registry (offline)."""

from __future__ import annotations

import pytest

from core.config import ConfigError, load_config_from_env
from core.phone.registry_builder import build_sms_registry, registered_sms_provider_names
from core.phone.runtime_factory import build_sms_provider_runtime
from core.phone.smspm.config import (
    DEFAULT_SMSPM_API_BASE_URL,
    SMSPM_REQUIRED_ENV,
    SMSPM_SMS_CONFIG_SPEC,
)
from core.phone.smspm.sender import SmspmSmsSender


def _minimal_env(**overrides: str) -> dict[str, str]:
    base = {
        "APP_PROFILE": "demo",
        "API_BASE_URL": "http://localhost:8100",
        "DB_BACKEND": "in_memory",
        "EID_PROVIDER": "mock",
        "SMS_PROVIDER": "mock",
    }
    base.update(overrides)
    return base


def _smspm_env(**overrides: str) -> dict[str, str]:
    env = _minimal_env(
        SMS_PROVIDER="smspm",
        SMSPM_HASH="hash-test",
        SMSPM_TOKEN="token-test",
        SMSPM_FROM="DOGEstonia",
    )
    env.update(overrides)
    return env


def test_registered_sms_provider_names_includes_smspm() -> None:
    names = registered_sms_provider_names()
    assert "smspm" in names
    assert {"mock", "file", "telnyx"}.issubset(names)


def test_smspm_sms_provider_loads_with_required_env() -> None:
    cfg = load_config_from_env(_smspm_env())
    assert cfg.sms_provider == "smspm"


def test_smspm_sms_provider_requires_hash() -> None:
    with pytest.raises(ConfigError, match="SMSPM_HASH"):
        load_config_from_env(_smspm_env(SMSPM_HASH=""))


def test_smspm_sms_provider_requires_token() -> None:
    with pytest.raises(ConfigError, match="SMSPM_TOKEN"):
        load_config_from_env(_smspm_env(SMSPM_TOKEN=""))


def test_smspm_sms_provider_requires_from() -> None:
    with pytest.raises(ConfigError, match="SMSPM_FROM"):
        load_config_from_env(_smspm_env(SMSPM_FROM=""))


def test_smspm_optional_webhook_and_report_not_required() -> None:
    settings = SMSPM_SMS_CONFIG_SPEC.load(
        {
            "SMSPM_HASH": "hash-test",
            "SMSPM_TOKEN": "token-test",
            "SMSPM_FROM": "DOGEstonia",
        }
    )
    assert settings.webhook_shared_secret == ""
    assert settings.report_url == ""
    assert "SMSPM_WEBHOOK_SHARED_SECRET" not in SMSPM_REQUIRED_ENV
    assert "SMSPM_REPORT_URL" not in SMSPM_REQUIRED_ENV


def test_smspm_optional_base_url_default() -> None:
    settings = SMSPM_SMS_CONFIG_SPEC.load(
        {
            "SMSPM_HASH": "hash-test",
            "SMSPM_TOKEN": "token-test",
            "SMSPM_FROM": "DOGEstonia",
        }
    )
    assert settings.api_base_url == DEFAULT_SMSPM_API_BASE_URL


def test_mock_without_smspm_env_ok() -> None:
    cfg = load_config_from_env(_minimal_env(SMS_PROVIDER="mock"))
    assert cfg.sms_provider == "mock"


def test_file_without_smspm_env_ok() -> None:
    cfg = load_config_from_env(_minimal_env(SMS_PROVIDER="file"))
    assert cfg.sms_provider == "file"


def test_telnyx_without_smspm_env_ok() -> None:
    cfg = load_config_from_env(
        _minimal_env(
            SMS_PROVIDER="telnyx",
            TELNYX_API_KEY="KEY_test",
            TELNYX_MESSAGING_PROFILE_ID="profile-uuid",
        )
    )
    assert cfg.sms_provider == "telnyx"


def test_unknown_sms_provider_still_rejected() -> None:
    with pytest.raises(ConfigError, match="SMS_PROVIDER must be"):
        load_config_from_env(_minimal_env(SMS_PROVIDER="unknown"))


def test_build_sms_registry_active_smspm_sender() -> None:
    env = _smspm_env()
    config = load_config_from_env(env)
    runtime = build_sms_provider_runtime(config=config, env=env)
    try:
        registry = build_sms_registry(runtime)
        sender = registry.get("smspm")
        assert isinstance(sender, SmspmSmsSender)
        assert sender.provider_name == "smspm"
    finally:
        if runtime.http_client is not None:
            runtime.http_client.close()
