from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, create_app
from core.config.providers import provide_app_config

_TEST_ENV = {
    "APP_PROFILE": "demo",
    "API_BASE_URL": "http://localhost:8100",
    "DB_BACKEND": "in_memory",
    "EID_PROVIDER": "mock",
    "REQUEST_TIMEOUT_S": "15",
    "OIDC_REQUEST_TIMEOUT_S": "10",
    "CORS_ALLOWED_ORIGINS": "http://localhost:3000,http://127.0.0.1:3000",
}


@pytest.fixture
def test_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    _clear_api_dependencies_cache()
    for key, value in _TEST_ENV.items():
        monkeypatch.setenv(key, value)
    config = provide_app_config()
    app = create_app(config)
    with TestClient(app) as client:
        yield client
