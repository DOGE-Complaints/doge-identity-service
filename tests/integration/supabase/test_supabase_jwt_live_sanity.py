"""Live Supabase JWT sanity for SEC-03 (aud claim + raw OctKey import)."""

from __future__ import annotations

import base64
import json

import pytest

from core.auth.supabase_validator import SupabaseJwtValidatorImpl
from tests.integration.supabase.conftest import (
    _optional_live_access_token_from_dotenv,
    _require_supabase_jwt_validation_creds_from_dotenv,
)


def _decode_jwt_payload(token: str) -> dict[str, object]:
    segment = token.split(".")[1]
    segment += "=" * (-len(segment) % 4)
    return json.loads(base64.urlsafe_b64decode(segment))


@pytest.mark.live_integration
def test_live_supabase_access_token_aud_and_validator() -> None:
    """Operator-assisted live check when SUPABASE_*_ACCESS_TOKEN is set in .env."""
    token = _optional_live_access_token_from_dotenv()
    if token is None:
        pytest.skip(
            "Set SUPABASE_TEST_ACCESS_TOKEN or SUPABASE_LIVE_ACCESS_TOKEN in .env "
            "for live JWT aud/key sanity (operator-assisted)"
        )
    supabase_url, jwt_secret = _require_supabase_jwt_validation_creds_from_dotenv()
    payload = _decode_jwt_payload(token)
    assert payload.get("aud") == "authenticated"
    assert payload.get("role") == "authenticated"
    validator = SupabaseJwtValidatorImpl(jwt_secret=jwt_secret, supabase_url=supabase_url)
    claims = validator.validate(token)
    assert claims.role == "authenticated"
    assert claims.supabase_user_id
