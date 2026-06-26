from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from typing import Any, Iterator
from unittest.mock import patch

import pytest

from core.config.schema import AppConfig, DeploymentProfile
from core.domain.models import AuthorizationRequest
from core.infrastructure.db_supabase import (
    SupabaseAuthorizationRequestStore,
    SupabaseDatabase,
    SupabaseOAuthTokenService,
    _format_datetime,
    _parse_datetime,
)
from core.oauth.errors import OAuthGrantError

SUPABASE_URL = "https://test-project.supabase.co"
SERVICE_ROLE_KEY = "test-service-role-key"


def _demo_config(**overrides: object) -> AppConfig:
    base = {
        "profile": DeploymentProfile.DEMO,
        "port": 8100,
        "api_base_url": "http://localhost:8100",
        "log_level": "INFO",
        "log_format": "text",
        "request_timeout_s": 15,
        "oidc_request_timeout_s": 10,
        "supabase_url": SUPABASE_URL,
        "supabase_service_role": SERVICE_ROLE_KEY,
        "supabase_jwt_secret": "jwt-secret",
        "database_url": "",
        "authentigate_issuer": "",
        "authentigate_client_id": "",
        "authentigate_client_secret": "",
        "authentigate_redirect_uri": "",
        "authentigate_scopes": "",
        "eid_secret": "",
        "eid_session_enc_key": "2zy6gKOpxhkaNwtmufGZqYb0T88uh-tkKHC5ygQOnIM=",
        "node_id": "test-node",
        "oauth_access_token_secret": "demo-key",
        "oauth_access_token_ttl_s": 3600,
        "oauth_authorization_code_ttl_s": 300,
        "gpt_oauth_client_id": "",
        "gpt_oauth_client_secret": "",
        "gpt_oauth_redirect_uri": "",
        "eid_provider": "mock",
        "eideasy_env": "sandbox",
        "eideasy_base_url": "",
        "eideasy_client_id": "",
        "eideasy_client_secret": "",
        "eideasy_redirect_uri": "",
        "eideasy_allowed_methods": "",
        "eideasy_default_country": "EE",
        "eideasy_allowed_countries": "EE",
        "db_backend": "supabase",
        "db_enabled": True,
        "cors_allowed_origins": "*",
        "allowed_return_urls": "",
        "sms_provider": "mock",
        "phone_allowed_dial_prefixes": ("+372",),
        "phone_code_length": 6,
        "phone_code_ttl_s": 300,
        "phone_max_attempts": 5,
        "phone_resend_cooldown_s": 60,
        "phone_one_account_per_number": True,
        "rate_limit_eid_start_requests": 5,
        "rate_limit_eid_start_window_s": 600,
        "rate_limit_callback_requests": 5,
        "rate_limit_callback_window_s": 600,
        "rate_limit_trusted_proxy_count": 0,
        "rate_limit_phone_request_requests": 5,
        "rate_limit_phone_request_window_s": 600,
        "service_api_token": "",
    }
    base.update(overrides)
    return AppConfig(**base)


def _eq_value(raw: str) -> str:
    return raw.removeprefix("eq.")


def _gt_value(raw: str) -> datetime:
    return _parse_datetime(raw.removeprefix("gt.")) or datetime.now(timezone.utc)


