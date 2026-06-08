from __future__ import annotations

import httpx

from core.config.schema import AppConfig
from core.domain.contracts import VerificationSessionStore
from core.providers.runtime import ProviderRuntime


def _needs_provider_http_client(config: AppConfig) -> bool:
    return config.eid_provider != "mock"


def build_provider_runtime(
    *,
    config: AppConfig,
    session_store: VerificationSessionStore,
) -> ProviderRuntime:
    http_client: httpx.Client | None = None
    if _needs_provider_http_client(config):
        http_client = httpx.Client(timeout=float(config.oidc_request_timeout_s))

    return ProviderRuntime(
        config=config,
        session_store=session_store,
        http_client=http_client,
        secret_box=None,
        oidc=None,
        clock=None,
    )
