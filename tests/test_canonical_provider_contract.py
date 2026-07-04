"""EPIC-IDS-09 STORY-IDS-EID-05 — canonical provider contract (offline)."""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, get_api_dependencies
from core.providers.base import EIDProviderError, EIDVerificationResult, EidErrorCode
from core.security.hashing import hash_secret
from tests.supabase_jwt_harness import DEFAULT_USER_ID, mint_supabase_access_token

_DEMO_USER_ID = DEFAULT_USER_ID
_RETURN_URL = "https://dogestonia.ee/verify"


@pytest.fixture(autouse=True)
def _reset_deps(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    monkeypatch.setenv("ALLOWED_RETURN_URLS", _RETURN_URL)
    yield
    _clear_api_dependencies_cache()


def _start_and_get_redirect(test_client: TestClient) -> str:
    token = mint_supabase_access_token(user_id=_DEMO_USER_ID)

    start = test_client.post(
        "/auth/eid/start",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "return_url": _RETURN_URL,
            "return_context": "dashboard_verification",
            "requested_action": "eid:verify",
        },
    )
    assert start.status_code == 200
    return start.json()["data"]["redirect_url"]


def test_callback_eid_provider_error_records_canonical_code_in_audit(
    test_client: TestClient,
) -> None:
    redirect_url = _start_and_get_redirect(test_client)

    with patch(
        "core.providers.mock.mock_provider.MockEIDProvider.handle_callback",
        side_effect=EIDProviderError(
            "User cancelled",
            code=EidErrorCode.USER_CANCELLED,
        ),
    ):
        response = test_client.get(
            redirect_url,
            headers={"Accept": "application/json"},
        )

    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "eid_verification_failed"
    assert body["error"]["eid_error_code"] == "USER_CANCELLED"

    deps = get_api_dependencies()
    assert deps.eid_audit_log_repository is not None
    failed = deps.eid_audit_log_repository.list_events(
        supabase_user_id=_DEMO_USER_ID,
        event_type="eid_verification_failed",
    )
    assert failed
    assert failed[-1].failure_reason == "USER_CANCELLED"


def test_callback_unexpected_exception_records_unknown(
    test_client: TestClient,
) -> None:
    redirect_url = _start_and_get_redirect(test_client)

    with patch(
        "core.providers.mock.mock_provider.MockEIDProvider.handle_callback",
        side_effect=RuntimeError("unexpected"),
    ):
        response = test_client.get(
            redirect_url,
            headers={"Accept": "application/json"},
        )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "eid_verification_failed"
    assert response.json()["error"]["eid_error_code"] == "UNKNOWN"

    deps = get_api_dependencies()
    assert deps.eid_audit_log_repository is not None
    failed = deps.eid_audit_log_repository.list_events(
        supabase_user_id=_DEMO_USER_ID,
        event_type="eid_verification_failed",
    )
    assert failed
    assert failed[-1].failure_reason == "UNKNOWN"


def test_same_subject_hash_different_providers_same_verified_person_hash() -> None:
    country = "EE"
    subject_hash = "stable-national-id-digest"
    secret = "test-eid-secret"

    mock_result = EIDVerificationResult(
        provider="mock",
        country=country,
        subject_hash=subject_hash,
        login_method="mock",
        verified_at=datetime.now(timezone.utc),
    )
    authentigate_result = EIDVerificationResult(
        provider="authentigate",
        country=country,
        subject_hash=subject_hash,
        login_method="smart_id",
        verified_at=datetime.now(timezone.utc),
    )

    mock_hash = hash_secret(f"{mock_result.country}:{mock_result.subject_hash}", key=secret)
    other_hash = hash_secret(
        f"{authentigate_result.country}:{authentigate_result.subject_hash}",
        key=secret,
    )

    assert mock_hash == other_hash
    assert mock_result.provider != authentigate_result.provider
