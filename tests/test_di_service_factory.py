"""EPIC-IDS-06 Story 2 — provide_service_factory wiring (offline)."""

from __future__ import annotations

import pytest

from core.infrastructure.providers import provide_service_factory
from core.infrastructure.repositories import (
    InMemoryEIDAuditLogRepository,
    InMemoryHealthRepository,
    InMemoryOAuthClientStore,
    InMemoryProfileRepository,
    InMemoryVerificationSessionStore,
)
from core.infrastructure.service_factory import DefaultServiceFactory


def test_factory_for_in_memory() -> None:
    factory = provide_service_factory()
    assert isinstance(factory, DefaultServiceFactory)
    assert isinstance(factory.get_health_repository(), InMemoryHealthRepository)
    assert isinstance(factory.get_profile_repository(), InMemoryProfileRepository)
    assert isinstance(factory.get_verification_session_store(), InMemoryVerificationSessionStore)
    assert isinstance(factory.get_eid_audit_log_repository(), InMemoryEIDAuditLogRepository)
    assert isinstance(factory.get_oauth_client_store(), InMemoryOAuthClientStore)


def test_factory_raises_without_supabase_creds(monkeypatch: pytest.MonkeyPatch) -> None:
    """Post EPIC-IDS-05: supabase backend without creds raises ValueError (not InMemory fallback)."""
    monkeypatch.setenv("DB_BACKEND", "supabase")
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    with pytest.raises(ValueError, match="SUPABASE_URL and SUPABASE_SERVICE_ROLE"):
        provide_service_factory()


def test_factory_returns_same_instance_for_same_repository_call() -> None:
    factory = provide_service_factory()
    assert factory.get_profile_repository() is factory.get_profile_repository()
    assert factory.get_verification_session_store() is factory.get_verification_session_store()
