from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final

from core.config.eid_provider_defaults import DEFAULT_AUTHENTIGATE_SCOPES
from core.providers.config_spec import ProviderConfigSpec, _env_value
DEFAULT_AUTHENTIGATE_ACR_VALUES: Final = "sid_ee mid_ee idcard_ee"
DEFAULT_AUTHENTIGATE_UI_LOCALES: Final = "et en"
DEFAULT_AUTHENTIGATE_COUNTRY: Final = "EE"

AUTHENTIGATE_REQUIRED_ENV: Final = (
    "AUTHENTIGATE_ISSUER",
    "AUTHENTIGATE_CLIENT_ID",
    "AUTHENTIGATE_CLIENT_SECRET",
    "AUTHENTIGATE_REDIRECT_URI",
)


def _discovery_url_from_issuer(issuer: str) -> str:
    return f"{issuer.rstrip('/')}/.well-known/openid-configuration"


@dataclass(frozen=True)
class AuthentigateSettings:
    issuer: str
    discovery_url: str
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: str
    acr_values: str
    ui_locales: str
    country: str

    @classmethod
    def load(cls, env: Mapping[str, str]) -> AuthentigateSettings:
        issuer = _env_value(env, "AUTHENTIGATE_ISSUER")
        discovery_url = _env_value(
            env,
            "AUTHENTIGATE_DISCOVERY_URL",
            _discovery_url_from_issuer(issuer) if issuer else "",
        )
        return cls(
            issuer=issuer,
            discovery_url=discovery_url,
            client_id=_env_value(env, "AUTHENTIGATE_CLIENT_ID"),
            client_secret=_env_value(env, "AUTHENTIGATE_CLIENT_SECRET"),
            redirect_uri=_env_value(env, "AUTHENTIGATE_REDIRECT_URI"),
            scopes=_env_value(env, "AUTHENTIGATE_SCOPES", DEFAULT_AUTHENTIGATE_SCOPES),
            acr_values=_env_value(env, "AUTHENTIGATE_ACR_VALUES", DEFAULT_AUTHENTIGATE_ACR_VALUES),
            ui_locales=_env_value(env, "AUTHENTIGATE_UI_LOCALES", DEFAULT_AUTHENTIGATE_UI_LOCALES),
            country=_env_value(env, "AUTHENTIGATE_COUNTRY", DEFAULT_AUTHENTIGATE_COUNTRY),
        )


AUTHENTIGATE_CONFIG_SPEC = ProviderConfigSpec(
    required=AUTHENTIGATE_REQUIRED_ENV,
    optional_defaults={
        "AUTHENTIGATE_SCOPES": DEFAULT_AUTHENTIGATE_SCOPES,
        "AUTHENTIGATE_ACR_VALUES": DEFAULT_AUTHENTIGATE_ACR_VALUES,
        "AUTHENTIGATE_UI_LOCALES": DEFAULT_AUTHENTIGATE_UI_LOCALES,
        "AUTHENTIGATE_COUNTRY": DEFAULT_AUTHENTIGATE_COUNTRY,
    },
    loader=AuthentigateSettings.load,
)
