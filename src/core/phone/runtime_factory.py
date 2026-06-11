from __future__ import annotations

from core.config.schema import AppConfig
from core.phone.runtime import SmsProviderRuntime


def build_sms_provider_runtime(*, config: AppConfig) -> SmsProviderRuntime:
    return SmsProviderRuntime(config=config)
