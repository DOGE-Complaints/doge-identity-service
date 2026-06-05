from __future__ import annotations

import base64
import json
import time

import pytest
from fastapi.testclient import TestClient
from joserfc import jwt
from joserfc.jwk import OctKey

from core.api.security import (
    SupabaseJwtBearerTokenAuth,
    UnauthorizedError,
    UserClaims,
)
from core.auth.supabase_validator import JwtValidationError, SupabaseJwtValidatorImpl
from core.domain.contracts import SupabaseJwtValidator

JWT_SECRET = "test-jwt-secret-for-story-5"
SUPABASE_URL = "https://test-project.supabase.co"
USER_ID = "11111111-1111-1111-1111-111111111111"
_DEMO_JWT_SECRET = "test-secret-for-demo"
_DEMO_SUPABASE_URL = "https://demo.local"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _make_demo_jwt(*, secret: str = _DEMO_JWT_SECRET, supabase_url: str = _DEMO_SUPABASE_URL) -> str:
    now = int(time.time())
    claims = {
        "sub": USER_ID,
        "role": "authenticated",
        "aud": "authenticated",
        "iss": f"{supabase_url.rstrip('/')}/auth/v1",
        "exp": now + 3600,
        "iat": now,
    }
    key = OctKey.import_key(secret)
    return jwt.encode({"alg": "HS256"}, claims, key)


def _make_valid_token(
    *,
    jwt_secret: str = JWT_SECRET,
    supabase_url: str = SUPABASE_URL,
    user_id: str = USER_ID,
    email: str | None = "user@example.com",
    exp_offset: int = 3600,
    iss: str | None = None,
    role: str = "authenticated",
) -> str:
    now = int(time.time())
    claims = {
        "sub": user_id,
        "email": email,
        "role": role,
        "aud": "authenticated",
        "iss": iss if iss is not None else f"{supabase_url.rstrip('/')}/auth/v1",
        "exp": now + exp_offset,
        "iat": now,
    }
    key = OctKey.import_key(jwt_secret)
    return jwt.encode({"alg": "HS256"}, claims, key)


def _make_alg_none_token(*, supabase_url: str = SUPABASE_URL) -> str:
    now = int(time.time())
    claims = {
        "sub": USER_ID,
        "role": "authenticated",
        "aud": "authenticated",
        "iss": f"{supabase_url.rstrip('/')}/auth/v1",
        "exp": now + 3600,
    }
    header = _b64url(json.dumps({"alg": "none", "typ": "JWT"}).encode())
    payload = _b64url(json.dumps(claims).encode())
    return f"{header}.{payload}."


@pytest.fixture
def validator() -> SupabaseJwtValidatorImpl:
    return SupabaseJwtValidatorImpl(jwt_secret=JWT_SECRET, supabase_url=SUPABASE_URL)


def test_validator_accepts_valid_token(validator: SupabaseJwtValidatorImpl) -> None:
    token = _make_valid_token()
    claims = validator.validate(token)
    assert claims == UserClaims(
        supabase_user_id=USER_ID,
        email="user@example.com",
        role="authenticated",
    )


def test_validator_rejects_expired_token(validator: SupabaseJwtValidatorImpl) -> None:
    token = _make_valid_token(exp_offset=-60)
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_validator_rejects_alg_none_token(validator: SupabaseJwtValidatorImpl) -> None:
    token = _make_alg_none_token()
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_validator_rejects_iss_mismatch(validator: SupabaseJwtValidatorImpl) -> None:
    token = _make_valid_token(iss="https://wrong.supabase.co/auth/v1")
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_supabase_jwt_bearer_maps_validation_error_to_unauthorized(
    validator: SupabaseJwtValidatorImpl,
) -> None:
    auth = SupabaseJwtBearerTokenAuth(validator=validator)
    with pytest.raises(UnauthorizedError) as exc_info:
        auth.validate({"authorization": "Bearer not-a-jwt"})
    assert exc_info.value.code == "AUTHENTICATION_REQUIRED"


def test_supabase_jwt_bearer_validates_bearer_header(
    validator: SupabaseJwtValidatorImpl,
) -> None:
    auth = SupabaseJwtBearerTokenAuth(validator=validator)
    token = _make_valid_token()
    claims = auth.validate({"authorization": f"Bearer {token}"})
    assert claims.supabase_user_id == USER_ID


def test_supabase_jwt_validator_impl_satisfies_protocol(
    validator: SupabaseJwtValidatorImpl,
) -> None:
    assert isinstance(validator, SupabaseJwtValidator)


def test_get_me_with_valid_supabase_token_returns_200(test_client: TestClient) -> None:
    """Default DI uses demo JWT fallbacks; /me returns profile payload (not 401)."""
    token = _make_demo_jwt()
    response = test_client.get("/me", headers={"authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["data"]["eid_verified"] is False
