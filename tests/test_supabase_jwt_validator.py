"""EPIC-IDS-06 Story 2 — SupabaseJwtValidator synthetic JWT tests (no network)."""

from __future__ import annotations

import base64
import json
import time

import pytest
from joserfc import jwt
from joserfc.jwk import OctKey

from core.auth.supabase_validator import JwtValidationError, SupabaseJwtValidatorImpl
from core.domain.models import UserClaims

JWT_SECRET = "story2-jwt-secret"
SUPABASE_URL = "https://test-project.supabase.co"
USER_ID = "22222222-2222-2222-2222-222222222222"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _make_valid_token(
    *,
    secret: str = JWT_SECRET,
    supabase_url: str = SUPABASE_URL,
    exp_offset: int = 3600,
    iss: str | None = None,
) -> str:
    now = int(time.time())
    claims = {
        "sub": USER_ID,
        "email": "user@example.com",
        "role": "authenticated",
        "aud": "authenticated",
        "iss": iss if iss is not None else f"{supabase_url.rstrip('/')}/auth/v1",
        "exp": now + exp_offset,
        "iat": now,
    }
    key = OctKey.import_key(secret)
    return jwt.encode({"alg": "HS256"}, claims, key)


def _make_alg_none_token() -> str:
    now = int(time.time())
    claims = {
        "sub": USER_ID,
        "role": "authenticated",
        "aud": "authenticated",
        "iss": f"{SUPABASE_URL.rstrip('/')}/auth/v1",
        "exp": now + 3600,
    }
    header = _b64url(json.dumps({"alg": "none", "typ": "JWT"}).encode())
    payload = _b64url(json.dumps(claims).encode())
    return f"{header}.{payload}."


@pytest.fixture
def validator() -> SupabaseJwtValidatorImpl:
    return SupabaseJwtValidatorImpl(jwt_secret=JWT_SECRET, supabase_url=SUPABASE_URL)


def test_valid_token_returns_user_claims(validator: SupabaseJwtValidatorImpl) -> None:
    token = _make_valid_token()
    claims = validator.validate(token)
    assert claims == UserClaims(
        supabase_user_id=USER_ID,
        email="user@example.com",
        role="authenticated",
    )


def test_expired_token_raises_jwt_validation_error(validator: SupabaseJwtValidatorImpl) -> None:
    token = _make_valid_token(exp_offset=-120)
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_wrong_signature_raises(validator: SupabaseJwtValidatorImpl) -> None:
    token = _make_valid_token(secret="other-secret")
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_alg_none_attack_rejected(validator: SupabaseJwtValidatorImpl) -> None:
    token = _make_alg_none_token()
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_iss_mismatch_raises(validator: SupabaseJwtValidatorImpl) -> None:
    token = _make_valid_token(iss="https://wrong.supabase.co/auth/v1")
    with pytest.raises(JwtValidationError):
        validator.validate(token)
