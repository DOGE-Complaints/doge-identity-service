from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final

from core.providers.config_spec import ProviderConfigSpec, _env_value

EIDEASY_REQUIRED_ENV: Final = (
    "EIDEASY_CLIENT_ID",
    "EIDEASY_CLIENT_SECRET",
    "EIDEASY_REDIRECT_URI",
)


@dataclass(frozen=True)
class EideasySettings:
    client_id: str
    client_secret: str
    redirect_uri: str

    @classmethod
    def load(cls, env: Mapping[str, str]) -> EideasySettings:
        return cls(
            client_id=_env_value(env, "EIDEASY_CLIENT_ID"),
            client_secret=_env_value(env, "EIDEASY_CLIENT_SECRET"),
            redirect_uri=_env_value(env, "EIDEASY_REDIRECT_URI"),
        )


EIDEASY_CONFIG_SPEC = ProviderConfigSpec(
    required=EIDEASY_REQUIRED_ENV,
    optional_defaults={},
    loader=EideasySettings.load,
)
