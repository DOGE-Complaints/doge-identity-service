from __future__ import annotations

import logging
from unittest.mock import MagicMock, patch

import httpx
import pytest

from core.infrastructure.db_supabase import SupabaseDatabase

SUPABASE_URL = "https://test-project.supabase.co"
SERVICE_ROLE_KEY = "test-service-role-key"


def test_from_http_empty_url_raises_value_error() -> None:
    with pytest.raises(ValueError, match="supabase_url is required"):
        SupabaseDatabase.from_http("", SERVICE_ROLE_KEY)


def test_from_http_empty_service_role_key_raises_value_error() -> None:
    with pytest.raises(ValueError, match="service_role_key is required"):
        SupabaseDatabase.from_http(SUPABASE_URL, "")


def test_from_http_strips_trailing_slash_from_base_url() -> None:
    db = SupabaseDatabase.from_http(f"{SUPABASE_URL}/", SERVICE_ROLE_KEY)
    assert db.base_url == SUPABASE_URL


def test_headers_apikey_matches_bearer_token_value() -> None:
    db = SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)
    headers = db._headers()
    assert headers["apikey"] == headers["Authorization"].split()[-1]
    assert headers["apikey"] == SERVICE_ROLE_KEY
    assert headers["Content-Type"] == "application/json"


def test_headers_includes_prefer_when_set() -> None:
    db = SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)
    headers = db._headers(prefer="resolution=merge-duplicates")
    assert headers["Prefer"] == "resolution=merge-duplicates"


def test_request_on_http_5xx_logs_error_and_raises(
    caplog: pytest.LogCaptureFixture,
) -> None:
    db = SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)
    mock_response = MagicMock()
    mock_response.is_success = False
    mock_response.status_code = 503
    mock_response.text = "service unavailable"
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "503 Service Unavailable",
        request=httpx.Request("GET", f"{SUPABASE_URL}/rest/v1/profiles"),
        response=mock_response,
    )

    mock_client = MagicMock()
    mock_client.request.return_value = mock_response
    mock_client.__enter__.return_value = mock_client
    mock_client.__exit__.return_value = False

    with caplog.at_level(logging.ERROR, logger="core.infrastructure.db_supabase"):
        with patch("core.infrastructure.db_supabase.httpx.Client", return_value=mock_client):
            with pytest.raises(httpx.HTTPError):
                db._request(method="GET", path="/rest/v1/profiles")

    assert any(
        record.levelname == "ERROR" and "supabase_request_error" in record.message
        for record in caplog.records
    )
