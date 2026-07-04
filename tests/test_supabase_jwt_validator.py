"""EPIC-IDS-06 Story 2 / SEC-06 — SupabaseJwtValidator JWKS-only tests (no network)."""

from __future__ import annotations

import time

import httpx
import pytest
from joserfc import jwt
from joserfc.jwk import ECKey, RSAKey

from core.auth.supabase_validator import (
    JwtValidationError,
    SupabaseJwtValidatorImpl,
    _header_alg,
)
from core.domain.models import UserClaims
from core.security.oidc.jwks_cache import JwksCache
from tests.supabase_jwt_harness import (
    DEFAULT_USER_ID,
    TEST_SUPABASE_URL,
    build_test_jwks_cache,
    build_test_validator,
    jwks_http_handler,
    jwks_uri,
    mint_alg_none_token,
    mint_header_alg_token,
    mint_supabase_access_token,
    mint_with_foreign_key,
)

USER_ID = DEFAULT_USER_ID


@pytest.fixture
def validator() -> SupabaseJwtValidatorImpl:
    return build_test_validator()


def test_valid_es256_token_returns_user_claims(validator: SupabaseJwtValidatorImpl) -> None:
    token = mint_supabase_access_token(user_id=USER_ID)
    claims = validator.validate(token)
    assert claims == UserClaims(
        supabase_user_id=USER_ID,
        email="user@example.com",
        role="authenticated",
    )


def test_expired_token_raises_jwt_validation_error(validator: SupabaseJwtValidatorImpl) -> None:
    token = mint_supabase_access_token(user_id=USER_ID, exp_offset=-120)
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_wrong_signature_raises(validator: SupabaseJwtValidatorImpl) -> None:
    token = mint_with_foreign_key(user_id=USER_ID)
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_alg_none_attack_rejected(validator: SupabaseJwtValidatorImpl) -> None:
    token = mint_alg_none_token()
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_iss_mismatch_raises(validator: SupabaseJwtValidatorImpl) -> None:
    token = mint_supabase_access_token(
        user_id=USER_ID,
        iss="https://wrong.supabase.co/auth/v1",
    )
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_wrong_aud_raises(validator: SupabaseJwtValidatorImpl) -> None:
    token = mint_supabase_access_token(user_id=USER_ID, aud="service_role")
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_missing_aud_raises(validator: SupabaseJwtValidatorImpl) -> None:
    token = mint_supabase_access_token(user_id=USER_ID, aud=None)
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_header_alg_parses_es256() -> None:
    token = mint_supabase_access_token(user_id=USER_ID)
    assert _header_alg(token) == "ES256"


def test_hs256_algorithm_rejected(validator: SupabaseJwtValidatorImpl) -> None:
    token = mint_header_alg_token("HS256")
    with pytest.raises(JwtValidationError, match="Unsupported JWT algorithm"):
        validator.validate(token)


def test_empty_supabase_url_fails_closed_for_es256() -> None:
    validator = SupabaseJwtValidatorImpl(supabase_url="", jwks_cache=None)
    token = mint_supabase_access_token(user_id=USER_ID)
    with pytest.raises(JwtValidationError, match="JWKS validation unavailable"):
        validator.validate(token)


def test_unsupported_algorithm_rejected(validator: SupabaseJwtValidatorImpl) -> None:
    token = mint_header_alg_token("RS512")
    with pytest.raises(JwtValidationError, match="Unsupported JWT algorithm"):
        validator.validate(token)


def test_rs256_token_validated_via_mock_jwks() -> None:
    signing_key = RSAKey.generate_key(2048, parameters={"kid": "supabase-kid"})
    jwks_payload = {"keys": [signing_key.as_dict(private=False)]}

    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url).endswith("/.well-known/jwks.json"):
            return httpx.Response(200, json=jwks_payload)
        return httpx.Response(404, text="not found")

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    validator = SupabaseJwtValidatorImpl(
        supabase_url=TEST_SUPABASE_URL,
        jwks_cache=JwksCache(http_client, jwks_uri()),
    )
    now = int(time.time())
    token = jwt.encode(
        {"alg": "RS256", "kid": "supabase-kid"},
        {
            "sub": USER_ID,
            "email": "user@example.com",
            "role": "authenticated",
            "aud": "authenticated",
            "iss": f"{TEST_SUPABASE_URL.rstrip('/')}/auth/v1",
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


def test_kid_refresh_retries_jwks_fetch() -> None:
    signing_key = ECKey.generate_key("P-256", parameters={"kid": "rotated-kid"})
    call_count = 0

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal call_count
        if not str(request.url).endswith("/.well-known/jwks.json"):
            return httpx.Response(404, text="not found")
        call_count += 1
        if call_count == 1:
            return httpx.Response(200, json={"keys": []})
        return httpx.Response(200, json={"keys": [signing_key.as_dict(private=False)]})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    validator = SupabaseJwtValidatorImpl(
        supabase_url=TEST_SUPABASE_URL,
        jwks_cache=JwksCache(http_client, jwks_uri()),
    )
    token = jwt.encode(
        {"alg": "ES256", "kid": "rotated-kid"},
        {
            "sub": USER_ID,
            "role": "authenticated",
            "aud": "authenticated",
            "iss": f"{TEST_SUPABASE_URL.rstrip('/')}/auth/v1",
            "exp": int(time.time()) + 3600,
        },
        signing_key,
    )
    claims = validator.validate(token)
    assert claims.supabase_user_id == USER_ID
    assert call_count == 2
