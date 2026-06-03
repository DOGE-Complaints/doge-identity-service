"""Story 5 contract: smoke directory excluded from default `pytest tests/` collection."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_default_collection_excludes_smoke_directory() -> None:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "--collect-only", "-q"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    combined = (proc.stdout + proc.stderr).lower()
    assert "tests/smoke" not in combined
    assert "test_local_server_smoke" not in combined
