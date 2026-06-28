from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Final

from core.providers.config_spec import _env_value

DEFAULT_FILE_SMS_OUTBOX_DIR: Final = "var/sms-outbox"


@dataclass(frozen=True)
class FileSmsSettings:
    outbox_dir: str

    @classmethod
    def load(cls, env: Mapping[str, str]) -> FileSmsSettings:
        return cls(outbox_dir=_env_value(env, "FILE_SMS_OUTBOX_DIR", DEFAULT_FILE_SMS_OUTBOX_DIR))


@dataclass(frozen=True)
class FileSmsProviderConfigSpec:
    required: tuple[str, ...] = ()
    optional_defaults: dict[str, str] = field(
        default_factory=lambda: {"FILE_SMS_OUTBOX_DIR": DEFAULT_FILE_SMS_OUTBOX_DIR}
    )
    loader: Callable[[Mapping[str, str]], FileSmsSettings] = FileSmsSettings.load

    def validate(self, env: Mapping[str, str]) -> None:
        return None

    def load(self, env: Mapping[str, str]) -> FileSmsSettings:
        return self.loader(env)


FILE_SMS_CONFIG_SPEC = FileSmsProviderConfigSpec()
