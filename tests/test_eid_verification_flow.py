"""EPIC-IDS-09 STORY-IDS-EID-01 — mock eID verification flow (offline e2e)."""

from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from joserfc import jwt
from joserfc.jwk import OctKey

from core.api.asgi_app import _clear_api_dependencies_cache, create_app, get_api_dependencies
from core.config.providers import provide_app_config
from core.domain.models import VerificationSession
from core.providers.base import EIDVerificationResult

_DEMO_JWT_SECRET = "test-secret-for-demo"
_DEMO_SUPABASE_URL = "https://demo.local"
_DEMO_USER_ID = "11111111-1111-1111-1111-111111111111"
_OTHER_USER_ID = "22222222-2222-2222-2222-222222222222"
_RETURN_URL = "https://dogestonia.ee/verify"


@pytest.fixture(autouse=True)
def _reset_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("ALLOWED_RETURN_URLS", _RETURN_URL)
    yield
    _clear_api_dependencies_cache()


def _demo_bearer_token(*, sub: str = _DEMO_USER_ID) -> str:
    now = int(time.time())
    claims = {
        "sub": sub,
        "role": "authenticated",
        "aud": "authenticated",
        "iss": f"{_DEMO_SUPABASE_URL.rstrip('/')}/auth/v1",
        "exp": now + 3600,
        "iat": now,
    }
    key = OctKey.import_key(_DEMO_JWT_SECRET)
    return jwt.encode({"alg": "HS256"}, claims, key)


def _start_payload(**overrides: object) -> dict[str, str]:
    payload = {
        "return_url": _RETURN_URL,
        "return_context": "dashboard_verification",
        "requested_action": "eid:verify",
    }
    payload.update(overrides)
    return payload


def test_eid_start_creates_session_and_returns_redirect(test_client: TestClient) -> None:
    token = _demo_bearer_token()
    response = test_client.post(
        "/auth/eid/start",
        headers={"Authorization": f"Bearer {token}"},
        json=_start_payload(),
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["redirect_url"].startswith("/auth/mock/callback?session_id=")
    assert data["session_id"]
    assert data["expires_at"].endswith("Z")

    deps = get_api_dependencies()
    assert deps.verification_session_store is not None
    session = deps.verification_session_store.get_by_id(data["session_id"])
    assert session is not None
    assert session.status == "started"
    assert session.supabase_user_id == _DEMO_USER_ID
    assert session.return_context == "dashboard_verification"
    assert session.requested_action == "eid:verify"

    assert deps.eid_audit_log_repository is not None
    events = deps.eid_audit_log_repository.list_events(
        supabase_user_id=_DEMO_USER_ID,
        event_type="eid_verification_started",
    )
    assert len(events) == 1
    assert events[0].success is True
    assert events[0].failure_reason is None


def test_mock_callback_verifies_profile_and_me_reflects_status(
    test_client: TestClient,
) -> None:
    token = _demo_bearer_token()
    start = test_client.post(
        "/auth/eid/start",
        headers={"Authorization": f"Bearer {token}"},
        json=_start_payload(),
    )
    redirect_url = start.json()["data"]["redirect_url"]

    callback = test_client.get(redirect_url, headers={"Accept": "application/json"})
    assert callback.status_code == 200
    assert callback.json()["data"]["status"] == "verified"

    me = test_client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    data = me.json()["data"]
    assert data["eid_verified"] is True
    assert data["eid_verified_at"]
    assert data["eid_provider"] == "mock"


def test_mock_callback_replay_is_idempotent(test_client: TestClient) -> None:
    token = _demo_bearer_token()
    start = test_client.post(
        "/auth/eid/start",
        headers={"Authorization": f"Bearer {token}"},
        json=_start_payload(),
    )
    redirect_url = start.json()["data"]["redirect_url"]

    first = test_client.get(redirect_url, headers={"Accept": "application/json"})
    assert first.status_code == 200
    hash_after_first = test_client.get(
        "/me", headers={"Authorization": f"Bearer {token}"}
    ).json()["data"]["eid_verified_at"]

    replay = test_client.get(redirect_url, headers={"Accept": "application/json"})
    assert replay.status_code == 200
    assert replay.json()["data"]["status"] == "already_consumed"

    hash_after_replay = test_client.get(
        "/me", headers={"Authorization": f"Bearer {token}"}
    ).json()["data"]["eid_verified_at"]
    assert hash_after_replay == hash_after_first


def test_mock_callback_expired_session_does_not_verify_profile(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("ALLOWED_RETURN_URLS", _RETURN_URL)
    app = create_app(provide_app_config())
    token = _demo_bearer_token()

    with TestClient(app) as client:
        start = client.post(
            "/auth/eid/start",
            headers={"Authorization": f"Bearer {token}"},
            json=_start_payload(),
        )
        session_id = start.json()["data"]["session_id"]
        deps = get_api_dependencies()
        store = deps.verification_session_store
        assert store is not None
        session = store.get_by_id(session_id)
        assert session is not None
        expired = VerificationSession(
            id=session.id,
            supabase_user_id=session.supabase_user_id,
            state=session.state,
            nonce=session.nonce,
            code_verifier_encrypted=session.code_verifier_encrypted,
            code_verifier_hash=session.code_verifier_hash,
            return_context=session.return_context,
            return_url=session.return_url,
            requested_action=session.requested_action,
            status=session.status,
            created_at=session.created_at,
            expires_at=datetime.now(timezone.utc) - timedelta(minutes=1),
            provider=session.provider,
            provider_session_data=session.provider_session_data,
        )
        store._by_id[session_id] = expired  # noqa: SLF001 — test fixture mutation

        callback = client.get(
            f"/auth/mock/callback?session_id={session_id}",
            headers={"Accept": "application/json"},
        )
        assert callback.status_code == 400
        assert callback.json()["error"]["code"] == "eid_session_expired"

        me = client.get("/me", headers={"Authorization": f"Bearer {token}"})
        assert me.json()["data"]["eid_verified"] is False


def test_mock_callback_profile_hash_conflict_returns_409(
    test_client: TestClient,
) -> None:
    fixed_verification = EIDVerificationResult(
        provider="mock",
        country="EE",
        login_method="mock",
        subject_hash="fixed-subject",
        verified_at=datetime.now(timezone.utc),
    )

    with patch(
        "core.providers.mock.mock_provider.MockEIDProvider.handle_callback",
        return_value=fixed_verification,
    ):
        first_token = _demo_bearer_token(sub=_DEMO_USER_ID)
        first_start = test_client.post(
            "/auth/eid/start",
            headers={"Authorization": f"Bearer {first_token}"},
            json=_start_payload(),
        )
        first_callback = test_client.get(
            first_start.json()["data"]["redirect_url"],
            headers={"Accept": "application/json"},
        )
        assert first_callback.status_code == 200

        second_token = _demo_bearer_token(sub=_OTHER_USER_ID)
        second_start = test_client.post(
            "/auth/eid/start",
            headers={"Authorization": f"Bearer {second_token}"},
            json=_start_payload(),
        )
        conflict = test_client.get(
            second_start.json()["data"]["redirect_url"],
            headers={"Accept": "application/json"},
        )

    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "profile_conflict"

    me = test_client.get("/me", headers={"Authorization": f"Bearer {second_token}"})
    assert me.json()["data"]["eid_verified"] is False

    deps = get_api_dependencies()
    assert deps.eid_audit_log_repository is not None
    failed = deps.eid_audit_log_repository.list_events(
        supabase_user_id=_OTHER_USER_ID,
        event_type="eid_verification_failed",
    )
    assert failed
    assert failed[-1].failure_reason == "profile_conflict"
