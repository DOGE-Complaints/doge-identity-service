"""STORY-IDS-VB-03 — offline attach success/failure for identity_verified."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from core.domain.models import ProfileRecord
from core.infrastructure.repositories import InMemoryProfileRepository, ProfileConflictError


def test_attach_phone_success_sets_identity_verified() -> None:
    repo = InMemoryProfileRepository()
    verified_at = datetime.now(timezone.utc)
    updated = repo.attach_phone_verification(
        user_id="u1",
        provider="mock",
        dial_prefix="+372",
        verified_phone_hash="phone-h",
        verified_at=verified_at,
        one_account_per_number=True,
    )
    assert updated.phone_verified is True
    assert updated.identity_verified is True


def test_attach_eid_success_sets_identity_verified() -> None:
    repo = InMemoryProfileRepository()
    verified_at = datetime.now(timezone.utc)
    updated = repo.attach_eid_verification(
        user_id="u1",
        provider="mock",
        country="EE",
        method="smart_id",
        verified_person_hash="person-h",
        verified_at=verified_at,
    )
    assert updated.eid_verified is True
    assert updated.identity_verified is True


def test_attach_phone_conflict_leaves_existing_opaque_unchanged() -> None:
    """Failure (hash conflict) must not clear already-true opaque on owner."""
    repo = InMemoryProfileRepository()
    verified_at = datetime.now(timezone.utc)
    owner = repo.attach_phone_verification(
        user_id="u1",
        provider="mock",
        dial_prefix="+372",
        verified_phone_hash="phone-h",
        verified_at=verified_at,
        one_account_per_number=True,
    )
    assert owner.identity_verified is True

    with pytest.raises(ProfileConflictError):
        repo.attach_phone_verification(
            user_id="u2",
            provider="mock",
            dial_prefix="+372",
            verified_phone_hash="phone-h",
            verified_at=verified_at,
            one_account_per_number=True,
        )

    still = repo.get_by_supabase_user_id("u1")
    assert still is not None
    assert still.identity_verified is True
    assert repo.get_by_supabase_user_id("u2") is None


def test_attach_eid_conflict_leaves_existing_opaque_unchanged() -> None:
    repo = InMemoryProfileRepository()
    verified_at = datetime.now(timezone.utc)
    owner = repo.attach_eid_verification(
        user_id="u1",
        provider="mock",
        country="EE",
        method="smart_id",
        verified_person_hash="person-h",
        verified_at=verified_at,
    )
    assert owner.identity_verified is True

    with pytest.raises(ProfileConflictError):
        repo.attach_eid_verification(
            user_id="u2",
            provider="mock",
            country="EE",
            method="smart_id",
            verified_person_hash="person-h",
            verified_at=verified_at,
        )

    still = repo.get_by_supabase_user_id("u1")
    assert still is not None
    assert still.identity_verified is True


def test_phone_conflict_does_not_clear_preexisting_opaque_on_challenger() -> None:
    """Challenger already opaque-true stays true when attach fails (no clear-on-failure)."""
    repo = InMemoryProfileRepository()
    verified_at = datetime.now(timezone.utc)
    now = verified_at
    repo.upsert(
        ProfileRecord(
            id="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            supabase_user_id="u2",
            display_name=None,
            avatar_url=None,
            eid_verified=False,
            verified_person_hash=None,
            eid_provider=None,
            eid_method=None,
            eid_country=None,
            eid_verified_at=None,
            phone_verified=False,
            verified_phone_hash=None,
            phone_provider=None,
            phone_dial_prefix=None,
            phone_verified_at=None,
            identity_verified=True,
            wallet_address=None,
            wallet_linked_at=None,
            wallet_signature_verified_at=None,
            wallet_signature_scheme=None,
            wallet_chain_id=None,
            created_at=now,
            updated_at=now,
        )
    )
    repo.attach_phone_verification(
        user_id="u1",
        provider="mock",
        dial_prefix="+372",
        verified_phone_hash="phone-h",
        verified_at=verified_at,
        one_account_per_number=True,
    )
    with pytest.raises(ProfileConflictError):
        repo.attach_phone_verification(
            user_id="u2",
            provider="mock",
            dial_prefix="+372",
            verified_phone_hash="phone-h",
            verified_at=verified_at,
            one_account_per_number=True,
        )
    challenger = repo.get_by_supabase_user_id("u2")
    assert challenger is not None
    assert challenger.identity_verified is True
    assert challenger.phone_verified is False