class OAuthPostgrestMock:
    def __init__(self) -> None:
        self.authorization_requests: list[dict[str, Any]] = []
        self.authorization_codes: list[dict[str, Any]] = []

    def __call__(
        self,
        *,
        method: str,
        path: str,
        params: dict[str, str] | None = None,
        json_body: dict[str, Any] | None = None,
        prefer: str | None = None,
    ) -> list[dict[str, Any]] | None:
        params = params or {}
        if path == "/rest/v1/oauth_authorization_requests":
            return self._handle_requests(method, params, json_body, prefer)
        if path == "/rest/v1/oauth_authorization_codes":
            return self._handle_codes(method, params, json_body, prefer)
        raise AssertionError(f"unexpected PostgREST call: {method} {path}")

    def _handle_requests(
        self,
        method: str,
        params: dict[str, str],
        json_body: dict[str, Any] | None,
        prefer: str | None,
    ) -> list[dict[str, Any]] | None:
        if method == "POST":
            assert json_body is not None
            self.authorization_requests.append(dict(json_body))
            return None
        if method == "GET":
            oauth_request_id = _eq_value(params["oauth_request_id"])
            matches = [
                row
                for row in self.authorization_requests
                if row["oauth_request_id"] == oauth_request_id
            ]
            return matches[:1]
        if method == "DELETE":
            oauth_request_id = _eq_value(params["oauth_request_id"])
            self.authorization_requests = [
                row
                for row in self.authorization_requests
                if row["oauth_request_id"] != oauth_request_id
            ]
            return None
        raise AssertionError(f"unexpected requests method: {method}")

    def _handle_codes(
        self,
        method: str,
        params: dict[str, str],
        json_body: dict[str, Any] | None,
        prefer: str | None,
    ) -> list[dict[str, Any]] | None:
        if method == "POST":
            assert json_body is not None
            self.authorization_codes.append(dict(json_body))
            return None
        if method == "PATCH":
            code = _eq_value(params["code"])
            consumed_filter = _eq_value(params["consumed"])
            min_expires = _gt_value(params["expires_at"])
            for row in self.authorization_codes:
                expires_at = _parse_datetime(row["expires_at"]) or datetime.min.replace(
                    tzinfo=timezone.utc
                )
                if (
                    row["code"] == code
                    and str(row["consumed"]).lower() == consumed_filter
                    and expires_at > min_expires
                ):
                    row["consumed"] = json_body["consumed"] if json_body else True
                    if prefer == "return=representation":
                        return [dict(row)]
                    return None
            return []
        raise AssertionError(f"unexpected codes method: {method}")


def _demo_authorization_request(**overrides: object) -> AuthorizationRequest:
    now = datetime.now(timezone.utc)
    base = {
        "oauth_request_id": "req-1",
        "client_id": "gpt-client",
        "redirect_uri": "http://localhost/callback",
        "scopes": ["profile:read"],
        "state": "state-abc",
        "code_challenge": None,
        "code_challenge_method": None,
        "created_at": now,
        "expires_at": now + timedelta(minutes=10),
    }
    base.update(overrides)
    return AuthorizationRequest(**base)


@contextmanager
def mock_postgrest(mock: OAuthPostgrestMock) -> Iterator[SupabaseDatabase]:
    with patch.object(SupabaseDatabase, "_request", mock):
        yield SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)


def test_supabase_authorization_request_store_save_get_consume() -> None:
    mock = OAuthPostgrestMock()
    with mock_postgrest(mock) as db:
        store = SupabaseAuthorizationRequestStore(db)
        request = _demo_authorization_request()
        now = datetime.now(timezone.utc)

        store.save(request)
        loaded = store.get("req-1")
        assert loaded == request

        consumed = store.consume("req-1", now=now)
        assert consumed == request
        assert store.get("req-1") is None


def test_supabase_authorization_request_store_consume_expired_returns_none() -> None:
    mock = OAuthPostgrestMock()
    with mock_postgrest(mock) as db:
        store = SupabaseAuthorizationRequestStore(db)
        expired_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        request = _demo_authorization_request(expires_at=expired_at)
        store.save(request)

        consumed = store.consume("req-1", now=datetime.now(timezone.utc))
        assert consumed is None
        assert store.get("req-1") is None


