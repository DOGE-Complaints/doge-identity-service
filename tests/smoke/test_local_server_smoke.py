"""EPIC-IDS-06 Story 5: real HTTP smoke against IDENTITY_URL (not default pytest collection)."""

from __future__ import annotations

import httpx
import pytest


pytestmark = pytest.mark.smoke


def test_health(identity_url: str) -> None:
    response = httpx.get(f"{identity_url}/health", timeout=5.0)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "ok"


def test_ready(identity_url: str) -> None:
    response = httpx.get(f"{identity_url}/ready", timeout=5.0)
    assert response.status_code in (200, 503)
    data = response.json()["data"]
    assert "db_backend" in data
    assert "db_ready" in data


def test_me_without_auth(identity_url: str) -> None:
    response = httpx.get(f"{identity_url}/me", timeout=5.0)
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_options_me(identity_url: str) -> None:
    response = httpx.options(f"{identity_url}/me", timeout=5.0)
    assert response.status_code == 200


def test_options_oauth_authorize(identity_url: str) -> None:
    response = httpx.options(f"{identity_url}/oauth/authorize", timeout=5.0)
    assert response.status_code == 200
