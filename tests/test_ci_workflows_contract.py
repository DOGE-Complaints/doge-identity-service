"""Story 4 contract: GitHub Actions workflow triggers and offline/live separation."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = REPO_ROOT / ".github" / "workflows"


def test_test_offline_workflow_exists_and_excludes_live_marker() -> None:
    path = WORKFLOWS / "test-offline.yml"
    text = path.read_text(encoding="utf-8")
    assert "pull_request" in text
    assert "push" in text
    assert 'not live_integration' in text
    assert "secrets.SUPABASE" not in text


def test_integration_live_workflow_main_and_dispatch_only() -> None:
    path = WORKFLOWS / "integration-live.yml"
    text = path.read_text(encoding="utf-8")
    assert "workflow_dispatch" in text
    assert "branches: [main]" in text
    assert "live_integration" in text
    assert "SUPABASE_TEST_URL" in text
    assert "SUPABASE_TEST_SERVICE_ROLE_KEY" in text
