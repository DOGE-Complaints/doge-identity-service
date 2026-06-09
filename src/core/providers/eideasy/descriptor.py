from __future__ import annotations

from core.providers.base import EIDProviderPort
from core.providers.descriptor import EIDProviderDescriptor, ProviderNotRegisteredError
from core.providers.eideasy.config import EIDEASY_CONFIG_SPEC
from core.providers.runtime import ProviderRuntime


def _build_eideasy_provider_stub(_runtime: ProviderRuntime) -> EIDProviderPort:
    raise ProviderNotRegisteredError(
        "eID Easy provider is not implemented yet (STORY-IDS-EID-02)"
    )


EIDEASY_EID_DESCRIPTOR = EIDProviderDescriptor(
    name="eideasy",
    config_spec=EIDEASY_CONFIG_SPEC,
    build=_build_eideasy_provider_stub,
)
