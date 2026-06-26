"""Live Supabase integration helpers (parse `.env` directly — bypasses autouse env block)."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.config.env_file import _parse_dotenv_file

_SERVICE_ROOT = Path(__file__).resolve().parents[3]
_DOTENV_PATH = _SERVICE_ROOT / ".env"


def _require_supabase_creds_from_dotenv() -> tuple[str, str]:
    """Return test-project PostgREST URL and service role key from `.env` only."""
    dotenv = _parse_dotenv_file(_DOTENV_PATH)
    url = (dotenv.get("SUPABASE_TEST_URL") or "").strip()
    key = (
        dotenv.get("SUPABASE_TEST_SERVICE_ROLE")
        or dotenv.get("SUPABASE_TEST_SERVICE_ROLE_KEY")
        or ""
    ).strip()
    if not url or not key:
        pytest.skip(
            "No SUPABASE_TEST_URL / SUPABASE_TEST_SERVICE_ROLE(_KEY) in .env "
            "— skipping live integration test"
        )
    prod_url = (dotenv.get("SUPABASE_URL") or "").strip()
    if prod_url and url.rstrip("/") == prod_url.rstrip("/"):
        pytest.fail(
            "SUPABASE_TEST_URL must not equal production SUPABASE_URL in .env"
        )
    return url, key


def _require_supabase_jwt_validation_creds_from_dotenv() -> tuple[str, str]:
    """Return Supabase auth URL and JWT secret for HS256 validator live sanity."""
    dotenv = _parse_dotenv_file(_DOTENV_PATH)
    url = (
        dotenv.get("SUPABASE_TEST_URL")
        or dotenv.get("SUPABASE_URL")
        or ""
    ).strip().rstrip("/")
    secret = (
        dotenv.get("SUPABASE_TEST_JWT_SECRET")
        or dotenv.get("SUPABASE_JWT_SECRET")
        or ""
    ).strip()
    if not url or not secret:
        pytest.skip(
            "No SUPABASE_TEST_URL/SUPABASE_URL + SUPABASE_TEST_JWT_SECRET/"
            "SUPABASE_JWT_SECRET in .env — skipping JWT live sanity"
        )
    return url, secret


def _optional_live_access_token_from_dotenv() -> str | None:
    dotenv = _parse_dotenv_file(_DOTENV_PATH)
    token = (
        dotenv.get("SUPABASE_TEST_ACCESS_TOKEN")
        or dotenv.get("SUPABASE_LIVE_ACCESS_TOKEN")
        or ""
    ).strip()
    return token or None


@pytest.fixture
def live_supabase_db():
    from core.infrastructure.db_supabase import SupabaseDatabase

    url, key = _require_supabase_creds_from_dotenv()
    return SupabaseDatabase.from_http(url, key)
