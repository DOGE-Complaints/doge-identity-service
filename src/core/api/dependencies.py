from __future__ import annotations

from dataclasses import dataclass, field

from core.config import provide_app_config
from core.config.schema import AppConfig
from core.domain.contracts import (
    AuthorizationRequestStore,
    BearerTokenAuth,
    EIDAuditLogRepository,
    OAuthClientStore,
    OAuthTokenService,
    PhoneAuditLogRepository,
    PhoneVerificationSessionStore,
    ProfileRepository,
    SupabaseJwtValidator,
    VerificationSessionStore,
)
from core.phone.registry import SmsSenderRegistry
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
    "oauth_authorization_request_store",
    "sms_sender_registry",
    "phone_verification_session_store",
    "phone_audit_log_repository",
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
    oauth_authorization_request_store: AuthorizationRequestStore | None = None
    sms_sender_registry: SmsSenderRegistry | None = None
    phone_verification_session_store: PhoneVerificationSessionStore | None = None
    phone_audit_log_repository: PhoneAuditLogRepository | None = None


HandlerDependencies = ApiDependencies


def build_api_dependencies() -> ApiDependencies:
    """
    Build the DI container. Called once per process via lru_cache (in asgi_app).
    """
    from core.infrastructure.db_supabase import SupabaseDatabase
    from core.infrastructure.providers import provide_service_factory

    config = provide_app_config()
    db_backend = config.db_backend
    db_checks: dict[str, bool] = {}
    if db_backend == "in_memory":
        db_ready = True
    elif db_backend == "supabase":
        # Startup probe uses a separate SupabaseDatabase instance from
        # provide_service_factory() (providers.py supabase_db). Unifying them is
        # out of scope here; see EPIC-IDS-06 / re-audit S3-1.
        health_db = SupabaseDatabase.from_http(
            supabase_url=config.supabase_url,
            service_role_key=config.supabase_service_role,
            timeout_s=float(config.request_timeout_s or 15),
        )
        db_checks = {
            "connectivity": health_db.healthcheck(),
            "schema": health_db.required_tables_ready(),
            "columns": health_db.required_columns_ready(),
            "provider_state": health_db.provider_state_ready(),
            "policy_probe": health_db.service_role_policy_probe(),
        }
        db_ready = all(db_checks.values())
    else:
        db_ready = False

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
        oauth_authorization_request_store=service_factory.get_oauth_authorization_request_store(),
        sms_sender_registry=service_factory.get_sms_sender_registry(),
        phone_verification_session_store=service_factory.get_phone_verification_session_store(),
        phone_audit_log_repository=service_factory.get_phone_audit_log_repository(),
    )
