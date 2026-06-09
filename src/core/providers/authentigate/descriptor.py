from __future__ import annotations

from core.providers.authentigate.config import AUTHENTIGATE_CONFIG_SPEC
from core.providers.base import EIDProviderPort
from core.providers.descriptor import EIDProviderDescriptor, ProviderNotRegisteredError
from core.providers.runtime import ProviderRuntime


def _build_authentigate_provider_stub(_runtime: ProviderRuntime) -> EIDProviderPort:
    raise ProviderNotRegisteredError(
        "Authentigate eID provider is not implemented yet (STORY-IDS-EID-02)"
    )


AUTHENTIGATE_EID_DESCRIPTOR = EIDProviderDescriptor(
    name="authentigate",
    config_spec=AUTHENTIGATE_CONFIG_SPEC,
    build=_build_authentigate_provider_stub,
)