def test_supabase_oauth_token_service_issue_and_consume_code() -> None:
    mock = OAuthPostgrestMock()
    with mock_postgrest(mock) as db:
        config = _demo_config()
        service = SupabaseOAuthTokenService(db, config=config)

        code = service.issue_authorization_code(
            supabase_user_id="22222222-2222-2222-2222-222222222222",
            client_id="gpt-client",
            scopes=["profile:read"],
            redirect_uri="http://localhost/callback",
        )
        assert len(mock.authorization_codes) == 1
        assert mock.authorization_codes[0]["code"] == code

        token = service.issue_access_token(
            code=code,
            client_id="gpt-client",
            client_secret="ignored",
            redirect_uri="http://localhost/callback",
        )
        assert token.count(".") == 2
        claims = service.validate_access_token(token)
        assert claims.sub == "22222222-2222-2222-2222-222222222222"
        assert claims.scopes == ["profile:read"]


def test_supabase_oauth_token_service_rejects_consumed_code() -> None:
    mock = OAuthPostgrestMock()
    with mock_postgrest(mock) as db:
        config = _demo_config()
        service = SupabaseOAuthTokenService(db, config=config)
        code = service.issue_authorization_code(
            supabase_user_id="user-1",
            client_id="gpt-client",
            scopes=["profile:read"],
            redirect_uri="http://localhost/callback",
        )
        service.issue_access_token(
            code=code,
            client_id="gpt-client",
            client_secret="ignored",
            redirect_uri="http://localhost/callback",
        )

        with pytest.raises(OAuthGrantError):
            service.issue_access_token(
                code=code,
                client_id="gpt-client",
                client_secret="ignored",
                redirect_uri="http://localhost/callback",
            )


def test_supabase_oauth_token_service_rejects_expired_code() -> None:
    mock = OAuthPostgrestMock()
    with mock_postgrest(mock) as db:
        config = _demo_config()
        service = SupabaseOAuthTokenService(db, config=config)
        code = service.issue_authorization_code(
            supabase_user_id="user-1",
            client_id="gpt-client",
            scopes=["profile:read"],
            redirect_uri="http://localhost/callback",
        )
        mock.authorization_codes[0]["expires_at"] = _format_datetime(
            datetime.now(timezone.utc) - timedelta(seconds=30)
        )

        with pytest.raises(OAuthGrantError):
            service.issue_access_token(
                code=code,
                client_id="gpt-client",
                client_secret="ignored",
                redirect_uri="http://localhost/callback",
            )


def test_durability_authorization_code_survives_store_recreate() -> None:
    mock = OAuthPostgrestMock()
    with mock_postgrest(mock) as db:
        config = _demo_config()
        service_a = SupabaseOAuthTokenService(db, config=config)
        code = service_a.issue_authorization_code(
            supabase_user_id="user-1",
            client_id="gpt-client",
            scopes=["profile:read"],
            redirect_uri="http://localhost/callback",
        )

        service_b = SupabaseOAuthTokenService(db, config=config)
        token = service_b.issue_access_token(
            code=code,
            client_id="gpt-client",
            client_secret="ignored",
            redirect_uri="http://localhost/callback",
        )
        assert service_b.validate_access_token(token).sub == "user-1"


def test_stateless_access_token_validates_without_db_reads() -> None:
    mock = OAuthPostgrestMock()
    with mock_postgrest(mock) as db:
        config = _demo_config()
        issuer = SupabaseOAuthTokenService(db, config=config)
        code = issuer.issue_authorization_code(
            supabase_user_id="user-1",
            client_id="gpt-client",
            scopes=["profile:read"],
            redirect_uri="http://localhost/callback",
        )
        token = issuer.issue_access_token(
            code=code,
            client_id="gpt-client",
            client_secret="ignored",
            redirect_uri="http://localhost/callback",
        )

    validator_db = SupabaseDatabase.from_http(SUPABASE_URL, SERVICE_ROLE_KEY)
    validator = SupabaseOAuthTokenService(validator_db, config=config)
    with patch.object(SupabaseDatabase, "_request") as mock_request:
        claims = validator.validate_access_token(token)
    mock_request.assert_not_called()
    assert claims.sub == "user-1"
