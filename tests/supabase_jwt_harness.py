"""Shared ES256 + mock-JWKS helpers for Supabase Bearer tokens in offline tests."""

from __future__ import annotations

import base64
import json
import time
from typing import Callable

import httpx
import pytest
from joserfc import jwt
from joserfc.jwk import ECKey, KeySet

from core.auth.supabase_validator import SupabaseJwtValidatorImpl
from core.security.oidc.jwks_cache import JwksCache

TEST_SUPABASE_URL = "https://test-project.supabase.co"
DEFAULT_USER_ID = "11111111-1111-1111-1111-111111111111"
_SIGNING_KEY: ECKey | None = None


def _signing_key() -> ECKey:
    global _SIGNING_KEY
    if _SIGNING_KEY is None:
        _SIGNING_KEY = ECKey.generate_key("P-256", parameters={"kid": "test-es256-kid"})
    return _SIGNING_KEY


def jwks_uri() -> str:
    return f"{TEST_SUPABASE_URL.rstrip('/')}/auth/v1/.well-known/jwks.json"


def jwks_payload() -> dict[str, list[dict[str, object]]]:
    key = _signing_key()
    return {"keys": [key.as_dict(private=False)]}


def jwks_http_handler() -> Callable[[httpx.Request], httpx.Response]:
    def handler(request: httpx.Request) -> httpx.Response:
        if str(request.url).endswith("/.well-known/jwks.json"):
            return httpx.Response(200, json=jwks_payload())
        return httpx.Response(404, text="not found")

    return handler


def build_jwks_http_client() -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(jwks_http_handler()))


def build_test_jwks_cache() -> JwksCache:
    return JwksCache(build_jwks_http_client(), jwks_uri())


def build_test_validator(*, supabase_url: str = TEST_SUPABASE_URL) -> SupabaseJwtValidatorImpl:
    return SupabaseJwtValidatorImpl(
        supabase_url=supabase_url,
        jwks_cache=build_test_jwks_cache(),
    )


def mint_supabase_access_token(
    *,
    user_id: str = DEFAULT_USER_ID,
    email: str | None = "user@example.com",
    supabase_url: str = TEST_SUPABASE_URL,
    exp_offset: int = 3600,
    iss: str | None = None,
    aud: str | None = "authenticated",
    role: str = "authenticated",
    signing_key: ECKey | None = None,
) -> str:
    key = signing_key or _signing_key()
    kid = key.as_dict()["kid"]
    now = int(time.time())
    claims: dict[str, object] = {
        "sub": user_id,
        "role": role,
        "iss": iss if iss is not None else f"{supabase_url.rstrip('/')}/auth/v1",
        "exp": now + exp_offset,
        "iat": now,
    }
    if email is not None:
        claims["email"] = email
    if aud is not None:
        claims["aud"] = aud
    return jwt.encode({"alg": "ES256", "kid": kid}, claims, key)


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def mint_header_alg_token(
    alg: str,
    *,
    supabase_url: str = TEST_SUPABASE_URL,
    user_id: str = DEFAULT_USER_ID,
) -> str:
    now = int(time.time())
    claims = {
        "sub": user_id,
        "role": "authenticated",
        "aud": "authenticated",
        "iss": f"{supabase_url.rstrip('/')}/auth/v1",
        "exp": now + 3600,
    }
    header = _b64url(json.dumps({"alg": alg, "typ": "JWT"}).encode())
    payload = _b64url(json.dumps(claims).encode())
    return f"{header}.{payload}.invalid-signature"


def mint_alg_none_token(*, supabase_url: str = TEST_SUPABASE_URL) -> str:
    return mint_header_alg_token("none", supabase_url=supabase_url)


def install_test_supabase_jwt_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUPABASE_URL", TEST_SUPABASE_URL)


def patch_providers_httpx_client_for_jwks(monkeypatch: pytest.MonkeyPatch) -> None:
    real_client = httpx.Client

    def factory(*args: object, **kwargs: object) -> httpx.Client:
        if kwargs.get("transport") is not None:
            return real_client(*args, **kwargs)
        kwargs["transport"] = httpx.MockTransport(jwks_http_handler())
        return real_client(*args, **kwargs)

    monkeypatch.setattr("core.infrastructure.providers.httpx.Client", factory)


def mint_with_foreign_key(
    *,
    supabase_url: str = TEST_SUPABASE_URL,
    user_id: str = DEFAULT_USER_ID,
) -> str:
    foreign_key = ECKey.generate_key("P-256", parameters={"kid": "foreign-kid"})
    return mint_supabase_access_token(
        user_id=user_id,
        supabase_url=supabase_url,
        signing_key=foreign_key,
    )


def key_set_for_tests() -> KeySet:
    return KeySet.import_key_set(jwks_payload())
