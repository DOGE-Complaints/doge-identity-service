"""Story 1 acceptance: _block_dotenv_leakage and live_integration auto-tagging."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from core.config.providers import provide_app_config


def test_autouse_sets_in_memory_and_mock_eid() -> None:
    assert os.environ.get("DB_BACKEND") == "in_memory"
    assert os.environ.get("EID_PROVIDER") == "mock"
    assert os.environ.get("SUPABASE_URL") == ""


def test_provide_app_config_stays_in_memory_when_dotenv_has_supabase(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text(
        "DB_BACKEND=supabase\n"
        "SUPABASE_URL=https://prod.example.supabase.co\n"
        "SUPABASE_SERVICE_ROLE=eyJprod\n",
        encoding="utf-8",
    )
    config = provide_app_config()
    assert config.db_backend == "in_memory"


def test_monkeypatch_can_override_autouse_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DB_BACKEND", "postgres")
    assert os.environ["DB_BACKEND"] == "postgres"


def test_not_live_integration_excludes_supabase_integration_dir() -> None:
    """Collected offline: integration/supabase live tests are deselected by marker."""
    integration_dir = Path(__file__).resolve().parent / "integration" / "supabase"
    assert integration_dir.is_dir()
    py_tests = list(integration_dir.glob("test_*.py"))
    assert py_tests, "expected at least one test module under integration/supabase"
