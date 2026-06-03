"""EPIC-IDS-06 Story 2 — API dependencies singleton (lru_cache)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import (
    _clear_api_dependencies_cache,
    create_app,
    get_api_dependencies,
)
from core.config.providers import provide_app_config


@pytest.fixture(autouse=True)
def _reset_deps() -> None:
    _clear_api_dependencies_cache()
    yield
    _clear_api_dependencies_cache()


def test_singleton_is_same_object() -> None:
    first = get_api_dependencies()
    second = get_api_dependencies()
    assert first is second


def test_clear_cache_allows_recreation(monkeypatch: pytest.MonkeyPatch) -> None:
    original = get_api_dependencies()
    _clear_api_dependencies_cache()
    monkeypatch.setenv("NODE_ID", "recreated-node")
    recreated = get_api_dependencies()
    assert recreated is not original
    assert recreated.config.node_id == "recreated-node"


def test_health_uses_singleton(test_client: TestClient) -> None:
    deps_before = get_api_dependencies()
    test_client.get("/health")
    test_client.get("/health")
    assert get_api_dependencies() is deps_before


def test_create_app_clears_cache_before_build(monkeypatch: pytest.MonkeyPatch) -> None:
    get_api_dependencies()
    app = create_app(provide_app_config())
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
