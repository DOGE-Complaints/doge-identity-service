from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from core.config.schema import AppConfig

if TYPE_CHECKING:
    from core.api.security import BearerTokenAuth


@dataclass(frozen=True)
class ApiDependencies:
    config: AppConfig
    bearer_token_auth: BearerTokenAuth
    db_backend: str
    db_ready: bool
    db_checks: dict[str, Any] = field(default_factory=dict)


def build_api_dependencies(config: AppConfig) -> ApiDependencies:
    from core.api.security import StubBearerTokenAuth

    db_backend = config.db_backend
    db_ready = db_backend == "in_memory"
    return ApiDependencies(
        config=config,
        bearer_token_auth=StubBearerTokenAuth(),
        db_backend=db_backend,
        db_ready=db_ready,
        db_checks={},
    )
