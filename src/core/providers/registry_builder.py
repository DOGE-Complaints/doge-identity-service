from __future__ import annotations

from core.providers.authentigate.descriptor import AUTHENTIGATE_EID_DESCRIPTOR
from core.providers.descriptor import EIDProviderDescriptor
from core.providers.eideasy.descriptor import EIDEASY_EID_DESCRIPTOR
from core.providers.mock.descriptor import MOCK_EID_DESCRIPTOR
from core.providers.registry import EIDProviderRegistry
from core.providers.runtime import ProviderRuntime

ALL_EID_PROVIDER_DESCRIPTORS: tuple[EIDProviderDescriptor, ...] = (
    MOCK_EID_DESCRIPTOR,
    EIDEASY_EID_DESCRIPTOR,
    AUTHENTIGATE_EID_DESCRIPTOR,
)

_DESCRIPTOR_BY_NAME = {descriptor.name: descriptor for descriptor in ALL_EID_PROVIDER_DESCRIPTORS}


def registered_eid_provider_names() -> frozenset[str]:
    return frozenset(_DESCRIPTOR_BY_NAME)


def get_provider_descriptor(name: str) -> EIDProviderDescriptor | None:
    return _DESCRIPTOR_BY_NAME.get(name)


def build_registry(runtime: ProviderRuntime) -> EIDProviderRegistry:
    active_name = runtime.config.eid_provider
    names_to_register = {"mock"}
    if active_name != "mock":
        names_to_register.add(active_name)

    providers = {}
    for name in names_to_register:
        descriptor = _DESCRIPTOR_BY_NAME.get(name)
        if descriptor is None:
            continue
        providers[name] = descriptor.build(runtime)

    return EIDProviderRegistry(providers)
