from __future__ import annotations

import ast
from pathlib import Path

import pytest

from core.domain.contracts import (
    BearerTokenAuth,
    EIDAuditLogRepository,
    HealthRepository,
    OAuthClientStore,
    OAuthTokenService,
    ProfileRepository,
    SupabaseJwtValidator,
    VerificationSessionStore,
)
from core.domain.models import (
    EIDAuditEvent,
    OAuthClient,
    ProfileRecord,
    VerificationSession,
)


DOMAIN_DIR = Path(__file__).resolve().parents[1] / "src" / "core" / "domain"
FORBIDDEN_IMPORT_PREFIXES = (
    "core.infrastructure",
    "httpx",
    "fastapi",
    "joserfc",
)


def _protocol_classes() -> tuple[type, ...]:
    return (
        HealthRepository,
        ProfileRepository,
        VerificationSessionStore,
        EIDAuditLogRepository,
        OAuthClientStore,
        OAuthTokenService,
        SupabaseJwtValidator,
        BearerTokenAuth,
    )


def test_contracts_import_without_error() -> None:
    for protocol in _protocol_classes():
        assert protocol.__name__


def test_all_protocols_are_runtime_checkable() -> None:
    for protocol in _protocol_classes():
        assert isinstance(protocol, type)
        assert getattr(protocol, "_is_runtime_protocol", False) or hasattr(
            protocol, "__protocol_attrs__"
        )


def test_models_import_without_error() -> None:
    assert ProfileRecord is not None
    assert VerificationSession is not None
    assert EIDAuditEvent is not None


def test_domain_models_do_not_define_unauthorized_error() -> None:
    import core.domain.models as models_module

    assert not hasattr(models_module, "UnauthorizedError")


def test_frozen_models_allow_shallow_list_mutation() -> None:
    """S1-2 policy: frozen=True blocks field reassignment, not in-place list mutation."""
    client = OAuthClient(
        client_id="c1",
        client_secret_hash="hash",
        redirect_uri="http://localhost/cb",
        scopes=["profile:read"],
    )
    client.scopes.append("stories:draft")
    assert client.scopes == ["profile:read", "stories:draft"]


def test_domain_layer_has_no_forbidden_imports() -> None:
    violations: list[str] = []
    for path in DOMAIN_DIR.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name
                    if any(
                        module_name == prefix or module_name.startswith(f"{prefix}.")
                        for prefix in FORBIDDEN_IMPORT_PREFIXES
                    ):
                        violations.append(f"{path.name}: import {module_name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module is None:
                    continue
                module_name = node.module
                if any(
                    module_name == prefix or module_name.startswith(f"{prefix}.")
                    for prefix in FORBIDDEN_IMPORT_PREFIXES
                ):
                    violations.append(f"{path.name}: from {module_name} import ...")
    assert violations == [], f"Forbidden imports in domain layer: {violations}"
