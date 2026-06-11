from __future__ import annotations

import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Final

from core.config.errors import ConfigError
from core.providers.config_spec import _env_value

DEFAULT_TELNYX_API_BASE_URL: Final = "https://api.telnyx.com"
DEFAULT_TELNYX_FROM: Final = "DOGEstonia"
DEFAULT_TELNYX_MESSAGE_TYPE: Final = "SMS"
DEFAULT_TELNYX_ENCODING: Final = "auto"

TELNYX_REQUIRED_ENV: Final = ("TELNYX_API_KEY",)

_E164_SENDER_RE = re.compile(r"^\+\d+$")


def is_e164_sender(value: str) -> bool:
    return bool(_E164_SENDER_RE.match(value))


def validate_telnyx_config(env: Mapping[str, str]) -> None:
    for key in TELNYX_REQUIRED_ENV:
        if not _env_value(env, key):
            raise ConfigError(f"Required env var {key!r} is missing or empty")

    from_sender = _env_value(env, "TELNYX_FROM", DEFAULT_TELNYX_FROM)
    profile_id = _env_value(env, "TELNYX_MESSAGING_PROFILE_ID")
    if not is_e164_sender(from_sender) and not profile_id:
        raise ConfigError(
            "TELNYX_MESSAGING_PROFILE_ID is required when TELNYX_FROM is alphanumeric (non-E.164)"
        )


@dataclass(frozen=True)
class TelnyxSettings:
    api_key: str
    api_base_url: str
    from_sender: str
    messaging_profile_id: str
    message_type: str
    encoding: str

    @classmethod
    def load(cls, env: Mapping[str, str]) -> TelnyxSettings:
        return cls(
            api_key=_env_value(env, "TELNYX_API_KEY"),
            api_base_url=_env_value(env, "TELNYX_API_BASE_URL", DEFAULT_TELNYX_API_BASE_URL),
            from_sender=_env_value(env, "TELNYX_FROM", DEFAULT_TELNYX_FROM),
            messaging_profile_id=_env_value(env, "TELNYX_MESSAGING_PROFILE_ID"),
            message_type=_env_value(env, "TELNYX_MESSAGE_TYPE", DEFAULT_TELNYX_MESSAGE_TYPE),
            encoding=_env_value(env, "TELNYX_ENCODING", DEFAULT_TELNYX_ENCODING),
        )


@dataclass(frozen=True)
class TelnyxSmsProviderConfigSpec:
    required: tuple[str, ...] = TELNYX_REQUIRED_ENV
    optional_defaults: dict[str, str] = field(
        default_factory=lambda: {
            "TELNYX_API_BASE_URL": DEFAULT_TELNYX_API_BASE_URL,
            "TELNYX_FROM": DEFAULT_TELNYX_FROM,
            "TELNYX_MESSAGE_TYPE": DEFAULT_TELNYX_MESSAGE_TYPE,
            "TELNYX_ENCODING": DEFAULT_TELNYX_ENCODING,
        }
    )
    loader: Callable[[Mapping[str, str]], TelnyxSettings] = TelnyxSettings.load

    def validate(self, env: Mapping[str, str]) -> None:
        validate_telnyx_config(env)

    def load(self, env: Mapping[str, str]) -> TelnyxSettings:
        self.validate(env)
        return self.loader(env)


TELNYX_SMS_CONFIG_SPEC = TelnyxSmsProviderConfigSpec()
