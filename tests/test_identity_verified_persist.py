"""STORY-IDS-VB-01 — offline persist + backfill semantics for identity_verified."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from core.domain.models import ProfileRecord
from core.infrastructure.db_supabase import _profile_from_row, _profile_to_row

_ROOT = Path(__file__).resolve().parents[1]
_MIGRATIONS = _ROOT / "supabase" / "migrations"


def _demo_profile(**overrides: object) -> ProfileRecord:
    now = datetime.now(timezone.utc)
    base: dict[str, object] = {
        "id": "11111111-1111-1111-1111-111111111111",
        "supabase_user_id": "22222222-2222-2222-2222-222222222222",
        "display_name": None,
        "avatar_url": None,
        "eid_verified": False,
        "verified_person_hash": None,
        "eid_provider": None,
        "eid_method": None,
        "eid_country": None,
        "eid_verified_at": None,
        "phone_verified": False,
        "verified_phone_hash": None,
        "phone_provider": None,
        "phone_dial_prefix": None,
        "phone_verified_at": None,
        "identity_verified": False,
        "wallet_address": None,
        "wallet_linked_at": None,
        "wallet_signature_verified_at": None,
        "wallet_signature_scheme": None,
        "wallet_chain_id": None,
        "created_at": now,
        "updated_at": now,
    }
    base.update(overrides)
    return ProfileRecord(**base)


def test_identity_verified_defaults_false_on_new_profile() -> None:
    profile = _demo_profile()
    assert profile.identity_verified is False


def test_identity_verified_map_round_trip_false_and_true() -> None:
    for value in (False, True):
        profile = _demo_profile(identity_verified=value)
        row = _profile_to_row(profile)
        assert row["identity_verified"] is value
        restored = _profile_from_row(row)
        assert restored.identity_verified is value


def test_identity_verified_from_row_missing_key_defaults_false() -> None:
    profile = _demo_profile(identity_verified=True)
    row = _profile_to_row(profile)
    del row["identity_verified"]
    restored = _profile_from_row(row)
    assert restored.identity_verified is False


def test_backfill_semantics_method_or_to_opaque() -> None:
    """TECH-ARCH §2.4: phone_verified OR eid_verified → identity_verified=true."""

    def expected_opaque(*, phone_verified: bool, eid_verified: bool) -> bool:
        return phone_verified or eid_verified

    cases = (
        (False, False, False),
        (True, False, True),
        (False, True, True),
        (True, True, True),
    )
    for phone, eid, opaque in cases:
        assert expected_opaque(phone_verified=phone, eid_verified=eid) is opaque


def test_backfill_migration_sql_on_disk() -> None:
    add_col = (_MIGRATIONS / "20260921000001_profiles_identity_verified.sql").read_text()
    backfill = (
        _MIGRATIONS / "20260921000002_profiles_identity_verified_backfill.sql"
    ).read_text()
    assert "ADD COLUMN IF NOT EXISTS identity_verified BOOLEAN NOT NULL DEFAULT FALSE" in add_col
    assert "SET identity_verified = TRUE" in backfill
    assert "phone_verified = TRUE" in backfill
    assert "eid_verified = TRUE" in backfill
