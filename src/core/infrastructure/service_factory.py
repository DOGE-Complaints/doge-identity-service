from __future__ import annotations

from dataclasses import dataclass

from core.config.schema import AppConfig
from core.domain.contracts import (
    BearerTokenAuth,
    EIDAuditLogRepository,
    HealthRepository,
    OAuthClientStore,
    OAuthTokenService,
    PhoneAuditLogRepository,
    PhoneVerificationSessionStore,
    ProfileRepository,
    SupabaseJwtValidator,
    VerificationSessionStore,
)
from core.domain.contracts import AuthorizationRequestStore
from core.phone.registry import SmsSenderRegistry
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
    oauth_authorization_request_store: AuthorizationRequestStore
    supabase_jwt_validator: SupabaseJwtValidator
    bearer_token_auth: BearerTokenAuth
    eid_provider_registry: EIDProviderRegistry
    sms_sender_registry: SmsSenderRegistry
    phone_verification_session_store: PhoneVerificationSessionStore
    phone_audit_log_repository: PhoneAuditLogRepository

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

    def get_oauth_authorization_request_store(self) -> AuthorizationRequestStore:
        return self.oauth_authorization_request_store

    def get_sms_sender_registry(self) -> SmsSenderRegistry:
        return self.sms_sender_registry

    def get_phone_verification_session_store(self) -> PhoneVerificationSessionStore:
        return self.phone_verification_session_store

    def get_phone_audit_log_repository(self) -> PhoneAuditLogRepository:
        return self.phone_audit_log_repository
