"""EPIC-IDS-06 Story 2 — SupabaseJwtValidator synthetic JWT tests (no network)."""

from __future__ import annotations

import base64
import json
import time

import httpx
import pytest
from joserfc import jwt
from joserfc.jwk import OctKey, RSAKey

from core.auth.supabase_validator import (
    JwtValidationError,
    SupabaseJwtValidatorImpl,
    _header_alg,
)
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
    aud: str | None = "authenticated",
) -> str:
    now = int(time.time())
    claims = {
        "sub": USER_ID,
        "email": "user@example.com",
        "role": "authenticated",
        "iss": iss if iss is not None else f"{supabase_url.rstrip('/')}/auth/v1",
        "exp": now + exp_offset,
        "iat": now,
    }
    if aud is not None:
        claims["aud"] = aud
    key = OctKey.import_key(secret)
    return jwt.encode({"alg": "HS256"}, claims, key)


def _b64url_oct_jwk(secret: str) -> dict[str, str]:
    return {"kty": "oct", "k": _b64url(secret.encode())}


def _make_header_alg_token(alg: str) -> str:
    now = int(time.time())
    claims = {
        "sub": USER_ID,
        "role": "authenticated",
        "aud": "authenticated",
        "iss": f"{SUPABASE_URL.rstrip('/')}/auth/v1",
        "exp": now + 3600,
    }
    header = _b64url(json.dumps({"alg": alg, "typ": "JWT"}).encode())
    payload = _b64url(json.dumps(claims).encode())
    return f"{header}.{payload}.invalid-signature"


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


def test_wrong_aud_raises(validator: SupabaseJwtValidatorImpl) -> None:
    token = _make_valid_token(aud="service_role")
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_missing_aud_raises(validator: SupabaseJwtValidatorImpl) -> None:
    token = _make_valid_token(aud=None)
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_raw_secret_import_validates_hs256_token(validator: SupabaseJwtValidatorImpl) -> None:
    token = _make_valid_token()
    assert validator.validate(token).supabase_user_id == USER_ID


def test_raw_octkey_import_is_canonical_for_supabase_hs256(
    validator: SupabaseJwtValidatorImpl,
) -> None:
    """Supabase signs with dashboard JWT secret string; raw OctKey.import_key matches HS256."""
    token = _make_valid_token()
    validator.validate(token)
    wrapped_key = OctKey.import_key(_b64url_oct_jwk(JWT_SECRET))
    wrapped_token = jwt.encode(
        {"alg": "HS256"},
        {
            "sub": USER_ID,
            "role": "authenticated",
            "aud": "authenticated",
            "iss": f"{SUPABASE_URL.rstrip('/')}/auth/v1",
            "exp": int(time.time()) + 3600,
        },
        wrapped_key,
    )
    # joserfc: JWK k=b64url(secret bytes) may coincide with raw import for short secrets;
    # validator canonical path remains raw string per spec 09 / Supabase dashboard secret.
    validator.validate(wrapped_token)


def test_header_alg_parses_hs256() -> None:
    token = _make_valid_token()
    assert _header_alg(token) == "HS256"


def test_jwks_cache_disabled_for_demo_local() -> None:
    validator = SupabaseJwtValidatorImpl(
        jwt_secret=JWT_SECRET,
        supabase_url="https://demo.local",
    )
    assert validator._jwks_cache is None


def test_jwks_unavailable_raises_for_asymmetric_alg_on_demo_local() -> None:
    validator = SupabaseJwtValidatorImpl(
        jwt_secret=JWT_SECRET,
        supabase_url="https://demo.local",
    )
    token = _make_header_alg_token("ES256")
    with pytest.raises(JwtValidationError, match="JWKS validation unavailable"):
        validator.validate(token)


def test_unsupported_algorithm_rejected(validator: SupabaseJwtValidatorImpl) -> None:
    token = _make_header_alg_token("RS512")
    with pytest.raises(JwtValidationError, match="Unsupported JWT algorithm"):
        validator.validate(token)


def test_rs256_token_validated_via_mock_jwks() -> None:
    jwks_uri = f"{SUPABASE_URL.rstrip('/')}/auth/v1/.well-known/jwks.json"
    signing_key = RSAKey.generate_key(2048, parameters={"kid": "supabase-kid"})
    jwks_payload = {"keys": [signing_key.as_dict(private=False)]}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url == httpx.URL(jwks_uri):
            return httpx.Response(200, json=jwks_payload)
        return httpx.Response(404, text="not found")

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    validator = SupabaseJwtValidatorImpl(
        jwt_secret=JWT_SECRET,
        supabase_url=SUPABASE_URL,
        http_client=http_client,
    )
    now = int(time.time())
    token = jwt.encode(
        {"alg": "RS256", "kid": "supabase-kid"},
        {
            "sub": USER_ID,
            "email": "user@example.com",
            "role": "authenticated",
            "aud": "authenticated",
            "iss": f"{SUPABASE_URL.rstrip('/')}/auth/v1",
            "exp": now + 3600,
            "iat": now,
        },
        signing_key,
    )
    claims = validator.validate(token)
    assert claims == UserClaims(
        supabase_user_id=USER_ID,
        email="user@example.com",
        role="authenticated",
    )
