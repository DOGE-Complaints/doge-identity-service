from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from core.config import provide_app_config
from core.config.schema import AppConfig

if TYPE_CHECKING:
    from core.api.security import BearerTokenAuth

# EPIC-IDS-04 optional identity service slots (see epic §3 field table).
EPIC_IDS_04_OPTIONAL_FIELDS: tuple[str, ...] = (
    "supabase_jwt_validator",
    "profile_repository",
    "verification_session_store",
    "eid_audit_log_repository",
    "eid_provider_registry",
    "oauth_client_store",
    "oauth_token_service",
    "story_draft_repository",
)


@dataclass(frozen=True)
class ApiDependencies:
    # ── Always present ──────────────────────────────────────────────
    config: AppConfig
    bearer_token_auth: BearerTokenAuth

    # ── DB state ───────────────────────────────────────────────────
    db_backend: str
    db_ready: bool
    db_checks: dict[str, bool] = field(default_factory=dict)

    # ── Identity services (None in EPIC-IDS-03, filled in EPIC-IDS-04) ──
    supabase_jwt_validator: object | None = None
    profile_repository: object | None = None
    verification_session_store: object | None = None
    eid_audit_log_repository: object | None = None
    eid_provider_registry: object | None = None
    oauth_client_store: object | None = None
    oauth_token_service: object | None = None
    story_draft_repository: object | None = None


HandlerDependencies = ApiDependencies


def build_api_dependencies() -> ApiDependencies:
    """
    Build the DI container. Called once per process via lru_cache (in asgi_app).
    """
    from core.api.security import StubBearerTokenAuth

    config = provide_app_config()
    db_backend = config.db_backend
    # TODO EPIC-IDS-05: run 5-level Supabase healthchecks
    db_checks: dict[str, bool] = {}
    # degraded ready for supabase until EPIC-IDS-05 (epic §9)
    db_ready = db_backend == "in_memory"

    # TODO EPIC-IDS-04: replace with provide_service_factory(...)
    bearer_token_auth = StubBearerTokenAuth()  # replaced in EPIC-IDS-04
    return ApiDependencies(
        config=config,
        bearer_token_auth=bearer_token_auth,
        db_backend=db_backend,
        db_ready=db_ready,
        db_checks=db_checks,
    )

    # EPIC-IDS-04 will replace this block:
    # from core.infrastructure.providers import provide_service_factory
    # service_factory = provide_service_factory(config)
    # return ApiDependencies(
    #     config=config,
    #     bearer_token_auth=service_factory.get_bearer_token_auth(),
    #     db_backend=config.db_backend,
    #     db_ready=db_ready,
    #     db_checks=db_checks,
    #     supabase_jwt_validator=service_factory.get_supabase_jwt_validator(),
    #     profile_repository=service_factory.get_profile_repository(),
    #     verification_session_store=service_factory.get_verification_session_store(),
    #     eid_audit_log_repository=service_factory.get_eid_audit_log_repository(),
    #     eid_provider_registry=service_factory.get_eid_provider_registry(),
    #     oauth_client_store=service_factory.get_oauth_client_store(),
    #     oauth_token_service=service_factory.get_oauth_token_service(),
    #     story_draft_repository=service_factory.get_story_draft_repository(),
    # )
