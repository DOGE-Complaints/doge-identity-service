from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import TypeVar

from core.config.errors import ConfigError

TSettings = TypeVar("TSettings")


def _env_value(source: Mapping[str, str], key: str, default: str = "") -> str:
    return str(source.get(key, default)).strip()


@dataclass(frozen=True)
class ProviderConfigSpec:
    required: tuple[str, ...]
    optional_defaults: dict[str, str]
    loader: Callable[[Mapping[str, str]], TSettings]

    def validate(self, env: Mapping[str, str]) -> None:
        for key in self.required:
            if not _env_value(env, key):
                raise ConfigError(f"Required env var {key!r} is missing or empty")

    def load(self, env: Mapping[str, str]) -> TSettings:
        self.validate(env)
        return self.loader(env)


def noop_provider_settings_loader(_env: Mapping[str, str]) -> None:
    return None
