from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


class JwtValidationError(Exception):
    """Raised when Supabase JWT validation fails (Story 5 maps to UnauthorizedError)."""


class ProfileConflictError(Exception):
    """Raised when verified_person_hash or verified_phone_hash unique constraint conflicts."""


@dataclass(frozen=True)
class UserClaims:
    supabase_user_id: str
    email: str | None
    role: str


@dataclass(frozen=True)
class ProfileRecord:
    id: str
    supabase_user_id: str
    display_name: str | None
    avatar_url: str | None
    eid_verified: bool
    verified_person_hash: str | None
    eid_provider: str | None
    eid_method: str | None
    eid_country: str | None
    eid_verified_at: datetime | None
    phone_verified: bool
    verified_phone_hash: str | None
    phone_provider: str | None
    phone_dial_prefix: str | None
    phone_verified_at: datetime | None
    wallet_address: str | None
    wallet_linked_at: datetime | None
    wallet_signature_verified_at: datetime | None
    wallet_signature_scheme: str | None
    wallet_chain_id: str | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class VerificationSession:
    id: str
    supabase_user_id: str
    state: str
    nonce: str | None
    code_verifier_encrypted: str | None
    code_verifier_hash: str | None
    return_context: str | None
    return_url: str | None
    requested_action: str | None
    status: str
    created_at: datetime
    expires_at: datetime
    provider: str
    # Shallow mutation of provider_session_data is allowed in InMemory-only epic; EPIC-IDS-05 may tighten.
    provider_session_data: dict[str, object]


@dataclass(frozen=True)
class PhoneVerificationSession:
    id: str
    supabase_user_id: str
    phone_hash: str
    dial_prefix: str
    code_hash: str
    status: str
    attempts: int
    created_at: datetime
    expires_at: datetime
    provider: str
    provider_message_id: str | None
    delivery_status: str | None = None
    delivery_updated_at: datetime | None = None


@dataclass(frozen=True)
class PhoneVerificationResult:
    provider: str
    dial_prefix: str
    subject_hash: str
    verified_at: datetime


@dataclass(frozen=True)
class PhoneAuditEvent:
    id: str
    supabase_user_id: str | None
    event_type: str
    provider: str | None
    success: bool
    failure_reason: str | None
    request_id: str | None
    ip_hash: str | None
    user_agent_hash: str | None
    created_at: datetime


@dataclass(frozen=True)
class EIDAuditEvent:
    id: str
    supabase_user_id: str | None
    event_type: str
    provider: str | None
    method: str | None
    success: bool
    failure_reason: str | None
    request_id: str | None
    ip_hash: str | None
    user_agent_hash: str | None
    created_at: datetime


@dataclass(frozen=True)
class OAuthClient:
    client_id: str
    client_secret_hash: str
    redirect_uri: str
    # list allows shallow mutation; frozen=True blocks reassignment only (see test_frozen_models_allow_shallow_list_mutation).
    scopes: list[str]


@dataclass(frozen=True)
class OAuthTokenClaims:
    sub: str
    # list allows shallow mutation; frozen=True blocks reassignment only (see test_frozen_models_allow_shallow_list_mutation).
    scopes: list[str]
    exp: int
    client_id: str


@dataclass(frozen=True)
class AuthorizationRequest:
    oauth_request_id: str
    client_id: str
    redirect_uri: str
    scopes: list[str]
    state: str
    code_challenge: str | None
    code_challenge_method: str | None
    created_at: datetime
    expires_at: datetime
    requested_action: str | None = None
    return_context: str | None = None

