"""SEC-04: prove SUPABASE_SERVICE_ROLE is never exposed in logs/responses/trace."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, create_app
from core.config import ConfigError
from core.config.providers import provide_app_config

_SENTINEL_SERVICE_ROLE = "eyJ-sentinel-service-role-secret-do-not-expose-SEC04"
_SRC_ROOT = Path(__file__).resolve().parents[1] / "src"
_LOG_PRINT_DEBUG = re.compile(r"\b(log\.|logger\.|print\(|debug\()", re.IGNORECASE)
_SERVICE_ROLE_REF = re.compile(r"service_role", re.IGNORECASE)


def _client_with_sentinel_env(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", _SENTINEL_SERVICE_ROLE)
    _clear_api_dependencies_cache()
    config = provide_app_config()
    app = create_app(config)
    return TestClient(app)


def _response_texts(client: TestClient, *paths: str) -> list[str]:
    texts: list[str] = []
    for path in paths:
        response = client.get(path)
        texts.append(response.text)
    return texts


def test_src_has_no_log_print_debug_of_service_role_value() -> None:
    offenders: list[str] = []
    for path in _SRC_ROOT.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if not _SERVICE_ROLE_REF.search(text):
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if _LOG_PRINT_DEBUG.search(line) and _SERVICE_ROLE_REF.search(line):
                if "service_role_key is required" in line:
                    continue
                offenders.append(f"{path.relative_to(_SRC_ROOT.parent)}:{line_no}:{line.strip()}")
    assert offenders == [], "service_role must not appear in log/print/debug lines:\n" + "\n".join(
        offenders
    )


def test_health_and_ready_never_echo_service_role(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with _client_with_sentinel_env(monkeypatch) as client:
        for body in _response_texts(client, "/health", "/ready"):
            assert _SENTINEL_SERVICE_ROLE not in body
            assert "SUPABASE_SERVICE_ROLE" not in body


def test_unauthorized_me_never_echoes_service_role(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with _client_with_sentinel_env(monkeypatch) as client:
        response = client.get("/me")
        assert response.status_code == 401
        assert _SENTINEL_SERVICE_ROLE not in response.text
        payload = response.json()
        assert json.dumps(payload).count(_SENTINEL_SERVICE_ROLE) == 0


def test_rate_limit_envelope_shape_never_includes_service_role_key_name() -> None:
    from core.api.envelope import build_error_envelope, build_rate_limit_envelope

    for builder in (
        build_error_envelope("TEST", "failure", trace_id="trace-1"),
        build_rate_limit_envelope(30, trace_id="trace-2"),
    ):
        serialized = json.dumps(builder)
        assert "SUPABASE_SERVICE_ROLE" not in serialized
        assert _SENTINEL_SERVICE_ROLE not in serialized


def test_internal_error_envelope_never_echoes_service_role(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import core.api.asgi_app as asgi_app_module

    def _boom(*_args: Any, **_kwargs: Any) -> tuple[dict, int]:
        raise RuntimeError(f"simulated failure with {_SENTINEL_SERVICE_ROLE}")

    monkeypatch.setattr(asgi_app_module, "handle_health", _boom)
    with _client_with_sentinel_env(monkeypatch) as client:
        response = client.get("/health")
        assert response.status_code == 500
        payload = response.json()
        assert payload["error"]["code"] == "INTERNAL_ERROR"
        assert _SENTINEL_SERVICE_ROLE not in response.text
        assert "SUPABASE_SERVICE_ROLE" not in response.text


def test_config_error_envelope_never_echoes_service_role_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import core.api.asgi_app as asgi_app_module

    def _config_fail(*_args: Any, **_kwargs: Any) -> tuple[dict, int]:
        raise ConfigError("SUPABASE_SERVICE_ROLE is required for APP_PROFILE=pilot")

    monkeypatch.setattr(asgi_app_module, "handle_health", _config_fail)
    with _client_with_sentinel_env(monkeypatch) as client:
        response = client.get("/health")
        assert response.status_code == 500
        payload = response.json()
        assert payload["error"]["code"] == "CONFIG_ERROR"
        assert _SENTINEL_SERVICE_ROLE not in response.text


def test_runtime_exception_logs_exclude_service_role_sentinel(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    import core.api.asgi_app as asgi_app_module

    def _boom(*_args: Any, **_kwargs: Any) -> tuple[dict, int]:
        raise RuntimeError("simulated internal failure without secret")

    monkeypatch.setattr(asgi_app_module, "handle_health", _boom)
    with caplog.at_level(logging.ERROR, logger="core.runtime"):
        with _client_with_sentinel_env(monkeypatch) as client:
            response = client.get("/health")
            assert response.status_code == 500
    assert _SENTINEL_SERVICE_ROLE not in caplog.text
    assert "SUPABASE_SERVICE_ROLE" not in caplog.text

