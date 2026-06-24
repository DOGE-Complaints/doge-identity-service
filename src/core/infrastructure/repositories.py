from __future__ import annotations

import base64
import dataclasses
import hashlib
import hmac
import json
import secrets
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from core.config.schema import AppConfig
from core.domain.models import (
    AuthorizationRequest,
    EIDAuditEvent,
    OAuthClient,
    OAuthTokenClaims,
    PhoneAuditEvent,
    PhoneVerificationSession,
    ProfileConflictError,
    ProfileRecord,
    VerificationSession,
)
from core.security.hashing import hash_secret


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


@dataclass
class _StoredAuthCode:
    supabase_user_id: str
    client_id: str
    scopes: list[str]
    redirect_uri: str
    code_challenge: str | None
    code_challenge_method: str | None
    expires_at: float
    consumed: bool = False


class InMemoryHealthRepository:
    def ping(self) -> bool:
        return True


class InMemoryProfileRepository:
    def __init__(self) -> None:
        self._by_user_id: dict[str, ProfileRecord] = {}
        self._by_verified_hash: dict[str, str] = {}
        self._by_verified_phone_hash: dict[str, str] = {}

    def get_by_supabase_user_id(self, user_id: str) -> ProfileRecord | None:
        return self._by_user_id.get(user_id)

    def get_by_verified_person_hash(self, hash_: str) -> ProfileRecord | None:
        user_id = self._by_verified_hash.get(hash_)
        if user_id is None:
            return None
        return self._by_user_id.get(user_id)

    def get_by_verified_phone_hash(self, hash_: str) -> ProfileRecord | None:
        user_id = self._by_verified_phone_hash.get(hash_)
        if user_id is None:
            return None
        return self._by_user_id.get(user_id)

    def upsert(self, profile: ProfileRecord) -> ProfileRecord:
        existing = self._by_user_id.get(profile.supabase_user_id)
        if existing is not None and existing.verified_person_hash:
            self._by_verified_hash.pop(existing.verified_person_hash, None)
        if existing is not None and existing.verified_phone_hash:
            self._by_verified_phone_hash.pop(existing.verified_phone_hash, None)
        if profile.verified_person_hash:
            owner = self._by_verified_hash.get(profile.verified_person_hash)
            if owner is not None and owner != profile.supabase_user_id:
                raise ProfileConflictError(
                    f"verified_person_hash already bound to user {owner}"
                )
            self._by_verified_hash[profile.verified_person_hash] = profile.supabase_user_id
        if profile.verified_phone_hash:
            owner = self._by_verified_phone_hash.get(profile.verified_phone_hash)
            if owner is not None and owner != profile.supabase_user_id:
                raise ProfileConflictError(
                    f"verified_phone_hash already bound to user {owner}"
                )
            self._by_verified_phone_hash[profile.verified_phone_hash] = (
                profile.supabase_user_id
            )
        self._by_user_id[profile.supabase_user_id] = profile
        return profile

    def attach_eid_verification(
        self,
        user_id: str,
        *,
        provider: str,
        country: str,
        method: str,
        verified_person_hash: str,
        verified_at: datetime,
    ) -> ProfileRecord:
        existing_owner = self._by_verified_hash.get(verified_person_hash)
        if existing_owner is not None and existing_owner != user_id:
            raise ProfileConflictError(
                f"verified_person_hash already bound to user {existing_owner}"
            )

        profile = self._by_user_id.get(user_id)
        if profile is None:
            now = _utcnow()
            profile = ProfileRecord(
                id=str(uuid.uuid4()),
                supabase_user_id=user_id,
                display_name=None,
                avatar_url=None,
                eid_verified=False,
                verified_person_hash=None,
                eid_provider=None,
                eid_method=None,
                eid_country=None,
                eid_verified_at=None,
                phone_verified=False,
                verified_phone_hash=None,
                phone_provider=None,
                phone_dial_prefix=None,
                phone_verified_at=None,
                wallet_address=None,
                wallet_linked_at=None,
                wallet_signature_verified_at=None,
                wallet_signature_scheme=None,
                wallet_chain_id=None,
                created_at=now,
                updated_at=now,
            )

        if profile.verified_person_hash and profile.verified_person_hash != verified_person_hash:
            self._by_verified_hash.pop(profile.verified_person_hash, None)

        updated = dataclasses.replace(
            profile,
            eid_verified=True,
            verified_person_hash=verified_person_hash,
            eid_provider=provider,
            eid_method=method,
            eid_country=country,
            eid_verified_at=verified_at,
            updated_at=_utcnow(),
        )
        self._by_verified_hash[verified_person_hash] = user_id
        self._by_user_id[user_id] = updated
        return updated

    def attach_phone_verification(
        self,
        user_id: str,
        *,
        provider: str,
        dial_prefix: str,
        verified_phone_hash: str,
        verified_at: datetime,
        one_account_per_number: bool,
    ) -> ProfileRecord:
        if one_account_per_number:
            existing_owner = self._by_verified_phone_hash.get(verified_phone_hash)
            if existing_owner is not None and existing_owner != user_id:
                raise ProfileConflictError(
                    f"verified_phone_hash already bound to user {existing_owner}"
                )

        profile = self._by_user_id.get(user_id)
        if profile is None:
            now = _utcnow()
            profile = ProfileRecord(
                id=str(uuid.uuid4()),
                supabase_user_id=user_id,
                display_name=None,
                avatar_url=None,
                eid_verified=False,
                verified_person_hash=None,
                eid_provider=None,
                eid_method=None,
                eid_country=None,
                eid_verified_at=None,
                phone_verified=False,
                verified_phone_hash=None,
                phone_provider=None,
                phone_dial_prefix=None,
                phone_verified_at=None,
                wallet_address=None,
                wallet_linked_at=None,
                wallet_signature_verified_at=None,
                wallet_signature_scheme=None,
                wallet_chain_id=None,
                created_at=now,
                updated_at=now,
            )

        if (
            profile.verified_phone_hash
            and profile.verified_phone_hash != verified_phone_hash
        ):
            self._by_verified_phone_hash.pop(profile.verified_phone_hash, None)

        updated = dataclasses.replace(
            profile,
            phone_verified=True,
            verified_phone_hash=verified_phone_hash,
            phone_provider=provider,
            phone_dial_prefix=dial_prefix,
            phone_verified_at=verified_at,
            updated_at=_utcnow(),
        )
        self._by_verified_phone_hash[verified_phone_hash] = user_id
        self._by_user_id[user_id] = updated
        return updated


