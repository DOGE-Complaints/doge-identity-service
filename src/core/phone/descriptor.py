from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from core.config.errors import ConfigError
from core.phone.base import SmsSenderPort
from core.phone.runtime import SmsProviderRuntime
from core.providers.config_spec import ProviderConfigSpec


class SmsProviderNotRegisteredError(ConfigError):
    """Raised when an SMS provider name is not registered in the SMS registry."""


@dataclass(frozen=True)
class SmsProviderDescriptor:
    name: str
    config_spec: ProviderConfigSpec
    build: Callable[[SmsProviderRuntime], SmsSenderPort]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("SmsProviderDescriptor.name must be non-empty")
