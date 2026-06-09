"""Providers layer package."""

from core.providers.base import (
    EIDProviderError,
    EIDProviderPort,
    EIDStartResult,
    EIDVerificationResult,
)
from core.providers.config_spec import ProviderConfigSpec
from core.providers.descriptor import EIDProviderDescriptor, ProviderNotRegisteredError
from core.providers.registry import EIDProviderRegistry
from core.providers.registry_builder import ALL_EID_PROVIDER_DESCRIPTORS, build_registry, get_provider_descriptor
from core.providers.runtime import ProviderRuntime
from core.providers.runtime_factory import build_provider_runtime

__all__ = [
    "ALL_EID_PROVIDER_DESCRIPTORS",
    "EIDProviderDescriptor",
    "EIDProviderError",
    "EIDProviderPort",
    "EIDProviderRegistry",
    "EIDStartResult",
    "EIDVerificationResult",
    "ProviderConfigSpec",
    "ProviderNotRegisteredError",
    "ProviderRuntime",
    "build_provider_runtime",
    "build_registry",
    "get_provider_descriptor",
]