class InMemoryVerificationSessionStore:
    def __init__(self) -> None:
        self._by_id: dict[str, VerificationSession] = {}
        self._by_state: dict[str, str] = {}

    def create(self, session: VerificationSession) -> VerificationSession:
        self._by_id[session.id] = session
        if session.status == "started":
            self._by_state[session.state] = session.id
        return session

    def get_by_state(self, state: str) -> VerificationSession | None:
        session_id = self._by_state.get(state)
        if session_id is None:
            return None
        return self._by_id.get(session_id)

    def get_by_id(self, session_id: str) -> VerificationSession | None:
        return self._by_id.get(session_id)

    def mark_consumed(self, session_id: str) -> None:
        session = self._by_id.get(session_id)
        if session is None:
            return
        if session.status == "consumed":
            return
        updated = dataclasses.replace(session, status="consumed")
        self._by_id[session_id] = updated
        self._by_state.pop(session.state, None)

    def mark_failed(self, session_id: str, reason: str) -> None:
        del reason
        session = self._by_id.get(session_id)
        if session is None:
            return
        updated = dataclasses.replace(session, status="failed")
        self._by_id[session_id] = updated
        self._by_state.pop(session.state, None)

    def expire_pending(self, now: datetime) -> int:
        expired_count = 0
        for session_id, session in list(self._by_id.items()):
            if session.status != "started":
                continue
            if session.expires_at >= now:
                continue
            updated = dataclasses.replace(session, status="expired")
            self._by_id[session_id] = updated
            self._by_state.pop(session.state, None)
            expired_count += 1
        return expired_count


