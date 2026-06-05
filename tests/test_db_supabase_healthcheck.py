from __future__ import annotations

from unittest.mock import patch

import httpx
import pytest

from core.infrastructure.db_supabase import SupabaseDatabase

_DB = SupabaseDatabase.from_http("https://example.supabase.co", "service-role-key")

_HEALTH_METHODS = (
    "healthcheck",
    "required_tables_ready",
    "required_columns_ready",
    "provider_state_ready",
    "service_role_policy_probe",
)


@pytest.mark.parametrize("method_name", _HEALTH_METHODS)
def test_health_methods_return_bool_and_never_raise(method_name: str) -> None:
    method = getattr(_DB, method_name)
    with patch.object(
        SupabaseDatabase,
        "_request",
        side_effect=httpx.ConnectError("network down"),
    ):
        result = method()
    assert result is False
    assert isinstance(result, bool)


def test_healthcheck_success_on_ok_response() -> None:
    with patch.object(SupabaseDatabase, "_request", return_value=[]):
        assert _DB.healthcheck() is True


def test_required_tables_ready_iterates_identity_tables() -> None:
    seen_paths: list[str] = []

    def _record_request(*, method: str, path: str, **kwargs: object) -> list[object]:
        del method, kwargs
        seen_paths.append(path)
        return []

    with patch.object(SupabaseDatabase, "_request", side_effect=_record_request):
        assert _DB.required_tables_ready() is True

    assert seen_paths == [
        "/rest/v1/profiles",
        "/rest/v1/eid_verification_sessions",
        "/rest/v1/eid_audit_events",
    ]


def test_service_role_policy_probe_posts_and_deletes_probe_event() -> None:
    calls: list[tuple[str, str]] = []

    def _record_request(*, method: str, path: str, **kwargs: object) -> None:
        del kwargs
        calls.append((method, path))
        return None

    with patch.object(SupabaseDatabase, "_request", side_effect=_record_request):
        assert _DB.service_role_policy_probe() is True

    assert calls[0] == ("POST", "/rest/v1/eid_audit_events")
    assert calls[1] == ("DELETE", "/rest/v1/eid_audit_events")
