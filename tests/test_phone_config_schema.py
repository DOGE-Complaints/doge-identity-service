from __future__ import annotations

import pytest

from core.config import ConfigError, load_config_from_env
from core.config.providers import provide_app_config


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


def test_telnyx_sms_provider_requires_api_key() -> None:
    with pytest.raises(ConfigError, match="TELNYX_API_KEY"):
        load_config_from_env(_minimal_env(SMS_PROVIDER="telnyx"))


def test_telnyx_sms_provider_requires_profile_for_alphanumeric_from() -> None:
    with pytest.raises(ConfigError, match="TELNYX_MESSAGING_PROFILE_ID"):
        load_config_from_env(
            _minimal_env(
                SMS_PROVIDER="telnyx",
                TELNYX_API_KEY="KEY_test",
                TELNYX_FROM="DOGEstonia",
            )
        )


def test_telnyx_sms_provider_loads_with_required_env() -> None:
    cfg = load_config_from_env(
        _minimal_env(
            SMS_PROVIDER="telnyx",
            TELNYX_API_KEY="KEY_test",
            TELNYX_MESSAGING_PROFILE_ID="profile-uuid",
        )
    )
    assert cfg.sms_provider == "telnyx"


def test_phone_allowed_dial_prefixes_parsed_to_tuple() -> None:
    cfg = load_config_from_env(_minimal_env(PHONE_ALLOWED_DIAL_PREFIXES="+372,+358"))
    assert cfg.phone_allowed_dial_prefixes == ("+372", "+358")


def test_core_phone_params_on_app_config() -> None:
    cfg = provide_app_config()
    assert cfg.sms_provider == "mock"
    assert cfg.phone_allowed_dial_prefixes == ("+372",)
    assert cfg.phone_code_length == 6
    assert cfg.phone_code_ttl_s == 300
    assert cfg.phone_max_attempts == 5
    assert cfg.phone_resend_cooldown_s == 60
    assert cfg.phone_one_account_per_number is True
    assert not hasattr(cfg, "telnyx_api_key")


def test_sms_provider_membership_lists_registered_names() -> None:
    with pytest.raises(ConfigError, match="mock"):
        load_config_from_env(_minimal_env(SMS_PROVIDER="unknown"))
