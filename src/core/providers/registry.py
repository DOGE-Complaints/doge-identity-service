from __future__ import annotations

from core.config.schema import AppConfig
from core.providers.base import EIDProviderPort
from core.providers.descriptor import ProviderNotRegisteredError


class EIDProviderRegistry:
    def __init__(self, providers: dict[str, EIDProviderPort]) -> None:
        self._providers = dict(providers)

    @property
    def registered_names(self) -> frozenset[str]:
        return frozenset(self._providers)

    def get(self, name: str) -> EIDProviderPort:
        if name not in self._providers:
            available = ", ".join(sorted(self._providers))
            raise ProviderNotRegisteredError(
                f"eID provider {name!r} is not registered; доступны: {available}"
            )
        return self._providers[name]

    def get_active(self, config: AppConfig) -> EIDProviderPort:
        return self.get(config.eid_provider)
