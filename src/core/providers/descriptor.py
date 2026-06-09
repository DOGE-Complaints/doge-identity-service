from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from core.config.errors import ConfigError
from core.providers.base import EIDProviderPort
from core.providers.config_spec import ProviderConfigSpec
from core.providers.runtime import ProviderRuntime


class ProviderNotRegisteredError(ConfigError):
    """Raised when a provider name is not registered in the eID registry."""


@dataclass(frozen=True)
class EIDProviderDescriptor:
    name: str
    config_spec: ProviderConfigSpec
    build: Callable[[ProviderRuntime], EIDProviderPort]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("EIDProviderDescriptor.name must be non-empty")
