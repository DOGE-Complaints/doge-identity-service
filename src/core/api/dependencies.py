from __future__ import annotations

from dataclasses import dataclass, field

from core.config import provide_app_config
from core.config.schema import AppConfig
from core.domain.contracts import (
    BearerTokenAuth,
    EIDAuditLogRepository,
    OAuthClientStore,
    OAuthTokenService,
    ProfileRepository,
    StoryDraftRepository,
    SupabaseJwtValidator,
    VerificationSessionStore,
)
from core.providers.registry import EIDProviderRegistry

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

    # ── Identity services (filled via provide_service_factory in EPIC-IDS-04) ──
    supabase_jwt_validator: SupabaseJwtValidator | None = None
    profile_repository: ProfileRepository | None = None
    verification_session_store: VerificationSessionStore | None = None
    eid_audit_log_repository: EIDAuditLogRepository | None = None
    eid_provider_registry: EIDProviderRegistry | None = None
    oauth_client_store: OAuthClientStore | None = None
    oauth_token_service: OAuthTokenService | None = None
    story_draft_repository: StoryDraftRepository | None = None


HandlerDependencies = ApiDependencies


def build_api_dependencies() -> ApiDependencies:
    """
    Build the DI container. Called once per process via lru_cache (in asgi_app).
    """
    from core.infrastructure.providers import provide_service_factory

    config = provide_app_config()
    db_backend = config.db_backend
    # TODO EPIC-IDS-05: run 5-level Supabase healthchecks
    db_checks: dict[str, bool] = {}
    # degraded ready for supabase until EPIC-IDS-05 (epic §9)
    db_ready = db_backend == "in_memory"

    service_factory = provide_service_factory(config)
    return ApiDependencies(
        config=config,
        bearer_token_auth=service_factory.get_bearer_token_auth(),
        db_backend=db_backend,
        db_ready=db_ready,
        db_checks=db_checks,
        supabase_jwt_validator=service_factory.get_supabase_jwt_validator(),
        profile_repository=service_factory.get_profile_repository(),
        verification_session_store=service_factory.get_verification_session_store(),
        eid_audit_log_repository=service_factory.get_eid_audit_log_repository(),
        eid_provider_registry=service_factory.get_eid_provider_registry(),
        oauth_client_store=service_factory.get_oauth_client_store(),
        oauth_token_service=service_factory.get_oauth_token_service(),
        story_draft_repository=service_factory.get_story_draft_repository(),
    )
