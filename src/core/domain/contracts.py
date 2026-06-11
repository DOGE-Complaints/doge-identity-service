from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Mapping, Protocol, runtime_checkable

if TYPE_CHECKING:
    from core.domain.models import (
        EIDAuditEvent,
        OAuthClient,
        OAuthTokenClaims,
        PhoneVerificationSession,
        ProfileRecord,
        UserClaims,
        VerificationSession,
    )


@runtime_checkable
class HealthRepository(Protocol):
    def ping(self) -> bool: ...


@runtime_checkable
class ProfileRepository(Protocol):
    def get_by_supabase_user_id(self, user_id: str) -> ProfileRecord | None: ...

    def get_by_verified_person_hash(self, hash_: str) -> ProfileRecord | None: ...

    def get_by_verified_phone_hash(self, hash_: str) -> ProfileRecord | None: ...

    def upsert(self, profile: ProfileRecord) -> ProfileRecord: ...

    def attach_eid_verification(
        self,
        user_id: str,
        *,
        provider: str,
        country: str,
        method: str,
        verified_person_hash: str,
        verified_at: datetime,
    ) -> ProfileRecord: ...

    def attach_phone_verification(
        self,
        user_id: str,
        *,
        provider: str,
        dial_prefix: str,
        verified_phone_hash: str,
        verified_at: datetime,
        one_account_per_number: bool,
    ) -> ProfileRecord: ...


@runtime_checkable
class VerificationSessionStore(Protocol):
    def create(self, session: VerificationSession) -> VerificationSession: ...

    def get_by_state(self, state: str) -> VerificationSession | None: ...

    def get_by_id(self, session_id: str) -> VerificationSession | None: ...

    def mark_consumed(self, session_id: str) -> None: ...

    def mark_failed(self, session_id: str, reason: str) -> None: ...

    def expire_pending(self, now: datetime) -> int: ...


@runtime_checkable
class PhoneVerificationSessionStore(Protocol):
    def create(self, session: PhoneVerificationSession) -> PhoneVerificationSession: ...

    def get_by_id(self, session_id: str) -> PhoneVerificationSession | None: ...

    def get_active_by_user(self, supabase_user_id: str, *, now: datetime) -> PhoneVerificationSession | None: ...

    def replace(self, session: PhoneVerificationSession) -> PhoneVerificationSession: ...

    def mark_consumed(self, session_id: str) -> None: ...

    def mark_failed(self, session_id: str, reason: str) -> None: ...

    def mark_expired(self, session_id: str) -> None: ...

    def expire_pending(self, now: datetime) -> int: ...


@runtime_checkable
class EIDAuditLogRepository(Protocol):
    def log_event(self, event: EIDAuditEvent) -> None: ...

    def list_events(
        self,
        *,
        supabase_user_id: str | None = None,
        event_type: str | None = None,
        limit: int = 100,
    ) -> list[EIDAuditEvent]: ...


@runtime_checkable
class OAuthClientStore(Protocol):
    def get_client(self, client_id: str) -> OAuthClient | None: ...

    def list_clients(self) -> list[OAuthClient]: ...


@runtime_checkable
class OAuthTokenService(Protocol):
    def issue_authorization_code(
        self,
        *,
        supabase_user_id: str,
        client_id: str,
        scopes: list[str],
        redirect_uri: str,
        code_challenge: str | None = None,
        code_challenge_method: str | None = None,
    ) -> str: ...

    def issue_access_token(
        self,
        *,
        code: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        code_verifier: str | None = None,
    ) -> str: ...

    def validate_access_token(self, token: str) -> OAuthTokenClaims: ...


@runtime_checkable
class SupabaseJwtValidator(Protocol):
    def validate(self, token: str) -> UserClaims: ...


@runtime_checkable
class BearerTokenAuth(Protocol):
    def validate(self, headers: Mapping[str, str]) -> UserClaims: ...
