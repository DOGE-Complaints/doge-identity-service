from __future__ import annotations

from core.providers.base import EIDProviderPort
from core.providers.config_spec import ProviderConfigSpec, noop_provider_settings_loader
from core.providers.descriptor import EIDProviderDescriptor
from core.providers.mock.mock_provider import MockEIDProvider
from core.providers.runtime import ProviderRuntime

MOCK_CONFIG_SPEC = ProviderConfigSpec(
    required=(),
    optional_defaults={},
    loader=noop_provider_settings_loader,
)


def _build_mock_provider(runtime: ProviderRuntime) -> EIDProviderPort:
    return MockEIDProvider(runtime.session_store)


MOCK_EID_DESCRIPTOR = EIDProviderDescriptor(
    name="mock",
    config_spec=MOCK_CONFIG_SPEC,
    build=_build_mock_provider,
)
