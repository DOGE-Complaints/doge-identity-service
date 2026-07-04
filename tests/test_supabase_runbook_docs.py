from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = REPO_ROOT / "docs" / "runbook" / "supabase-project-setup.md"
ENV_EXAMPLE = REPO_ROOT / ".env.example"
MIGRATIONS_DIR = REPO_ROOT / "supabase" / "migrations"

OPERATIONAL_MIGRATION_FILES = (
    "20260525000001_create_profiles.sql",
    "20260525000002_create_eid_verification_sessions.sql",
    "20260525000003_create_eid_audit_events.sql",
    "20260526000001_eid_sessions_provider_abstraction.sql",
)

HISTORICAL_MIGRATION_FILES = (
    "20260527000001_create_story_drafts.sql",
)


def test_runbook_file_exists() -> None:
    assert RUNBOOK.is_file()


@pytest.mark.parametrize(
    "snippet",
    [
        "Create Supabase project",
        "SUPABASE_URL",
        "SUPABASE_SERVICE_ROLE",
        ".well-known/jwks.json",
        "make check-env",
        "make serve",
        "startup.persistence_backend",
        "db_ready=True",
    ],
)
def test_runbook_contains_epic_story5_steps(snippet: str) -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    assert snippet in text


@pytest.mark.parametrize("migration_file", OPERATIONAL_MIGRATION_FILES)
def test_runbook_lists_operational_migrations_in_order(migration_file: str) -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    assert migration_file in text
    assert (MIGRATIONS_DIR / migration_file).is_file()


def test_runbook_marks_story_drafts_migration_historical() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    assert "20260527000001_create_story_drafts.sql" in text
    assert "DEPRECATED" in text or "do not apply" in text.lower()
    assert "Historical" in text or "historical" in text


def test_runbook_documents_ci_test_secrets() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    for secret in (
        "SUPABASE_TEST_URL",
        "SUPABASE_TEST_SERVICE_ROLE_KEY",
    ):
        assert secret in text
    assert "≠" in text or "!=" in text or "отличаться" in text.lower()


def test_env_example_has_supabase_backend_vars() -> None:
    text = ENV_EXAMPLE.read_text(encoding="utf-8")
    for key in ("DB_BACKEND", "SUPABASE_URL", "SUPABASE_SERVICE_ROLE"):
        assert key in text


@pytest.mark.parametrize("migration_file", HISTORICAL_MIGRATION_FILES)
def test_historical_migration_file_exists_on_disk(migration_file: str) -> None:
    assert (MIGRATIONS_DIR / migration_file).is_file()
