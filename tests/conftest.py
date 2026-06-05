from __future__ import annotations

import os

import pytest

# EPIC-IDS-06 Story 5: smoke runs only via `pytest tests/smoke/` (operator / deploy check).
collect_ignore = ["smoke"]
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, create_app
from core.config.providers import provide_app_config
from core.logging_setup import configure_logging

# Per-test env overrides for ASGI TestClient (applied after autouse _block_dotenv_leakage).
_TEST_CLIENT_ENV = {
    "CORS_ALLOWED_ORIGINS": "http://localhost:3000,http://127.0.0.1:3000",
    "REQUEST_TIMEOUT_S": "15",
    "OIDC_REQUEST_TIMEOUT_S": "10",
}


@pytest.fixture(autouse=True)
def _block_dotenv_leakage(monkeypatch: pytest.MonkeyPatch) -> None:
    # Deployment
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("PORT", "8100")
    monkeypatch.setenv("API_BASE_URL", "http://localhost:8100")
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    monkeypatch.setenv("LOG_FORMAT", "text")
    # DB — never real Supabase in unit tests
    monkeypatch.setenv("DB_BACKEND", "in_memory")
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    monkeypatch.setenv("SUPABASE_JWT_SECRET", "")
    monkeypatch.setenv("DATABASE_URL", "")
    # Authentigate OIDC — stub
    monkeypatch.setenv("AUTHENTIGATE_ISSUER", "https://stub.local")
    monkeypatch.setenv("AUTHENTIGATE_CLIENT_ID", "stub-client")
    monkeypatch.setenv("AUTHENTIGATE_CLIENT_SECRET", "stub-secret")
    monkeypatch.setenv(
        "AUTHENTIGATE_REDIRECT_URI",
        "http://localhost:8100/auth/authentigate/callback",
    )
    monkeypatch.setenv(
        "AUTHENTIGATE_SCOPES",
        "openid personal_code personal_code_country",
    )
    # eID provider — mock everywhere
    monkeypatch.setenv("EID_PROVIDER", "mock")
    monkeypatch.setenv("DOGESTONIA_EID_SECRET", "test-eid-hash-secret-not-real")
    monkeypatch.setenv("NODE_ID", "test-node")
    # OAuth server
    monkeypatch.setenv("OAUTH_ACCESS_TOKEN_SECRET", "test-oauth-secret-not-real")
    monkeypatch.setenv("OAUTH_ACCESS_TOKEN_TTL_S", "3600")
    monkeypatch.setenv("OAUTH_AUTHORIZATION_CODE_TTL_S", "300")
    monkeypatch.setenv("GPT_OAUTH_CLIENT_ID", "test-gpt-client")
    monkeypatch.setenv("GPT_OAUTH_CLIENT_SECRET", "test-gpt-client-secret")
    monkeypatch.setenv("GPT_OAUTH_REDIRECT_URI", "https://oauth.pstmn.io/v1/callback")
    # eID Easy — empty (provider=mock uses only base vars)
    monkeypatch.setenv("EIDEASY_ENV", "test")
    monkeypatch.setenv("EIDEASY_BASE_URL", "https://test.eideasy.com")
    monkeypatch.setenv("EIDEASY_CLIENT_ID", "")
    monkeypatch.setenv("EIDEASY_CLIENT_SECRET", "")
    monkeypatch.setenv(
        "EIDEASY_REDIRECT_URI",
        "http://localhost:8100/auth/eideasy/callback",
    )
    # CORS default for most tests (test_client may override)
    monkeypatch.setenv("CORS_ALLOWED_ORIGINS", "*")


@pytest.fixture(scope="session", autouse=True)
def _pytest_session_logging() -> None:
    configure_logging(
        os.environ.get("LOG_LEVEL", "INFO"),
        log_format="text",
        log_debug_dir=None,
    )


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    marker = pytest.mark.live_integration
    for item in items:
        path = str(item.path).replace("\\", "/")
        if "/tests/integration/supabase/" in path:
            item.add_marker(marker)


@pytest.fixture
def test_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    _clear_api_dependencies_cache()
    for key, value in _TEST_CLIENT_ENV.items():
        monkeypatch.setenv(key, value)
    config = provide_app_config()
    app = create_app(config)
    with TestClient(app) as client:
        yield client
