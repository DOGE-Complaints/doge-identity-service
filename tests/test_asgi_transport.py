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
_TEST_CLIENT_ENV = {
    "CORS_ALLOWED_ORIGINS": "http://localhost:3000,http://127.0.0.1:3000",
    "REQUEST_TIMEOUT_S": "15",
    "OIDC_REQUEST_TIMEOUT_S": "10",
}


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


def test_me_with_bearer_returns_200_not_verified(test_client: TestClient) -> None:
    token = _make_demo_bearer_token()
    response = test_client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["supabase_user_id"] == "11111111-1111-1111-1111-111111111111"
    assert data["eid_verified"] is False


def test_auth_eid_start_rejects_foreign_return_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_api_dependencies_cache()
    for key, value in _TEST_CLIENT_ENV.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setenv("ALLOWED_RETURN_URLS", "https://dogestonia.ee/verify")
    app = create_app(provide_app_config())
    token = _make_demo_bearer_token()
    with TestClient(app) as client:
        response = client.post(
            "/auth/eid/start",
            headers={"Authorization": f"Bearer {token}"},
            json={"return_url": "https://evil.com/phish"},
        )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_return_url"


def test_auth_eid_start_allows_listed_return_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_api_dependencies_cache()
    for key, value in _TEST_CLIENT_ENV.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setenv("ALLOWED_RETURN_URLS", "https://dogestonia.ee/verify")
    app = create_app(provide_app_config())
    token = _make_demo_bearer_token()
    with TestClient(app) as client:
        response = client.post(
            "/auth/eid/start",
            headers={"Authorization": f"Bearer {token}"},
            json={"return_url": "https://dogestonia.ee/verify"},
        )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["redirect_url"].startswith("/auth/mock/callback?session_id=")
    assert data["expires_at"]


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
        "/auth/phone/request",
        "/auth/phone/confirm",
        "/auth/{provider}/callback",
        "/oauth/authorize",
        "/oauth/authorize/complete",
        "/oauth/token",
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
    assert data["status"] == "degraded"
    assert data["db_backend"] == "supabase"
    assert data["db_ready"] is False
    assert set(data["db_checks"]) == {
        "connectivity",
        "schema",
        "columns",
        "provider_state",
        "policy_probe",
    }
    assert all(value is False for value in data["db_checks"].values())


def test_startup_log_emits_db_checks(monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    _clear_api_dependencies_cache()
    supabase_env = {
        "APP_PROFILE": "demo",
        "API_BASE_URL": "http://localhost:8100",
        "DB_BACKEND": "supabase",
        "EID_PROVIDER": "mock",
        "SUPABASE_URL": "https://example.supabase.co",
        "SUPABASE_SERVICE_ROLE": "service-role-key",
        "CORS_ALLOWED_ORIGINS": "http://localhost:3000",
        "LOG_LEVEL": "INFO",
    }
    for key, value in supabase_env.items():
        monkeypatch.setenv(key, value)
    monkeypatch.setattr("core.api.asgi_app.configure_logging", lambda *args, **kwargs: None)
    app = create_app(provide_app_config())
    with caplog.at_level("INFO", logger="core.api.asgi_app"):
        with TestClient(app) as client:
            client.get("/health")
    assert any(
        "startup.persistence_backend" in record.message and "db_checks=" in record.message
        for record in caplog.records
    )
