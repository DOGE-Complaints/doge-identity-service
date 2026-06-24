from __future__ import annotations

from datetime import datetime, timedelta, timezone

from core.domain.models import AuthorizationRequest
from core.infrastructure.repositories import InMemoryAuthorizationRequestStore


def test_authorization_request_store_save_get_consume() -> None:
    now = datetime.now(timezone.utc)
    store = InMemoryAuthorizationRequestStore()
    request = AuthorizationRequest(
        oauth_request_id="req-1",
        client_id="client",
        redirect_uri="https://example/cb",
        scopes=["profile:read"],
        state="state-1",
        code_challenge=None,
        code_challenge_method=None,
        created_at=now,
        expires_at=now + timedelta(minutes=5),
    )
    store.save(request)
    assert store.get("req-1") is request
    consumed = store.consume("req-1", now=now)
    assert consumed is request
    assert store.get("req-1") is None


def test_authorization_request_store_consume_expired_returns_none() -> None:
    now = datetime.now(timezone.utc)
    store = InMemoryAuthorizationRequestStore()
    request = AuthorizationRequest(
        oauth_request_id="req-expired",
        client_id="client",
        redirect_uri="https://example/cb",
        scopes=["profile:read"],
        state="state-1",
        code_challenge=None,
        code_challenge_method=None,
        created_at=now - timedelta(minutes=10),
        expires_at=now - timedelta(minutes=1),
    )
    store.save(request)
    assert store.consume("req-expired", now=now) is None
