from __future__ import annotations

import pytest
from starlette.requests import Request

from core.api.asgi_app import _clear_api_dependencies_cache, create_app, get_api_dependencies
from core.api.security import (
    SupabaseJwtBearerTokenAuth,
    UnauthorizedError,
    UserClaims,
    get_current_user,
)
from core.config.providers import provide_app_config
from core.domain.contracts import BearerTokenAuth
from core.domain.models import JwtValidationError
from tests.supabase_jwt_harness import DEFAULT_USER_ID, mint_supabase_access_token

_DEMO_USER_ID = DEFAULT_USER_ID


class _StubSupabaseJwtValidator:
    def validate(self, token: str) -> UserClaims:
        del token
        return UserClaims(supabase_user_id=_DEMO_USER_ID, email=None, role="authenticated")


def test_unauthorized_error_code() -> None:
    assert UnauthorizedError().code == "AUTHENTICATION_REQUIRED"


def test_bearer_token_auth_is_protocol() -> None:
    auth = SupabaseJwtBearerTokenAuth(validator=_StubSupabaseJwtValidator())
    assert isinstance(auth, BearerTokenAuth)


def test_supabase_jwt_validate_empty_headers_raises() -> None:
    auth = SupabaseJwtBearerTokenAuth(validator=_StubSupabaseJwtValidator())
    with pytest.raises(UnauthorizedError):
        auth.validate({})


def test_supabase_jwt_validate_bearer_returns_user_claims() -> None:
    auth = SupabaseJwtBearerTokenAuth(validator=_StubSupabaseJwtValidator())
    claims = auth.validate({"authorization": "Bearer xyz"})
    assert claims.supabase_user_id == _DEMO_USER_ID


def test_supabase_jwt_maps_jwt_validation_error() -> None:
    class _RejectingValidator:
        def validate(self, token: str) -> UserClaims:
            del token
            raise JwtValidationError("bad token")

    auth = SupabaseJwtBearerTokenAuth(validator=_RejectingValidator())
    with pytest.raises(UnauthorizedError):
        auth.validate({"authorization": "Bearer bad"})


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
    token = mint_supabase_access_token()
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
