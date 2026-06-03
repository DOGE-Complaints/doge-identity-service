"""EPIC-IDS-06 Story 2 — HTTP transport smoke via TestClient (in-process, no network)."""

from __future__ import annotations

import time

import pytest
from fastapi.testclient import TestClient
from joserfc import jwt
from joserfc.jwk import OctKey

from core.api.asgi_app import _clear_api_dependencies_cache, create_app
from core.config.providers import provide_app_config

_DEMO_JWT_SECRET = "test-secret-for-demo"
_DEMO_SUPABASE_URL = "https://demo.local"

_IDENTITY_ROUTE_PATHS = frozenset(
    {
        "/health",
        "/ready",
        "/me",
        "/auth/eid/start",
        "/auth/eideasy/callback",
        "/auth/authentigate/callback",
        "/auth/mock/callback",
        "/oauth/authorize",
        "/oauth/authorize/complete",
        "/oauth/token",
        "/story-drafts",
        "/story-drafts/{draft_id}/submit",
        "/stories",
        "/gpt/actions/submit-story",
    }
)


@pytest.fixture(autouse=True)
def _reset_deps() -> None:
    _clear_api_dependencies_cache()
    yield
    _clear_api_dependencies_cache()


def _demo_bearer_token() -> str:
    now = int(time.time())
    claims = {
        "sub": "11111111-1111-1111-1111-111111111111",
        "role": "authenticated",
        "aud": "authenticated",
        "iss": f"{_DEMO_SUPABASE_URL.rstrip('/')}/auth/v1",
        "exp": now + 3600,
        "iat": now,
    }
    key = OctKey.import_key(_DEMO_JWT_SECRET)
    return jwt.encode({"alg": "HS256"}, claims, key)


def test_health_returns_200(test_client: TestClient) -> None:
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ok"


def test_ready_returns_status(test_client: TestClient) -> None:
    response = test_client.get("/ready")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["db_backend"] == "in_memory"
    assert data["db_ready"] is True


def test_me_without_auth_returns_401(test_client: TestClient) -> None:
    response = test_client.get("/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_me_with_stub_bearer_returns_501(test_client: TestClient) -> None:
    token = _demo_bearer_token()
    response = test_client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 501
    assert response.json()["error"]["code"] == "NOT_IMPLEMENTED"


def test_options_me_cors_preflight(test_client: TestClient) -> None:
    response = test_client.options("/me")
    assert response.status_code == 200


def test_trace_id_propagation(test_client: TestClient) -> None:
    response = test_client.get("/health", headers={"x-trace-id": "custom"})
    assert response.status_code == 200
    assert response.json()["data"]["trace_id"] == "custom"


def test_all_identity_routes_registered(test_client: TestClient) -> None:
    paths = {getattr(route, "path", None) for route in test_client.app.routes}
    assert _IDENTITY_ROUTE_PATHS.issubset(paths)


def test_clear_cache_allows_new_app_instance(monkeypatch: pytest.MonkeyPatch) -> None:
    """DI cache reset between tests (autouse _reset_deps) enables fresh app wiring."""
    _clear_api_dependencies_cache()
    monkeypatch.setenv("API_BASE_URL", "http://localhost:8100")
    app = create_app(provide_app_config())
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
