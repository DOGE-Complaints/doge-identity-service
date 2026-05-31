from __future__ import annotations

from dataclasses import dataclass

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


@dataclass(frozen=True)
class DefaultServiceFactory:
    config: AppConfig
    health_repository: HealthRepository
    profile_repository: ProfileRepository
    verification_session_store: VerificationSessionStore
    eid_audit_log_repository: EIDAuditLogRepository
    oauth_client_store: OAuthClientStore
    oauth_token_service: OAuthTokenService
    story_draft_repository: StoryDraftRepository
    supabase_jwt_validator: SupabaseJwtValidator
    bearer_token_auth: BearerTokenAuth
    eid_provider_registry: EIDProviderRegistry

    def get_health_repository(self) -> HealthRepository:
        return self.health_repository

    def get_supabase_jwt_validator(self) -> SupabaseJwtValidator:
        return self.supabase_jwt_validator

    def get_bearer_token_auth(self) -> BearerTokenAuth:
        return self.bearer_token_auth

    def get_profile_repository(self) -> ProfileRepository:
        return self.profile_repository

    def get_verification_session_store(self) -> VerificationSessionStore:
        return self.verification_session_store

    def get_eid_audit_log_repository(self) -> EIDAuditLogRepository:
        return self.eid_audit_log_repository

    def get_eid_provider_registry(self) -> EIDProviderRegistry:
        return self.eid_provider_registry

    def get_oauth_client_store(self) -> OAuthClientStore:
        return self.oauth_client_store

    def get_oauth_token_service(self) -> OAuthTokenService:
        return self.oauth_token_service

    def get_story_draft_repository(self) -> StoryDraftRepository:
        return self.story_draft_repository
