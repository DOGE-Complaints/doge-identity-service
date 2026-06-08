from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import httpx

from core.config.schema import AppConfig
from core.domain.contracts import VerificationSessionStore


@dataclass(frozen=True)
class ProviderRuntime:
    config: AppConfig
    session_store: VerificationSessionStore
    http_client: httpx.Client | None = None
    secret_box: Any | None = None
    oidc: Any | None = None
    clock: Callable[[], datetime] | None = None