class InMemoryPhoneVerificationSessionStore:
    def __init__(self) -> None:
        self._by_id: dict[str, PhoneVerificationSession] = {}

    def create(self, session: PhoneVerificationSession) -> PhoneVerificationSession:
        self._by_id[session.id] = session
        return session

    def get_by_id(self, session_id: str) -> PhoneVerificationSession | None:
        return self._by_id.get(session_id)

    def get_active_by_user(self, supabase_user_id: str, *, now: datetime) -> PhoneVerificationSession | None:
        active: PhoneVerificationSession | None = None
        for session in self._by_id.values():
            if session.supabase_user_id != supabase_user_id:
                continue
            if session.status != "started":
                continue
            if session.expires_at < now:
                continue
            if active is None or session.created_at > active.created_at:
                active = session
        return active

    def get_latest_for_confirm(self, supabase_user_id: str) -> PhoneVerificationSession | None:
        latest: PhoneVerificationSession | None = None
        for session in self._by_id.values():
            if session.supabase_user_id != supabase_user_id:
                continue
            if session.status not in {"started", "failed"}:
                continue
            if latest is None or session.created_at > latest.created_at:
                latest = session
        return latest

    def get_by_provider_message_id(self, provider_message_id: str) -> PhoneVerificationSession | None:
        for session in self._by_id.values():
            if session.provider_message_id == provider_message_id:
                return session
        return None

    def replace(self, session: PhoneVerificationSession) -> PhoneVerificationSession:
        self._by_id[session.id] = session
        return session

    def mark_consumed(self, session_id: str) -> None:
        session = self._by_id.get(session_id)
        if session is None:
            return
        if session.status == "consumed":
            return
        self._by_id[session_id] = dataclasses.replace(session, status="consumed")

    def mark_failed(self, session_id: str, reason: str) -> None:
        del reason
        session = self._by_id.get(session_id)
        if session is None:
            return
        self._by_id[session_id] = dataclasses.replace(session, status="failed")

    def mark_expired(self, session_id: str) -> None:
        session = self._by_id.get(session_id)
        if session is None:
            return
        self._by_id[session_id] = dataclasses.replace(session, status="expired")

    def expire_pending(self, now: datetime) -> int:
        expired_count = 0
        for session_id, session in list(self._by_id.items()):
            if session.status != "started":
                continue
            if session.expires_at >= now:
                continue
            self._by_id[session_id] = dataclasses.replace(session, status="expired")
            expired_count += 1
        return expired_count


class InMemoryPhoneAuditLogRepository:
    def __init__(self) -> None:
        self._events: list[PhoneAuditEvent] = []

    def log_event(self, event: PhoneAuditEvent) -> None:
        self._events.append(event)

    def list_events(
        self,
        *,
        supabase_user_id: str | None = None,
        event_type: str | None = None,
        limit: int = 100,
    ) -> list[PhoneAuditEvent]:
        results = self._events
        if supabase_user_id is not None:
            results = [event for event in results if event.supabase_user_id == supabase_user_id]
        if event_type is not None:
            results = [event for event in results if event.event_type == event_type]
        return results[-limit:]


class InMemoryEIDAuditLogRepository:
    def __init__(self) -> None:
        self._events: list[EIDAuditEvent] = []

    def log_event(self, event: EIDAuditEvent) -> None:
        self._events.append(event)

    def list_events(
        self,
        *,
        supabase_user_id: str | None = None,
        event_type: str | None = None,
        limit: int = 100,
    ) -> list[EIDAuditEvent]:
        results = self._events
        if supabase_user_id is not None:
            results = [event for event in results if event.supabase_user_id == supabase_user_id]
        if event_type is not None:
            results = [event for event in results if event.event_type == event_type]
        return results[-limit:]


class InMemoryOAuthClientStore:
    def __init__(self, clients: dict[str, OAuthClient]) -> None:
        self._clients = clients

    @classmethod
    def from_config(cls, config: AppConfig) -> InMemoryOAuthClientStore:
        """Build store with single GPT OAuth client from AppConfig."""
        client = OAuthClient(
            client_id=config.gpt_oauth_client_id or "test-gpt-client",
            client_secret_hash=hash_secret(
                config.gpt_oauth_client_secret or "demo",
                key=config.oauth_access_token_secret or "demo-key",
            ),
            redirect_uri=config.gpt_oauth_redirect_uri or "",
            scopes=["profile:read", "stories:draft", "stories:create"],
        )
        return cls(clients={client.client_id: client})

    def get_client(self, client_id: str) -> OAuthClient | None:
        return self._clients.get(client_id)

    def list_clients(self) -> list[OAuthClient]:
        return list(self._clients.values())


