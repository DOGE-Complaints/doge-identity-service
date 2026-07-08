from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from typing import Any, Iterator
from unittest.mock import patch
from uuid import uuid4

from core.domain.models import PhoneAuditEvent, PhoneVerificationSession
from core.infrastructure.db_supabase import (
    SupabaseDatabase,
    SupabasePhoneAuditLogRepository,
    SupabasePhoneVerificationSessionStore,
    _parse_datetime,
)
from core.security.hashing import hash_secret

SUPABASE_URL = "https://test-project.supabase.co"
SERVICE_ROLE_KEY = "test-service-role-key"


def _eq_value(raw: str) -> str:
    return raw.removeprefix("eq.")


def _lt_value(raw: str) -> datetime:
    return _parse_datetime(raw.removeprefix("lt.")) or datetime.min.replace(tzinfo=timezone.utc)


def _phone_session(
    *,
    session_id: str | None = None,
    user_id: str = "11111111-1111-1111-1111-111111111111",
    status: str = "started",
    attempts: int = 0,
    created_at: datetime | None = None,
    expires_at: datetime | None = None,
    provider_message_id: str | None = None,
) -> PhoneVerificationSession:
    now = datetime(2026, 6, 26, 12, 0, 0, tzinfo=timezone.utc)
    created = created_at or now
    expires = expires_at or (created + timedelta(minutes=5))
    return PhoneVerificationSession(
        id=session_id or str(uuid4()),
        supabase_user_id=user_id,
        phone_hash=hash_secret("+37255555555", key="test-key"),
        dial_prefix="+372",
        code_hash="hash",
        status=status,
        attempts=attempts,
        created_at=created,
        expires_at=expires,
        provider="mock",
        provider_message_id=provider_message_id,
        delivery_status=None,
        delivery_updated_at=None,
    )


def _phone_audit_event(
    *,
    event_id: str | None = None,
    user_id: str = "11111111-1111-1111-1111-111111111111",
) -> PhoneAuditEvent:
    now = datetime(2026, 6, 26, 12, 0, 0, tzinfo=timezone.utc)
    return PhoneAuditEvent(
        id=event_id or str(uuid4()),
        supabase_user_id=user_id,
        event_type="phone.request",
        provider="mock",
        success=True,
        failure_reason=None,
        request_id="req-1",
        ip_hash=None,
        user_agent_hash=None,
        created_at=now,
    )


class PhonePostgrestMock:
    def __init__(self) -> None:
        self.sessions: list[dict[str, Any]] = []
        self.audit_events: list[dict[str, Any]] = []

    def __call__(
        self,
        *,
        method: str,
        path: str,
        params: dict[str, str] | None = None,
        json_body: dict[str, Any] | None = None,
        prefer: str | None = None,
    ) -> list[dict[str, Any]] | None:
        params = params or {}
        if path == "/rest/v1/phone_verification_sessions":
            return self._handle_sessions(method, params, json_body, prefer)
        if path == "/rest/v1/phone_audit_events":
            return self._handle_audit(method, params, json_body, prefer)
        raise AssertionError(f"unexpected PostgREST call: {method} {path}")

    def _find_session(self, session_id: str) -> dict[str, Any] | None:
        for row in self.sessions:
            if row["id"] == session_id:
                return row
        return None

    def _handle_sessions(
        self,
        method: str,
        params: dict[str, str],
        json_body: dict[str, Any] | None,
        prefer: str | None,
    ) -> list[dict[str, Any]] | None:
        if method == "POST":
            assert json_body is not None
            self.sessions.append(dict(json_body))
            if prefer == "return=representation":
                return [dict(json_body)]
            return None
        if method == "GET":
            if "id" in params:
                session_id = _eq_value(params["id"])
                row = self._find_session(session_id)
                return [dict(row)] if row else []
            if "provider_message_id" in params:
                message_id = _eq_value(params["provider_message_id"])
                matches = [
                    row
                    for row in self.sessions
                    if row.get("provider_message_id") == message_id
                ]
                return matches[:1]
            if "supabase_user_id" in params:
                user_id = _eq_value(params["supabase_user_id"])
                return [dict(row) for row in self.sessions if row["supabase_user_id"] == user_id]
            raise AssertionError(f"unexpected GET params: {params}")
        if method == "PATCH":
            assert json_body is not None
            if "id" in params:
                session_id = _eq_value(params["id"])
                row = self._find_session(session_id)
                if row is None:
                    return [] if prefer == "return=representation" else None
                row.update(json_body)
                if prefer == "return=representation":
                    return [dict(row)]
                return None
            if params.get("status") == "eq.started" and "expires_at" in params:
                cutoff = _lt_value(params["expires_at"])
                updated: list[dict[str, Any]] = []
                for row in self.sessions:
                    expires_at = _parse_datetime(row["expires_at"]) or datetime.max.replace(
                        tzinfo=timezone.utc
                    )
                    if row["status"] == "started" and expires_at < cutoff:
                        row["status"] = json_body.get("status", "expired")
                        updated.append(dict(row))
                return updated if prefer == "return=representation" else None
            raise AssertionError(f"unexpected PATCH params: {params}")
        raise AssertionError(f"unexpected sessions method: {method}")

    def _handle_audit(
        self,
        method: str,
        params: dict[str, str],
        json_body: dict[str, Any] | None,
        prefer: str | None,
    ) -> list[dict[str, Any]] | None:
        del prefer
        if method == "POST":
            assert json_body is not None
            self.audit_events.append(dict(json_body))
            return None
        if method == "GET":
            results = list(self.audit_events)
            if "supabase_user_id" in params:
                user_id = _eq_value(params["supabase_user_id"])
                results = [row for row in results if row.get("supabase_user_id") == user_id]
            if "event_type" in params:
                event_type = _eq_value(params["event_type"])
                results = [row for row in results if row.get("event_type") == event_type]
            limit = int(params.get("limit", "100"))
            return results[:limit]
        raise AssertionError(f"unexpected audit method: {method}")


