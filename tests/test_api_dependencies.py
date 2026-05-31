from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, create_app, get_api_dependencies
from core.api.dependencies import (
    EPIC_IDS_04_OPTIONAL_FIELDS,
    ApiDependencies,
    HandlerDependencies,
    build_api_dependencies,
)
from core.api.security import StubBearerTokenAuth
from core.config.providers import provide_app_config


IDENTITY_OPTIONAL_FIELDS = EPIC_IDS_04_OPTIONAL_FIELDS

_BASE_ENV = {
    "APP_PROFILE": "demo",
    "API_BASE_URL": "http://localhost:8100",
    "DB_BACKEND": "in_memory",
    "EID_PROVIDER": "mock",
    "REQUEST_TIMEOUT_S": "15",
    "OIDC_REQUEST_TIMEOUT_S": "10",
    "CORS_ALLOWED_ORIGINS": "http://localhost:3000",
}


def _apply_env(monkeypatch: pytest.MonkeyPatch, env: dict[str, str]) -> None:
    for key, value in env.items():
        monkeypatch.setenv(key, value)


def test_handler_dependencies_is_alias() -> None:
    assert HandlerDependencies is ApiDependencies


def test_api_dependencies_imports_from_package() -> None:
    from core.api.dependencies import ApiDependencies as AD, HandlerDependencies as HD

    assert HD is AD


def test_api_dependencies_identity_slots_default_none() -> None:
    config = provide_app_config(_BASE_ENV)
    deps = ApiDependencies(
        config=config,
        bearer_token_auth=StubBearerTokenAuth(),
        db_backend="in_memory",
        db_ready=True,
    )
    for field_name in IDENTITY_OPTIONAL_FIELDS:
        assert getattr(deps, field_name) is None


def test_api_dependencies_is_frozen() -> None:
    config = provide_app_config(_BASE_ENV)
    deps = ApiDependencies(
        config=config,
        bearer_token_auth=StubBearerTokenAuth(),
        db_backend="in_memory",
        db_ready=True,
    )
    with pytest.raises(FrozenInstanceError):
        deps.config = config  # type: ignore[misc]


def test_get_api_dependencies_singleton_is_frozen(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    _apply_env(monkeypatch, _BASE_ENV)
    create_app(provide_app_config())
    deps = get_api_dependencies()
    with pytest.raises(FrozenInstanceError):
        deps.db_backend = "x"  # type: ignore[misc]


def test_build_api_dependencies_zero_arg(monkeypatch: pytest.MonkeyPatch) -> None:
    _apply_env(monkeypatch, _BASE_ENV)
    deps = build_api_dependencies()
    assert deps.db_backend == "in_memory"
    assert deps.db_ready is True
    assert deps.profile_repository is not None
    assert type(deps.bearer_token_auth).__name__ == "SupabaseJwtBearerTokenAuth"


def test_get_api_dependencies_is_singleton(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    _apply_env(monkeypatch, _BASE_ENV)
    create_app(provide_app_config())
    assert get_api_dependencies() is get_api_dependencies()


def test_clear_cache_creates_new_singleton(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    _apply_env(monkeypatch, _BASE_ENV)
    create_app(provide_app_config())
    first = get_api_dependencies()
    _clear_api_dependencies_cache()
    second = get_api_dependencies()
    assert first is not second


def test_monkeypatch_log_level_reloads_config(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    _apply_env(monkeypatch, {**_BASE_ENV, "LOG_LEVEL": "INFO"})
    create_app(provide_app_config())
    assert get_api_dependencies().config.log_level == "INFO"
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    _clear_api_dependencies_cache()
    create_app(provide_app_config())
    assert get_api_dependencies().config.log_level == "DEBUG"


def test_lifespan_configures_logging(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    _apply_env(monkeypatch, {**_BASE_ENV, "LOG_LEVEL": "WARNING"})
    app = create_app(provide_app_config())
    with TestClient(app) as client:
        client.get("/health")
    assert logging.getLogger().level == logging.WARNING


def test_parallel_requests_share_same_dependencies(monkeypatch: pytest.MonkeyPatch) -> None:
    _clear_api_dependencies_cache()
    _apply_env(monkeypatch, _BASE_ENV)
    app = create_app(provide_app_config())
    deps_id = id(get_api_dependencies())

    def fetch_health() -> int:
        with TestClient(app) as client:
            response = client.get("/health")
            return id(get_api_dependencies()) if response.status_code == 200 else -1

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: fetch_health(), range(2)))

    assert all(result == deps_id for result in results)


def test_epic_ids_04_optional_fields_match_factory_getters() -> None:
    """Story 3 t02: dataclass slots align with epic §3 and commented provide_service_factory block."""
    assert len(EPIC_IDS_04_OPTIONAL_FIELDS) == 8
    for field_name in EPIC_IDS_04_OPTIONAL_FIELDS:
        assert field_name in ApiDependencies.__dataclass_fields__


def test_build_api_dependencies_uses_provide_service_factory() -> None:
    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "src" / "core" / "api" / "dependencies.py"
    text = source.read_text(encoding="utf-8")
    assert "from core.infrastructure.providers import provide_service_factory" in text
    assert "service_factory = provide_service_factory(config)" in text
    assert "# TODO EPIC-IDS-05: run 5-level Supabase healthchecks" in text
    assert "get_story_draft_repository" in text
