from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from core.api.security import (
    SupabaseJwtBearerTokenAuth,
    UnauthorizedError,
    UserClaims,
)
from core.auth.supabase_validator import JwtValidationError, SupabaseJwtValidatorImpl
from core.domain.contracts import SupabaseJwtValidator
from tests.supabase_jwt_harness import (
    DEFAULT_USER_ID,
    TEST_SUPABASE_URL,
    build_test_validator,
    mint_alg_none_token,
    mint_supabase_access_token,
)

USER_ID = DEFAULT_USER_ID


@pytest.fixture
def validator() -> SupabaseJwtValidatorImpl:
    return build_test_validator()


def test_validator_accepts_valid_token(validator: SupabaseJwtValidatorImpl) -> None:
    token = mint_supabase_access_token(user_id=USER_ID)
    claims = validator.validate(token)
    assert claims == UserClaims(
        supabase_user_id=USER_ID,
        email="user@example.com",
        role="authenticated",
    )


def test_validator_rejects_expired_token(validator: SupabaseJwtValidatorImpl) -> None:
    token = mint_supabase_access_token(user_id=USER_ID, exp_offset=-60)
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_validator_rejects_alg_none_token(validator: SupabaseJwtValidatorImpl) -> None:
    token = mint_alg_none_token()
    with pytest.raises(JwtValidationError):
        validator.validate(token)


def test_validator_rejects_iss_mismatch(validator: SupabaseJwtValidatorImpl) -> None:
    token = mint_supabase_access_token(
        user_id=USER_ID,
        iss="https://wrong.supabase.co/auth/v1",
    )
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
    token = mint_supabase_access_token(user_id=USER_ID)
    claims = auth.validate({"authorization": f"Bearer {token}"})
    assert claims.supabase_user_id == USER_ID


def test_supabase_jwt_validator_impl_satisfies_protocol(
    validator: SupabaseJwtValidatorImpl,
) -> None:
    assert isinstance(validator, SupabaseJwtValidator)


def test_get_me_with_valid_supabase_token_returns_200(test_client: TestClient) -> None:
    token = mint_supabase_access_token(user_id=USER_ID, supabase_url=TEST_SUPABASE_URL)
    response = test_client.get("/me", headers={"authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["data"]["eid_verified"] is False
