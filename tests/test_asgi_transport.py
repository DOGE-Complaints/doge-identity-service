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


def _make_demo_bearer_token() -> str:
    now = int(time.time())
    claims = {
        "sub": "11111111-1111-1111-1111-111111111111",
        "role": "authenticated",
        "aud": "authenticated",
        "iss": f"{_DEMO_SUPABASE_URL}/auth/v1",
        "exp": now + 3600,
        "iat": now,
    }
    key = OctKey.import_key(_DEMO_JWT_SECRET)
    return jwt.encode({"alg": "HS256"}, claims, key)


def test_app_title(test_client: TestClient) -> None:
    assert test_client.app.title == "doge-identity-service"


def test_health_returns_ok_envelope(test_client: TestClient) -> None:
    response = test_client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["data"]["status"] == "ok"
    assert "trace_id" in payload["data"]


def test_health_propagates_x_trace_id(test_client: TestClient) -> None:
    response = test_client.get("/health", headers={"x-trace-id": "my-trace"})
    assert response.status_code == 200
    assert response.json()["data"]["trace_id"] == "my-trace"


def test_ready_in_memory_backend(test_client: TestClient) -> None:
    response = test_client.get("/ready")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["db_backend"] == "in_memory"
    assert data["db_ready"] is True


def test_me_without_auth_returns_401(test_client: TestClient) -> None:
    response = test_client.get("/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_me_with_bearer_returns_501_stub(test_client: TestClient) -> None:
    token = _make_demo_bearer_token()
    response = test_client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 501
    error = response.json()["error"]
    assert error["code"] == "NOT_IMPLEMENTED"
    assert "next_epic" in error


def test_options_me_returns_200(test_client: TestClient) -> None:
    response = test_client.options("/me")
    assert response.status_code == 200


def test_options_oauth_authorize_returns_200(test_client: TestClient) -> None:
    response = test_client.options("/oauth/authorize")
    assert response.status_code == 200


def test_route_table_contains_identity_contract_paths(test_client: TestClient) -> None:
    paths = {getattr(route, "path", None) for route in test_client.app.routes}
    expected = {
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
    assert expected.issubset(paths)


def test_cors_allowed_origin_header_present(test_client: TestClient) -> None:
    response = test_client.get(
        "/health",
        headers={"Origin": "http://localhost:3000"},
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_cors_disallowed_origin_not_reflected(test_client: TestClient) -> None:
    response = test_client.get(
        "/health",
        headers={"Origin": "http://evil.com"},
    )
    assert response.headers.get("access-control-allow-origin") != "http://evil.com"


def test_ready_supabase_backend_reports_degraded(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    supabase_env = {
        "APP_PROFILE": "demo",
        "API_BASE_URL": "http://localhost:8100",
        "DB_BACKEND": "supabase",
        "EID_PROVIDER": "mock",
        "SUPABASE_URL": "https://example.supabase.co",
        "SUPABASE_SERVICE_ROLE": "service-role-key",
        "CORS_ALLOWED_ORIGINS": "http://localhost:3000",
    }
    for key, value in supabase_env.items():
        monkeypatch.setenv(key, value)
    config = provide_app_config()
    app = create_app(config)
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/ready")
    assert response.status_code == 503
    data = response.json()["data"]
    assert data["db_backend"] == "supabase"
    assert data["db_ready"] is False
