from __future__ import annotations

import re
from pathlib import Path

import pytest

MIGRATIONS_DIR = (
    Path(__file__).resolve().parents[1] / "supabase" / "migrations"
)

OPERATIONAL_MIGRATIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "20260525000001_create_profiles.sql",
        ("profiles", "ENABLE ROW LEVEL SECURITY", "profiles_service_role_all", "IF NOT EXISTS"),
    ),
    (
        "20260525000002_create_eid_verification_sessions.sql",
        (
            "eid_verification_sessions",
            "ENABLE ROW LEVEL SECURITY",
            "eid_verification_sessions_service_role_all",
            "IF NOT EXISTS",
        ),
    ),
    (
        "20260525000003_create_eid_audit_events.sql",
        (
            "eid_audit_events",
            "ENABLE ROW LEVEL SECURITY",
            "eid_audit_events_service_role_all",
            "IF NOT EXISTS",
        ),
    ),
    (
        "20260526000001_eid_sessions_provider_abstraction.sql",
        (
            "provider_session_data",
            "ADD COLUMN IF NOT EXISTS",
            "idx_eid_sessions_provider",
            "ALTER COLUMN nonce DROP NOT NULL",
        ),
    ),
)

POST_HISTORICAL_MIGRATIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "20260611000001_profiles_phone_verification.sql",
        (
            "phone_verified",
            "verified_phone_hash",
            "unique_verified_phone_hash",
            "ADD COLUMN IF NOT EXISTS",
        ),
    ),
    (
        "20260624000001_oauth_authorization_tables.sql",
        (
            "oauth_authorization_requests",
            "oauth_authorization_codes",
            "oauth_authorization_requests_expires_idx",
            "oauth_authorization_codes_expires_idx",
            "code TEXT PRIMARY KEY",
            "ENABLE ROW LEVEL SECURITY",
            "oauth_authorization_requests_service_role_all",
            "oauth_authorization_codes_service_role_all",
        ),
    ),
)

HISTORICAL_MIGRATIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "20260527000001_create_story_drafts.sql",
        (
            "DEPRECATED",
            "story_drafts",
            "draft_id",
            "supabase_user_id",
            "payload JSONB",
            "ENABLE ROW LEVEL SECURITY",
            "story_drafts_service_role_all",
            "IF NOT EXISTS",
        ),
    ),
)

TIMESTAMP_PATTERN = re.compile(r"^\d{14}_[a-z0-9_]+\.sql$")


@pytest.mark.parametrize("filename,required_snippets", OPERATIONAL_MIGRATIONS)
def test_operational_migration_file_exists_with_required_sql(
    filename: str, required_snippets: tuple[str, ...]
) -> None:
    path = MIGRATIONS_DIR / filename
    assert path.is_file(), f"missing migration file: {path}"
    assert TIMESTAMP_PATTERN.match(filename), f"bad filename convention: {filename}"
    text = path.read_text(encoding="utf-8")
    for snippet in required_snippets:
        assert snippet in text, f"{filename} missing {snippet!r}"


@pytest.mark.parametrize("filename,required_snippets", POST_HISTORICAL_MIGRATIONS)
def test_post_historical_migration_file_exists_with_required_sql(
    filename: str, required_snippets: tuple[str, ...]
) -> None:
    path = MIGRATIONS_DIR / filename
    assert path.is_file(), f"missing migration file: {path}"
    text = path.read_text(encoding="utf-8")
    for snippet in required_snippets:
        assert snippet in text, f"{filename} missing {snippet!r}"


@pytest.mark.parametrize("filename,required_snippets", HISTORICAL_MIGRATIONS)
def test_historical_migration_file_exists_with_deprecated_header(
    filename: str, required_snippets: tuple[str, ...]
) -> None:
    path = MIGRATIONS_DIR / filename
    assert path.is_file(), f"missing historical migration file: {path}"
    text = path.read_text(encoding="utf-8")
    for snippet in required_snippets:
        assert snippet in text, f"{filename} missing {snippet!r}"


def test_migration_filenames_are_chronological() -> None:
    names = sorted(path.name for path in MIGRATIONS_DIR.glob("*.sql"))
    expected = [item[0] for item in OPERATIONAL_MIGRATIONS] + [
        item[0] for item in HISTORICAL_MIGRATIONS
    ] + [item[0] for item in POST_HISTORICAL_MIGRATIONS]
    assert names == expected


def test_identity_core_tables_covered_by_operational_migrations() -> None:
    sql = "\n".join(
        (MIGRATIONS_DIR / item[0]).read_text(encoding="utf-8")
        for item in OPERATIONAL_MIGRATIONS
    )
    for table in (
        "profiles",
        "eid_verification_sessions",
        "eid_audit_events",
    ):
        assert table in sql


def test_provider_state_columns_present() -> None:
    alter_sql = (
        MIGRATIONS_DIR / "20260526000001_eid_sessions_provider_abstraction.sql"
    ).read_text(encoding="utf-8")
    assert "provider TEXT NOT NULL DEFAULT 'eideasy'" in alter_sql
    assert "provider_session_data JSONB NOT NULL DEFAULT '{}'" in alter_sql


def test_profiles_critical_columns_for_healthcheck() -> None:
    profiles_sql = (
        MIGRATIONS_DIR / "20260525000001_create_profiles.sql"
    ).read_text(encoding="utf-8")
    for column in (
        "supabase_user_id",
        "eid_verified",
        "verified_person_hash",
        "eid_verified_at",
    ):
        assert column in profiles_sql


def test_profiles_phone_verification_columns_and_index() -> None:
    phone_sql = (
        MIGRATIONS_DIR / "20260611000001_profiles_phone_verification.sql"
    ).read_text(encoding="utf-8")
    for column in (
        "phone_verified",
        "verified_phone_hash",
        "phone_provider",
        "phone_dial_prefix",
        "phone_verified_at",
    ):
        assert column in phone_sql
    assert "unique_verified_phone_hash" in phone_sql
