from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

import httpx

from core.config.schema import AppConfig
from core.domain.contracts import VerificationSessionStore
from core.security.oidc import OidcToolkit
from core.security.session_secret import SessionSecretBox


@dataclass(frozen=True)
class ProviderRuntime:
    config: AppConfig
    session_store: VerificationSessionStore
    http_client: httpx.Client | None = None
    secret_box: SessionSecretBox | None = None
    oidc: OidcToolkit | None = None
    clock: Callable[[], datetime] | None = None