class InMemoryAuthorizationRequestStore:
    def __init__(self) -> None:
        self._requests: dict[str, AuthorizationRequest] = {}

    def save(self, request: AuthorizationRequest) -> None:
        self._requests[request.oauth_request_id] = request

    def get(self, oauth_request_id: str) -> AuthorizationRequest | None:
        return self._requests.get(oauth_request_id)

    def consume(self, oauth_request_id: str, *, now: datetime) -> AuthorizationRequest | None:
        request = self._requests.get(oauth_request_id)
        if request is None:
            return None
        if now >= request.expires_at:
            del self._requests[oauth_request_id]
            return None
        del self._requests[oauth_request_id]
        return request


class InMemoryOAuthTokenService:
    def __init__(
        self,
        *,
        config: AppConfig,
        client_store: InMemoryOAuthClientStore | None = None,
    ) -> None:
        self._config = config
        self._client_store = client_store
        self._codes: dict[str, _StoredAuthCode] = {}

    def issue_authorization_code(
        self,
        *,
        supabase_user_id: str,
        client_id: str,
        scopes: list[str],
        redirect_uri: str,
        code_challenge: str | None = None,
        code_challenge_method: str | None = None,
    ) -> str:
        code = secrets.token_urlsafe(32)
        self._codes[code] = _StoredAuthCode(
            supabase_user_id=supabase_user_id,
            client_id=client_id,
            scopes=list(scopes),
            redirect_uri=redirect_uri,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            expires_at=time.time() + self._config.oauth_authorization_code_ttl_s,
        )
        return code

    def issue_access_token(
        self,
        *,
        code: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        code_verifier: str | None = None,
    ) -> str:
        from core.oauth.errors import OAuthClientError, OAuthGrantError
        from core.oauth.client_secret import verify_client_secret

        if self._client_store is not None:
            client = self._client_store.get_client(client_id)
            if client is None:
                raise OAuthClientError("invalid_client", "Unknown OAuth client.")
            if not verify_client_secret(
                client_secret,
                expected_hash=client.client_secret_hash,
                key=self._config.oauth_access_token_secret or "demo-key",
            ):
                raise OAuthClientError("invalid_client", "Client authentication failed.")
        stored = self._codes.get(code)
        if stored is None or stored.consumed:
            raise OAuthGrantError("invalid_grant", "Authorization code expired or already used.")
        if stored.client_id != client_id or stored.redirect_uri != redirect_uri:
            raise OAuthGrantError("invalid_grant", "Authorization code mismatch.")
        if time.time() > stored.expires_at:
            raise OAuthGrantError("invalid_grant", "Authorization code expired or already used.")
        if stored.code_challenge is not None:
            if code_verifier is None:
                raise OAuthGrantError("invalid_grant", "PKCE code_verifier required.")
            digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
            challenge = _b64url_encode(digest)
            if challenge != stored.code_challenge:
                raise OAuthGrantError("invalid_grant", "PKCE verification failed.")
        stored.consumed = True
        now = int(time.time())
        payload = {
            "iss": self._config.api_base_url or "https://identity.dogestonia.ee",
            "sub": stored.supabase_user_id,
            "aud": "doge-identity-service",
            "exp": now + self._config.oauth_access_token_ttl_s,
            "iat": now,
            "jti": str(uuid.uuid4()),
            "scope": " ".join(stored.scopes),
            "token_type": "oauth_access",
            "client_id": client_id,
        }
        from core.oauth.access_token_jwt import encode_access_token_jwt

        return encode_access_token_jwt(self._config, payload)

    def validate_access_token(self, token: str) -> OAuthTokenClaims:
        from core.oauth.access_token_jwt import claims_from_access_token_jwt

        return claims_from_access_token_jwt(self._config, token)


