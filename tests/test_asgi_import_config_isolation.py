"""EPIC-IDS-06 audit F1: asgi_app must not evaluate production config at import time."""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

from core.config import ConfigError


def test_import_asgi_app_module_without_config_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DB_BACKEND", "supabase")
    monkeypatch.setenv("SUPABASE_URL", "https://prod.local")
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE", raising=False)

    import core.api.asgi_app as asgi_mod

    importlib.reload(asgi_mod)
    assert hasattr(asgi_mod, "create_app")
    assert not hasattr(asgi_mod, "_config")


def test_access_app_with_incomplete_supabase_env_raises_config_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DB_BACKEND", "supabase")
    monkeypatch.setenv("SUPABASE_URL", "https://prod.local")
    monkeypatch.delenv("SUPABASE_SERVICE_ROLE", raising=False)

    import core.api.asgi_app as asgi_mod

    importlib.reload(asgi_mod)
    asgi_mod._default_production_app.cache_clear()

    with pytest.raises(ConfigError):
        _ = asgi_mod.app


def test_collect_bootstrap_smoke_with_dirty_process_env() -> None:
    root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["DB_BACKEND"] = "supabase"
    env["SUPABASE_URL"] = "https://prod.local"
    env.pop("SUPABASE_SERVICE_ROLE", None)

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_bootstrap_smoke.py",
            "--collect-only",
            "-q",
        ],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "ConfigError" not in result.stderr + result.stdout
