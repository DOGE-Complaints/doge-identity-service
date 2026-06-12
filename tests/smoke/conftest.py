"""Smoke tests against a live identity server (IDENTITY_URL, default port 8100)."""

from __future__ import annotations

import os

import httpx
import pytest


@pytest.fixture(scope="session")
def identity_url() -> str:
    base = os.environ.get("IDENTITY_URL", "http://localhost:8100").rstrip("/")
    try:
        response = httpx.get(f"{base}/health", timeout=5.0)
    except httpx.HTTPError as exc:
        pytest.skip(f"identity server not reachable at {base}: {exc}")
    else:
        if response.status_code != 200:
            pytest.skip(
                f"identity server not healthy at {base}: /health returned {response.status_code}"
            )
    return base
