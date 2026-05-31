from __future__ import annotations

from core.config.schema import AppConfig
from core.providers.base import EIDProviderPort


class EIDProviderRegistry:
    def __init__(self, providers: dict[str, EIDProviderPort]) -> None:
        self._providers = dict(providers)

    def get(self, name: str) -> EIDProviderPort:
        if name not in self._providers:
            raise KeyError(name)
        return self._providers[name]

    def get_active(self, config: AppConfig) -> EIDProviderPort:
        return self.get(config.eid_provider)
