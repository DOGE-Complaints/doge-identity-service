from __future__ import annotations

from core.config.schema import AppConfig
from core.phone.base import SmsSenderPort
from core.phone.descriptor import SmsProviderNotRegisteredError


class SmsSenderRegistry:
    def __init__(self, providers: dict[str, SmsSenderPort]) -> None:
        self._providers = dict(providers)

    @property
    def registered_names(self) -> frozenset[str]:
        return frozenset(self._providers)

    def get(self, name: str) -> SmsSenderPort:
        if name not in self._providers:
            available = ", ".join(sorted(self._providers))
            raise SmsProviderNotRegisteredError(
                f"SMS provider {name!r} is not registered; доступны: {available}"
            )
        return self._providers[name]

    def get_active(self, config: AppConfig) -> SmsSenderPort:
        return self.get(config.sms_provider)
