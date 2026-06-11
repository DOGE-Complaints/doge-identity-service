from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import httpx

from core.config.schema import AppConfig


@dataclass(frozen=True)
class SmsProviderRuntime:
    config: AppConfig
    http_client: httpx.Client | None = None
    settings: dict[str, Any] = field(default_factory=dict)
