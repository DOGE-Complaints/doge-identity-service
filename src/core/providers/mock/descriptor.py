from __future__ import annotations

from core.providers.base import EIDProviderPort
from core.providers.descriptor import EIDProviderDescriptor, empty_config_spec
from core.providers.mock.mock_provider import MockEIDProvider
from core.providers.runtime import ProviderRuntime


def _build_mock_provider(runtime: ProviderRuntime) -> EIDProviderPort:
    return MockEIDProvider(runtime.session_store)


MOCK_EID_DESCRIPTOR = EIDProviderDescriptor(
    name="mock",
    config_spec=empty_config_spec(),
    build=_build_mock_provider,
)