@contextmanager
def mock_postgrest(mock: PhonePostgrestMock) -> Iterator[SupabaseDatabase]:
    with patch.object(SupabaseDatabase, "_request", mock):
        yield SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)


def test_supabase_phone_session_store_create_and_get_by_id() -> None:
    mock = PhonePostgrestMock()
    with mock_postgrest(mock) as db:
        store = SupabasePhoneVerificationSessionStore(db)
        session = _phone_session(session_id="sess-a")
        store.create(session)
        loaded = store.get_by_id("sess-a")
        assert loaded == session


def test_supabase_phone_session_store_get_active_by_user() -> None:
    mock = PhonePostgrestMock()
    with mock_postgrest(mock) as db:
        store = SupabasePhoneVerificationSessionStore(db)
        now = datetime(2026, 6, 26, 12, 0, 0, tzinfo=timezone.utc)
        older = _phone_session(session_id="old", created_at=now - timedelta(minutes=2))
        newer = _phone_session(session_id="new", created_at=now)
        store.create(older)
        store.create(newer)
        active = store.get_active_by_user(
            "11111111-1111-1111-1111-111111111111",
            now=now,
        )
        assert active is not None
        assert active.id == "new"


def test_supabase_phone_session_store_mark_consumed_and_expired() -> None:
    mock = PhonePostgrestMock()
    with mock_postgrest(mock) as db:
        store = SupabasePhoneVerificationSessionStore(db)
        session = _phone_session(session_id="sess-expire")
        store.create(session)
        store.mark_consumed("sess-expire")
        loaded = store.get_by_id("sess-expire")
        assert loaded is not None
        assert loaded.status == "consumed"

        expired = _phone_session(
            session_id="sess-pending",
            expires_at=datetime(2026, 6, 26, 11, 59, 0, tzinfo=timezone.utc),
        )
        store.create(expired)
        count = store.expire_pending(datetime(2026, 6, 26, 12, 0, 0, tzinfo=timezone.utc))
        assert count == 1
        pending = store.get_by_id("sess-pending")
        assert pending is not None
        assert pending.status == "expired"


def test_durability_phone_session_survives_store_recreate() -> None:
    mock = PhonePostgrestMock()
    with mock_postgrest(mock) as db:
        store_a = SupabasePhoneVerificationSessionStore(db)
        session = _phone_session(session_id="durability-sess")
        store_a.create(session)

        store_b = SupabasePhoneVerificationSessionStore(db)
        loaded = store_b.get_latest_for_confirm("11111111-1111-1111-1111-111111111111")
        assert loaded is not None
        assert loaded.id == "durability-sess"


def test_durability_phone_audit_survives_repo_recreate() -> None:
    mock = PhonePostgrestMock()
    with mock_postgrest(mock) as db:
        repo_a = SupabasePhoneAuditLogRepository(db)
        event = _phone_audit_event(event_id="audit-1")
        repo_a.log_event(event)

        repo_b = SupabasePhoneAuditLogRepository(db)
        events = repo_b.list_events(
            supabase_user_id="11111111-1111-1111-1111-111111111111",
        )
        assert len(events) == 1
        assert events[0].id == "audit-1"
        assert events[0].ip_hash is None
        assert events[0].user_agent_hash is None


def test_supabase_phone_audit_stores_ip_ua_hashes_when_present() -> None:
    mock = PhonePostgrestMock()
    with mock_postgrest(mock) as db:
        repo = SupabasePhoneAuditLogRepository(db)
        event = PhoneAuditEvent(
            id=str(uuid4()),
            supabase_user_id="11111111-1111-1111-1111-111111111111",
            event_type="phone.request",
            provider="mock",
            success=True,
            failure_reason=None,
            request_id="req-2",
            ip_hash="ip-h",
            user_agent_hash="ua-h",
            created_at=datetime(2026, 6, 26, 12, 0, 0, tzinfo=timezone.utc),
        )
        repo.log_event(event)
        stored = repo.list_events(
            supabase_user_id="11111111-1111-1111-1111-111111111111",
        )[0]
        assert stored.ip_hash == "ip-h"
        assert stored.user_agent_hash == "ua-h"
