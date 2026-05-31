from __future__ import annotations

import time

import pytest
from joserfc import jwt
from joserfc.jwk import OctKey
from starlette.requests import Request

from core.api.asgi_app import _clear_api_dependencies_cache, create_app, get_api_dependencies
from core.config.providers import provide_app_config
from core.api.security import (
    STUB_SUPABASE_USER_ID,
    BearerTokenAuth,
    StubBearerTokenAuth,
    UnauthorizedError,
    UserClaims,
    get_current_user,
)

_DEMO_USER_ID = "11111111-1111-1111-1111-111111111111"


def _make_demo_bearer_token() -> str:
    now = int(time.time())
    claims = {
        "sub": _DEMO_USER_ID,
        "role": "authenticated",
        "aud": "authenticated",
        "iss": "https://demo.local/auth/v1",
        "exp": now + 3600,
        "iat": now,
    }
    key = OctKey.import_key("test-secret-for-demo")
    return jwt.encode({"alg": "HS256"}, claims, key)


def test_unauthorized_error_code() -> None:
    assert UnauthorizedError().code == "AUTHENTICATION_REQUIRED"


def test_bearer_token_auth_is_protocol() -> None:
    assert isinstance(StubBearerTokenAuth(), BearerTokenAuth)


def test_stub_validate_empty_headers_raises() -> None:
    with pytest.raises(UnauthorizedError):
        StubBearerTokenAuth().validate({})


def test_stub_validate_bearer_returns_user_claims() -> None:
    claims = StubBearerTokenAuth().validate({"authorization": "Bearer xyz"})
    assert claims == UserClaims(
        supabase_user_id=STUB_SUPABASE_USER_ID,
        email=None,
        role="authenticated",
    )


def test_get_current_user_uses_deps_bearer_auth(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    for key, value in {
        "APP_PROFILE": "demo",
        "API_BASE_URL": "http://localhost:8100",
        "DB_BACKEND": "in_memory",
        "EID_PROVIDER": "mock",
    }.items():
        monkeypatch.setenv(key, value)
    create_app(provide_app_config())
    token = _make_demo_bearer_token()
    scope = {
        "type": "http",
        "headers": [(b"authorization", f"Bearer {token}".encode())],
        "method": "GET",
        "path": "/me",
    }
    request = Request(scope)
    user = get_current_user(request, get_api_dependencies())
    assert user.supabase_user_id == _DEMO_USER_ID


def test_get_current_user_without_auth_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    for key, value in {
        "APP_PROFILE": "demo",
        "API_BASE_URL": "http://localhost:8100",
        "DB_BACKEND": "in_memory",
        "EID_PROVIDER": "mock",
    }.items():
        monkeypatch.setenv(key, value)
    create_app(provide_app_config())
    scope = {"type": "http", "headers": [], "method": "GET", "path": "/me"}
    request = Request(scope)
    with pytest.raises(UnauthorizedError):
        get_current_user(request, get_api_dependencies())
