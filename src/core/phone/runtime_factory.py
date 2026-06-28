from __future__ import annotations

from collections.abc import Mapping
from typing import Any

import httpx

from core.config.providers import resolve_config_env
from core.config.schema import AppConfig
from core.phone.registry_builder import get_sms_provider_descriptor
from core.phone.runtime import SmsProviderRuntime


def _needs_sms_http_client(config: AppConfig) -> bool:
    return config.sms_provider not in {"mock", "file"}


def build_sms_provider_runtime(
    *,
    config: AppConfig,
    env: Mapping[str, str] | None = None,
) -> SmsProviderRuntime:
    http_client: httpx.Client | None = None
    settings: dict[str, Any] = {}
    config_env = resolve_config_env(env)
    descriptor = get_sms_provider_descriptor(config.sms_provider)

    if descriptor is not None and config.sms_provider != "mock":
        settings[descriptor.name] = descriptor.config_spec.load(config_env)

    if _needs_sms_http_client(config):
        http_client = httpx.Client(timeout=float(config.request_timeout_s))

    return SmsProviderRuntime(config=config, http_client=http_client, settings=settings)
