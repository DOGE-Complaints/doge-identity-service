"""Supabase PostgREST client (httpx, no Supabase SDK).

PostgREST filter cheat sheet (use in query ``params``):

- ``eq.`` — equality, e.g. ``{"supabase_user_id": "eq.abc"}``
- ``in.()`` — membership, e.g. ``{"status": "in.(a,b,c)"}``
- ``is.null`` — IS NULL, e.g. ``{"field": "is.null"}``
- ``gt.``, ``lt.`` — comparisons, e.g. ``{"score": "gt.50"}``
"""

from __future__ import annotations

import dataclasses
import json
import logging
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import httpx

from core.config.schema import AppConfig
from core.domain.models import (
    EIDAuditEvent,
    OAuthClient,
    ProfileConflictError,
    ProfileRecord,
    VerificationSession,
)
from core.security.hashing import hash_secret

logger = logging.getLogger(__name__)

__all__ = [
    "SupabaseDatabase",
    "SupabaseProfileRepository",
    "SupabaseVerificationSessionStore",
    "SupabaseEIDAuditLogRepository",
    "SupabaseOAuthClientStore",
    "SupabaseHealthRepository",
]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _parse_datetime(value: object | None) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        normalized = value.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized)
    raise TypeError(f"unsupported datetime value: {value!r}")


def _format_datetime(value: datetime | None) -> str | None:
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.isoformat()


