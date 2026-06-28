from __future__ import annotations

import logging

from core.api.security import CompositeBearerTokenAuth, ServiceTokenAuth, SupabaseJwtBearerTokenAuth
from core.auth.supabase_validator import SupabaseJwtValidatorImpl
from core.config.providers import provide_app_config, resolve_config_env
from core.config.schema import AppConfig
from core.infrastructure.db_supabase import (
    SupabaseAuthorizationRequestStore,
    SupabaseDatabase,
    SupabaseEIDAuditLogRepository,
    SupabaseHealthRepository,
    SupabaseOAuthClientStore,
    SupabaseOAuthTokenService,
    SupabasePhoneAuditLogRepository,
    SupabasePhoneVerificationSessionStore,
    SupabaseProfileRepository,
    SupabaseVerificationSessionStore,
)
from core.infrastructure.repositories import (
    InMemoryAuthorizationRequestStore,
    InMemoryEIDAuditLogRepository,
    InMemoryHealthRepository,
    InMemoryOAuthClientStore,
    InMemoryOAuthTokenService,
    InMemoryPhoneAuditLogRepository,
    InMemoryPhoneVerificationSessionStore,
    InMemoryProfileRepository,
    InMemoryVerificationSessionStore,
)
from core.infrastructure.service_factory import DefaultServiceFactory
from core.phone.registry_builder import build_sms_registry
from core.phone.runtime_factory import build_sms_provider_runtime
from core.providers.registry_builder import build_registry
from core.providers.runtime_factory import build_provider_runtime

logger = logging.getLogger(__name__)

__all__ = ["provide_service_factory"]


def _build_in_memory_repositories(
    config: AppConfig,
) -> tuple[
    InMemoryHealthRepository,
    InMemoryProfileRepository,
    InMemoryVerificationSessionStore,
    InMemoryEIDAuditLogRepository,
    InMemoryOAuthClientStore,
]:
    return (
        InMemoryHealthRepository(),
        InMemoryProfileRepository(),
        InMemoryVerificationSessionStore(),
        InMemoryEIDAuditLogRepository(),
        InMemoryOAuthClientStore.from_config(config),
    )


def provide_service_factory(config: AppConfig | None = None) -> DefaultServiceFactory:
    resolved_config = config or provide_app_config()

    if resolved_config.db_backend == "in_memory":
        (
            health_repository,
            profile_repository,
            verification_session_store,
            eid_audit_log_repository,
            oauth_client_store,
        ) = _build_in_memory_repositories(resolved_config)
        oauth_token_service = InMemoryOAuthTokenService(
            config=resolved_config,
            client_store=oauth_client_store,
        )
        oauth_authorization_request_store = InMemoryAuthorizationRequestStore()
        phone_verification_session_store = InMemoryPhoneVerificationSessionStore()
        phone_audit_log_repository = InMemoryPhoneAuditLogRepository()
    elif resolved_config.db_backend == "supabase":
        if not resolved_config.supabase_url or not resolved_config.supabase_service_role:
            raise ValueError(
                "DB_BACKEND=supabase requires SUPABASE_URL and SUPABASE_SERVICE_ROLE"
            )
        supabase_db = SupabaseDatabase.from_http(
            supabase_url=resolved_config.supabase_url,
            service_role_key=resolved_config.supabase_service_role,
            timeout_s=float(resolved_config.request_timeout_s or 15),
        )
        health_repository = SupabaseHealthRepository(supabase_db)
        profile_repository = SupabaseProfileRepository(supabase_db)
        verification_session_store = SupabaseVerificationSessionStore(supabase_db)
        eid_audit_log_repository = SupabaseEIDAuditLogRepository(supabase_db)
        oauth_client_store = SupabaseOAuthClientStore(
            supabase_db,
            fallback_config=resolved_config,
        )
        oauth_token_service = SupabaseOAuthTokenService(
            supabase_db,
            config=resolved_config,
            client_store=oauth_client_store,
        )
        oauth_authorization_request_store = SupabaseAuthorizationRequestStore(supabase_db)
        phone_verification_session_store = SupabasePhoneVerificationSessionStore(supabase_db)
        phone_audit_log_repository = SupabasePhoneAuditLogRepository(supabase_db)
    else:
        raise ValueError(f"Unsupported db_backend: {resolved_config.db_backend}")

    supabase_jwt_validator = SupabaseJwtValidatorImpl(
        jwt_secret=resolved_config.supabase_jwt_secret or "test-secret-for-demo",
        supabase_url=resolved_config.supabase_url or "https://demo.local",
        request_timeout_s=float(resolved_config.request_timeout_s or 15),
    )
    bearer_token_auth = CompositeBearerTokenAuth(
        supabase_auth=SupabaseJwtBearerTokenAuth(validator=supabase_jwt_validator),
        oauth_token_service=oauth_token_service,
    )
    service_token_auth = ServiceTokenAuth.from_secret(resolved_config.service_api_token)

    provider_runtime = build_provider_runtime(
        config=resolved_config,
        session_store=verification_session_store,
    )
    registry = build_registry(provider_runtime)
    merged_env = resolve_config_env()
    sms_sender_registry = build_sms_registry(
        build_sms_provider_runtime(config=resolved_config, env=merged_env)
    )

    return DefaultServiceFactory(
        config=resolved_config,
        health_repository=health_repository,
        profile_repository=profile_repository,
        verification_session_store=verification_session_store,
        eid_audit_log_repository=eid_audit_log_repository,
        oauth_client_store=oauth_client_store,
        oauth_token_service=oauth_token_service,
        oauth_authorization_request_store=oauth_authorization_request_store,
        supabase_jwt_validator=supabase_jwt_validator,
        bearer_token_auth=bearer_token_auth,
        service_token_auth=service_token_auth,
        eid_provider_registry=registry,
        sms_sender_registry=sms_sender_registry,
        phone_verification_session_store=phone_verification_session_store,
        phone_audit_log_repository=phone_audit_log_repository,
    )
