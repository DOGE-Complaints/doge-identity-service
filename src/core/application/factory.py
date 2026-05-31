from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from core.config.schema import AppConfig
    from core.domain.contracts import (
        BearerTokenAuth,
        EIDAuditLogRepository,
        HealthRepository,
        OAuthClientStore,
        OAuthTokenService,
        ProfileRepository,
        StoryDraftRepository,
        SupabaseJwtValidator,
        VerificationSessionStore,
    )
    from core.providers.registry import EIDProviderRegistry


@runtime_checkable
class ServiceFactory(Protocol):
    @property
    def config(self) -> AppConfig: ...

    def get_health_repository(self) -> HealthRepository: ...

    def get_supabase_jwt_validator(self) -> SupabaseJwtValidator: ...

    def get_bearer_token_auth(self) -> BearerTokenAuth: ...

    def get_profile_repository(self) -> ProfileRepository: ...

    def get_verification_session_store(self) -> VerificationSessionStore: ...

    def get_eid_audit_log_repository(self) -> EIDAuditLogRepository: ...

    def get_eid_provider_registry(self) -> EIDProviderRegistry: ...

    def get_oauth_client_store(self) -> OAuthClientStore: ...

    def get_oauth_token_service(self) -> OAuthTokenService: ...

    def get_story_draft_repository(self) -> StoryDraftRepository: ...