def _jsonb_normalize(row: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    normalized = dict(row)
    for field in fields:
        if field not in normalized:
            continue
        raw = normalized[field]
        if isinstance(raw, str):
            normalized[field] = json.loads(raw)
    return normalized


def _first_row(rows: Any) -> dict[str, Any] | None:
    if not rows:
        return None
    if isinstance(rows, list):
        return rows[0] if rows else None
    if isinstance(rows, dict):
        return rows
    return None


def _profile_to_row(profile: ProfileRecord) -> dict[str, Any]:
    return {
        "id": profile.id,
        "supabase_user_id": profile.supabase_user_id,
        "display_name": profile.display_name,
        "avatar_url": profile.avatar_url,
        "eid_verified": profile.eid_verified,
        "verified_person_hash": profile.verified_person_hash,
        "eid_provider": profile.eid_provider,
        "eid_method": profile.eid_method,
        "eid_country": profile.eid_country,
        "eid_verified_at": _format_datetime(profile.eid_verified_at),
        "wallet_address": profile.wallet_address,
        "wallet_linked_at": _format_datetime(profile.wallet_linked_at),
        "wallet_signature_verified_at": _format_datetime(profile.wallet_signature_verified_at),
        "wallet_signature_scheme": profile.wallet_signature_scheme,
        "wallet_chain_id": profile.wallet_chain_id,
        "created_at": _format_datetime(profile.created_at),
        "updated_at": _format_datetime(profile.updated_at),
    }


def _profile_from_row(row: dict[str, Any]) -> ProfileRecord:
    return ProfileRecord(
        id=str(row["id"]),
        supabase_user_id=str(row["supabase_user_id"]),
        display_name=row.get("display_name"),
        avatar_url=row.get("avatar_url"),
        eid_verified=bool(row.get("eid_verified", False)),
        verified_person_hash=row.get("verified_person_hash"),
        eid_provider=row.get("eid_provider"),
        eid_method=row.get("eid_method"),
        eid_country=row.get("eid_country"),
        eid_verified_at=_parse_datetime(row.get("eid_verified_at")),
        wallet_address=row.get("wallet_address"),
        wallet_linked_at=_parse_datetime(row.get("wallet_linked_at")),
        wallet_signature_verified_at=_parse_datetime(
            row.get("wallet_signature_verified_at")
        ),
        wallet_signature_scheme=row.get("wallet_signature_scheme"),
        wallet_chain_id=row.get("wallet_chain_id"),
        created_at=_parse_datetime(row["created_at"]) or _utcnow(),
        updated_at=_parse_datetime(row["updated_at"]) or _utcnow(),
    )


def _verification_session_to_row(session: VerificationSession) -> dict[str, Any]:
    return {
        "id": session.id,
        "supabase_user_id": session.supabase_user_id,
        "state": session.state,
        "nonce": session.nonce,
        "code_verifier_encrypted": session.code_verifier_encrypted,
        "code_verifier_hash": session.code_verifier_hash,
        "return_context": session.return_context,
        "return_url": session.return_url,
        "requested_action": session.requested_action,
        "status": session.status,
        "created_at": _format_datetime(session.created_at),
        "expires_at": _format_datetime(session.expires_at),
        "provider": session.provider,
        "provider_session_data": session.provider_session_data,
    }


def _verification_session_from_row(row: dict[str, Any]) -> VerificationSession:
    normalized = _jsonb_normalize(row, ("provider_session_data",))
    provider_session_data = normalized.get("provider_session_data") or {}
    if not isinstance(provider_session_data, dict):
        provider_session_data = {}
    return VerificationSession(
        id=str(normalized["id"]),
        supabase_user_id=str(normalized["supabase_user_id"]),
        state=str(normalized["state"]),
        nonce=normalized.get("nonce"),
        code_verifier_encrypted=normalized.get("code_verifier_encrypted"),
        code_verifier_hash=normalized.get("code_verifier_hash"),
        return_context=normalized.get("return_context"),
        return_url=normalized.get("return_url"),
        requested_action=normalized.get("requested_action"),
        status=str(normalized["status"]),
        created_at=_parse_datetime(normalized["created_at"]) or _utcnow(),
        expires_at=_parse_datetime(normalized["expires_at"]) or _utcnow(),
        provider=str(normalized.get("provider", "eideasy")),
        provider_session_data=provider_session_data,
    )


def _audit_event_to_row(event: EIDAuditEvent) -> dict[str, Any]:
    return {
        "id": event.id,
        "supabase_user_id": event.supabase_user_id,
        "event_type": event.event_type,
        "provider": event.provider,
        "method": event.method,
        "success": event.success,
        "failure_reason": event.failure_reason,
        "request_id": event.request_id,
        "ip_hash": event.ip_hash,
        "user_agent_hash": event.user_agent_hash,
        "created_at": _format_datetime(event.created_at),
    }


def _audit_event_from_row(row: dict[str, Any]) -> EIDAuditEvent:
    return EIDAuditEvent(
        id=str(row["id"]),
        supabase_user_id=row.get("supabase_user_id"),
        event_type=str(row["event_type"]),
        provider=row.get("provider"),
        method=row.get("method"),
        success=bool(row["success"]),
        failure_reason=row.get("failure_reason"),
        request_id=row.get("request_id"),
        ip_hash=row.get("ip_hash"),
        user_agent_hash=row.get("user_agent_hash"),
        created_at=_parse_datetime(row["created_at"]) or _utcnow(),
    )


@dataclass(frozen=True)
class SupabaseDatabase:
    base_url: str
    service_role_key: str
    timeout_s: float = 15.0

    @classmethod
    def from_http(
        cls,
        supabase_url: str,
        service_role_key: str,
        timeout_s: float = 15.0,
    ) -> SupabaseDatabase:
        if not supabase_url:
            raise ValueError("supabase_url is required")
        if not service_role_key:
            raise ValueError("service_role_key is required")
        return cls(
            base_url=supabase_url.rstrip("/"),
            service_role_key=service_role_key,
            timeout_s=timeout_s,
        )

    def _headers(self, *, prefer: str | None = None) -> dict[str, str]:
        headers = {
            "apikey": self.service_role_key,
            "Authorization": f"Bearer {self.service_role_key}",
            "Content-Type": "application/json",
        }
        if prefer:
            headers["Prefer"] = prefer
        return headers

    def _request(
        self,
        *,
        method: str,
        path: str,
        params: dict[str, str] | None = None,
        json_body: dict[str, Any] | list[Any] | None = None,
        prefer: str | None = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        try:
            with httpx.Client(timeout=self.timeout_s) as client:
                response = client.request(
                    method=method,
                    url=url,
                    headers=self._headers(prefer=prefer),
                    params=params,
                    json=json_body,
                )
            if not response.is_success:
                logger.error(
                    "supabase_request_error method=%s path=%s status=%d body=%.300s",
                    method,
                    path,
                    response.status_code,
                    response.text,
                )
            response.raise_for_status()
            return response.json() if response.text.strip() else None
        except httpx.HTTPError as exc:
            logger.error(
                "supabase_http_error method=%s path=%s exc=%r",
                method,
                path,
                exc,
            )
            raise

    def healthcheck(self) -> bool:
        try:
            self._request(method="GET", path="/rest/v1/", params={"limit": "1"})
            return True
        except Exception:
            return False

    _REQUIRED_TABLES: tuple[str, ...] = (
        "profiles",
        "eid_verification_sessions",
        "eid_audit_events",
    )

    def required_tables_ready(self) -> bool:
        try:
            for table in self._REQUIRED_TABLES:
                self._request(
                    method="GET",
                    path=f"/rest/v1/{table}",
                    params={"limit": "1"},
                )
            return True
        except Exception:
            return False

    def required_columns_ready(self) -> bool:
        try:
            self._request(
                method="GET",
                path="/rest/v1/profiles",
                params={
                    "select": "supabase_user_id,eid_verified,verified_person_hash,eid_verified_at",
                    "limit": "1",
                },
            )
            return True
        except Exception:
            return False

    def provider_state_ready(self) -> bool:
        try:
            self._request(
                method="GET",
                path="/rest/v1/eid_verification_sessions",
                params={"select": "provider,provider_session_data", "limit": "1"},
            )
            return True
        except Exception:
            return False

    def service_role_policy_probe(self) -> bool:
        try:
            self._request(
                method="POST",
                path="/rest/v1/eid_audit_events",
                json_body={
                    "id": str(uuid.uuid4()),
                    "event_type": "health_probe",
                    "success": True,
                    "supabase_user_id": None,
                    "created_at": _format_datetime(_utcnow()),
                },
            )
            self._request(
                method="DELETE",
                path="/rest/v1/eid_audit_events",
                params={"event_type": "eq.health_probe"},
            )
            return True
        except Exception:
            return False


class SupabaseProfileRepository:
    def __init__(self, db: SupabaseDatabase) -> None:
        self._db = db

    def get_by_supabase_user_id(self, user_id: str) -> ProfileRecord | None:
        rows = self._db._request(
            method="GET",
            path="/rest/v1/profiles",
            params={"supabase_user_id": f"eq.{user_id}", "limit": "1"},
        )
        row = _first_row(rows)
        return _profile_from_row(row) if row else None

    def get_by_verified_person_hash(self, hash_: str) -> ProfileRecord | None:
        rows = self._db._request(
            method="GET",
            path="/rest/v1/profiles",
            params={"verified_person_hash": f"eq.{hash_}", "limit": "1"},
        )
        row = _first_row(rows)
        return _profile_from_row(row) if row else None

    def upsert(self, profile: ProfileRecord) -> ProfileRecord:
        rows = self._db._request(
            method="POST",
            path="/rest/v1/profiles",
            json_body=_profile_to_row(profile),
            prefer="resolution=merge-duplicates",
        )
        row = _first_row(rows)
        if row:
            return _profile_from_row(row)
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
        body = {
            "eid_verified": True,
            "verified_person_hash": verified_person_hash,
            "eid_provider": provider,
            "eid_method": method,
            "eid_country": country,
            "eid_verified_at": _format_datetime(verified_at),
            "updated_at": _format_datetime(_utcnow()),
        }
        try:
            rows = self._db._request(
                method="PATCH",
                path="/rest/v1/profiles",
                params={"supabase_user_id": f"eq.{user_id}"},
                json_body=body,
                prefer="return=representation",
            )
        except httpx.HTTPStatusError as exc:
            if exc.response is not None and exc.response.status_code == 409:
                raise ProfileConflictError(
                    f"verified_person_hash already bound: {verified_person_hash}"
                ) from exc
            raise

        row = _first_row(rows)
        if row:
            return _profile_from_row(row)

        existing = self.get_by_supabase_user_id(user_id)
        if existing is None:
            now = _utcnow()
            created = ProfileRecord(
                id=str(uuid.uuid4()),
                supabase_user_id=user_id,
                display_name=None,
                avatar_url=None,
                eid_verified=True,
                verified_person_hash=verified_person_hash,
                eid_provider=provider,
                eid_method=method,
                eid_country=country,
                eid_verified_at=verified_at,
                wallet_address=None,
                wallet_linked_at=None,
                wallet_signature_verified_at=None,
                wallet_signature_scheme=None,
                wallet_chain_id=None,
                created_at=now,
                updated_at=now,
            )
            return self.upsert(created)

        updated = dataclasses.replace(
            existing,
            eid_verified=True,
            verified_person_hash=verified_person_hash,
            eid_provider=provider,
            eid_method=method,
            eid_country=country,
            eid_verified_at=verified_at,
            updated_at=_utcnow(),
        )
        return self.upsert(updated)


class SupabaseVerificationSessionStore:
    def __init__(self, db: SupabaseDatabase) -> None:
        self._db = db

    def create(self, session: VerificationSession) -> VerificationSession:
        rows = self._db._request(
            method="POST",
            path="/rest/v1/eid_verification_sessions",
            json_body=_verification_session_to_row(session),
            prefer="return=representation",
        )
        row = _first_row(rows)
        return _verification_session_from_row(row) if row else session

    def get_by_state(self, state: str) -> VerificationSession | None:
        rows = self._db._request(
            method="GET",
            path="/rest/v1/eid_verification_sessions",
            params={
                "state": f"eq.{state}",
                "status": "eq.started",
                "limit": "1",
            },
        )
        row = _first_row(rows)
        return _verification_session_from_row(row) if row else None

    def get_by_id(self, session_id: str) -> VerificationSession | None:
        rows = self._db._request(
            method="GET",
            path="/rest/v1/eid_verification_sessions",
            params={"id": f"eq.{session_id}", "limit": "1"},
        )
        row = _first_row(rows)
        return _verification_session_from_row(row) if row else None

    def mark_consumed(self, session_id: str) -> None:
        self._db._request(
            method="PATCH",
            path="/rest/v1/eid_verification_sessions",
            params={"id": f"eq.{session_id}", "status": "eq.started"},
            json_body={"status": "consumed"},
        )

    def mark_failed(self, session_id: str, reason: str) -> None:
        self._db._request(
            method="PATCH",
            path="/rest/v1/eid_verification_sessions",
            params={"id": f"eq.{session_id}"},
            json_body={"status": "failed", "failure_reason": reason},
        )

    def expire_pending(self, now: datetime) -> int:
        rows = self._db._request(
            method="PATCH",
            path="/rest/v1/eid_verification_sessions",
            params={
                "status": "eq.started",
                "expires_at": f"lt.{_format_datetime(now)}",
            },
            json_body={"status": "expired"},
            prefer="return=representation",
        )
        if isinstance(rows, list):
            return len(rows)
        return 0


class SupabaseEIDAuditLogRepository:
    def __init__(self, db: SupabaseDatabase) -> None:
        self._db = db

    def log_event(self, event: EIDAuditEvent) -> None:
        self._db._request(
            method="POST",
            path="/rest/v1/eid_audit_events",
            json_body=_audit_event_to_row(event),
        )

    def list_events(
        self,
        *,
        supabase_user_id: str | None = None,
        event_type: str | None = None,
        limit: int = 100,
    ) -> list[EIDAuditEvent]:
        params: dict[str, str] = {
            "order": "created_at.desc",
            "limit": str(limit),
        }
        if supabase_user_id is not None:
            params["supabase_user_id"] = f"eq.{supabase_user_id}"
        if event_type is not None:
            params["event_type"] = f"eq.{event_type}"
        rows = self._db._request(
            method="GET",
            path="/rest/v1/eid_audit_events",
            params=params,
        ) or []
        return [_audit_event_from_row(row) for row in rows]


class SupabaseOAuthClientStore:
    """OAuth client registry backed by env/fallback config, not PostgREST.

    Accepts ``db`` for the same constructor shape as other Supabase repositories,
    but does not read OAuth clients from a database table (EPIC-IDS-05 §9).
    """

    def __init__(
        self,
        db: SupabaseDatabase,
        *,
        fallback_config: AppConfig | None = None,
        clients: dict[str, OAuthClient] | None = None,
    ) -> None:
        del db  # unused: clients come from fallback_config or explicit ``clients``
        if clients is not None:
            self._clients = clients
        elif fallback_config is not None:
            client = OAuthClient(
                client_id=fallback_config.gpt_oauth_client_id or "test-gpt-client",
                client_secret_hash=hash_secret(
                    fallback_config.gpt_oauth_client_secret or "demo",
                    key=fallback_config.oauth_access_token_secret or "demo-key",
                ),
                redirect_uri=fallback_config.gpt_oauth_redirect_uri or "",
                scopes=["profile:read", "stories:draft", "stories:create"],
            )
            self._clients = {client.client_id: client}
        else:
            self._clients = {}

    def get_client(self, client_id: str) -> OAuthClient | None:
        return self._clients.get(client_id)

    def list_clients(self) -> list[OAuthClient]:
        return list(self._clients.values())


class SupabaseHealthRepository:
    """Backend-specific HealthRepository for /ready endpoint."""

    def __init__(self, db: SupabaseDatabase) -> None:
        self._db = db

    def ping(self) -> bool:
        return self._db.healthcheck()
