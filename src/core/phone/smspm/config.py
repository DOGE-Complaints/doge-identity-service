from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Final

from core.config.errors import ConfigError
from core.providers.config_spec import _env_value

DEFAULT_SMSPM_API_BASE_URL: Final = "https://api.smspm.com"

SMSPM_REQUIRED_ENV: Final = ("SMSPM_HASH", "SMSPM_TOKEN", "SMSPM_FROM")


def validate_smspm_config(env: Mapping[str, str]) -> None:
    for key in SMSPM_REQUIRED_ENV:
        if not _env_value(env, key):
            raise ConfigError(f"Required env var {key!r} is missing or empty")


@dataclass(frozen=True)
class SmspmSettings:
    hash: str
    token: str
    from_sender: str
    api_base_url: str

    @classmethod
    def load(cls, env: Mapping[str, str]) -> SmspmSettings:
        return cls(
            hash=_env_value(env, "SMSPM_HASH"),
            token=_env_value(env, "SMSPM_TOKEN"),
            from_sender=_env_value(env, "SMSPM_FROM"),
            api_base_url=_env_value(env, "SMSPM_API_BASE_URL", DEFAULT_SMSPM_API_BASE_URL),
        )


@dataclass(frozen=True)
class SmspmSmsProviderConfigSpec:
    required: tuple[str, ...] = SMSPM_REQUIRED_ENV
    optional_defaults: dict[str, str] = field(
        default_factory=lambda: {"SMSPM_API_BASE_URL": DEFAULT_SMSPM_API_BASE_URL}
    )
    loader: Callable[[Mapping[str, str]], SmspmSettings] = SmspmSettings.load

    def validate(self, env: Mapping[str, str]) -> None:
        validate_smspm_config(env)

    def load(self, env: Mapping[str, str]) -> SmspmSettings:
        self.validate(env)
        return self.loader(env)


SMSPM_SMS_CONFIG_SPEC = SmspmSmsProviderConfigSpec()
