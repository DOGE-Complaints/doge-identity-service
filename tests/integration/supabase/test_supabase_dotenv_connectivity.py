"""Live connectivity and schema probes against the dedicated test Supabase project."""

from __future__ import annotations

from tests.integration.supabase.conftest import _require_supabase_creds_from_dotenv


def test_supabase_connectivity() -> None:
    from core.infrastructure.db_supabase import SupabaseDatabase

    url, key = _require_supabase_creds_from_dotenv()
    db = SupabaseDatabase.from_http(url, key)
    assert db.healthcheck() is True, "Supabase connectivity check failed"


def test_supabase_identity_tables_ready() -> None:
    from core.infrastructure.db_supabase import SupabaseDatabase

    url, key = _require_supabase_creds_from_dotenv()
    db = SupabaseDatabase.from_http(url, key)
    assert db.required_tables_ready() is True, (
        "Required identity tables missing — run bootstrap SQL "
        "(profiles, eid_verification_sessions, eid_audit_events, story_drafts)"
    )


def test_supabase_identity_columns_ready() -> None:
    from core.infrastructure.db_supabase import SupabaseDatabase

    url, key = _require_supabase_creds_from_dotenv()
    db = SupabaseDatabase.from_http(url, key)
    assert db.required_columns_ready() is True, (
        "profiles identity columns not ready — apply EPIC-IDS-05 migrations"
    )


def test_supabase_provider_state_ready() -> None:
    from core.infrastructure.db_supabase import SupabaseDatabase

    url, key = _require_supabase_creds_from_dotenv()
    db = SupabaseDatabase.from_http(url, key)
    assert db.provider_state_ready() is True, (
        "eid_verification_sessions provider columns missing — apply req-17 migration"
    )


def test_supabase_service_role_policy() -> None:
    from core.infrastructure.db_supabase import SupabaseDatabase

    url, key = _require_supabase_creds_from_dotenv()
    db = SupabaseDatabase.from_http(url, key)
    assert db.service_role_policy_probe() is True, (
        "service_role cannot write eid_audit_events — check RLS policies for service_role"
    )
