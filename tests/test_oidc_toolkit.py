"""EPIC-IDS-09 STORY-IDS-EID-07 — provider-agnostic OIDC toolkit (offline)."""

from __future__ import annotations

import json
from unittest.mock import patch

import httpx
import pytest
from joserfc import jwt
from joserfc.jwk import KeySet, RSAKey

from core.config.schema import AppConfig
from core.config.providers import provide_app_config
from core.infrastructure.repositories import InMemoryVerificationSessionStore
from core.providers.base import EidErrorCode
from core.providers.runtime_factory import build_provider_runtime
from core.security.oidc import (
    IdTokenValidator,
    JwksCache,
    OidcDiscoveryClient,
    OidcIdTokenValidationError,
    OidcToolkit,
    build_oidc_toolkit,
)

_ISSUER = "https://issuer.example"
_JWKS_URI = f"{_ISSUER}/jwks"
_CLIENT_ID = "client-id"
_NONCE = "nonce-123"
_DISCOVERY_URL = f"{_ISSUER}/.well-known/openid-configuration"


def _discovery_payload() -> dict[str, str]:
    return {
        "issuer": _ISSUER,
        "authorization_endpoint": f"{_ISSUER}/auth",
        "token_endpoint": f"{_ISSUER}/token",
        "jwks_uri": _JWKS_URI,
    }


def _rsa_key(*, kid: str) -> RSAKey:
    return RSAKey.generate_key(2048, parameters={"kid": kid})


def _jwks_payload(*keys: RSAKey) -> dict[str, list[dict[str, object]]]:
    return {"keys": [key.as_dict(private=False) for key in keys]}


def _encode_id_token(
    key: RSAKey,
    *,
    iss: str = _ISSUER,
    aud: str = _CLIENT_ID,
    nonce: str = _NONCE,
    exp: int = 9_999_999_999,
    iat: int = 1,
) -> str:
    kid = key.as_dict()["kid"]
    claims = {
        "iss": iss,
        "aud": aud,
        "exp": exp,
        "iat": iat,
        "nonce": nonce,
    }
    return jwt.encode({"alg": "RS256", "kid": kid}, claims, key)


class _MockOidcTransport:
    def __init__(self, *, jwks_responses: list[dict[str, list[dict[str, object]]]]) -> None:
        self.discovery_calls = 0
        self.jwks_calls = 0
        self._jwks_responses = list(jwks_responses)

    def handler(self, request: httpx.Request) -> httpx.Response:
        if request.url == httpx.URL(_DISCOVERY_URL):
            self.discovery_calls += 1
            return httpx.Response(200, json=_discovery_payload())
        if request.url == httpx.URL(_JWKS_URI):
            self.jwks_calls += 1
            payload = self._jwks_responses[min(self.jwks_calls - 1, len(self._jwks_responses) - 1)]
            return httpx.Response(200, json=payload)
        return httpx.Response(404, text="not found")


def _http_client(transport: _MockOidcTransport) -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(transport.handler))


def test_discovery_client_caches_openid_configuration() -> None:
    transport = _MockOidcTransport(jwks_responses=[{"keys": []}])
    client = _http_client(transport)
    discovery = OidcDiscoveryClient(client)

    first = discovery.get_discovery(_ISSUER)
    second = discovery.get_discovery(_ISSUER)

    assert first == second
    assert first.issuer == _ISSUER
    assert first.jwks_uri == _JWKS_URI
    assert transport.discovery_calls == 1


def test_jwks_cache_resolves_unknown_kid_after_refresh() -> None:
    old_key = _rsa_key(kid="old-kid")
    new_key = _rsa_key(kid="new-kid")
    transport = _MockOidcTransport(
        jwks_responses=[
            _jwks_payload(old_key),
            _jwks_payload(new_key),
        ],
    )
    cache = JwksCache(_http_client(transport), _JWKS_URI, ttl_seconds=3600, clock=lambda: 0.0)

    key_set = cache.resolve_key_set_for_kid(new_key.as_dict()["kid"])

    assert transport.jwks_calls == 2
    assert key_set.get_by_kid(new_key.as_dict()["kid"]) is not None


def test_id_token_validator_accepts_valid_rs256_token() -> None:
    key = _rsa_key(kid="signing-key")
    transport = _MockOidcTransport(jwks_responses=[_jwks_payload(key)])
    toolkit = build_oidc_toolkit(_http_client(transport))
    validator = toolkit.id_token_validator(_JWKS_URI)
    token = _encode_id_token(key)

    claims = validator.validate(
        token,
        expected_iss=_ISSUER,
        expected_aud=_CLIENT_ID,
        expected_nonce=_NONCE,
    )

    assert claims["iss"] == _ISSUER
    assert claims["aud"] == _CLIENT_ID
    assert claims["nonce"] == _NONCE


@pytest.mark.parametrize(
    ("token_factory", "expected_fragment"),
    [
        (
            lambda key, other: jwt.encode(
                {"alg": "RS256", "kid": key.as_dict()["kid"]},
                {
                    "iss": _ISSUER,
                    "aud": _CLIENT_ID,
                    "exp": 9_999_999_999,
                    "iat": 1,
                    "nonce": _NONCE,
                },
                other,
            ),
            "signature validation failed",
        ),
        (
            lambda key, _: _encode_id_token(key, iss="https://wrong.example"),
            "claims validation failed",
        ),
        (
            lambda key, _: _encode_id_token(key, aud="wrong-client"),
            "claims validation failed",
        ),
        (
            lambda key, _: _encode_id_token(key, nonce="wrong-nonce"),
            "claims validation failed",
        ),
        (
            lambda key, _: _encode_id_token(key, exp=1),
            "claims validation failed",
        ),
    ],
)
def test_id_token_validator_maps_failures_to_identity_validation_failed(
    token_factory,
    expected_fragment: str,
) -> None:
    signing_key = _rsa_key(kid="signing-key")
    other_key = _rsa_key(kid="other-key")
    transport = _MockOidcTransport(jwks_responses=[_jwks_payload(signing_key)])
    validator = IdTokenValidator(JwksCache(_http_client(transport), _JWKS_URI))
    token = token_factory(signing_key, other_key)

    with pytest.raises(OidcIdTokenValidationError) as exc_info:
        validator.validate(
            token,
            expected_iss=_ISSUER,
            expected_aud=_CLIENT_ID,
            expected_nonce=_NONCE,
        )

    assert exc_info.value.code is EidErrorCode.IDENTITY_VALIDATION_FAILED
    assert expected_fragment in str(exc_info.value)


def test_id_token_validator_refreshes_jwks_on_unknown_kid() -> None:
    old_key = _rsa_key(kid="old-kid")
    new_key = _rsa_key(kid="new-kid")
    transport = _MockOidcTransport(
        jwks_responses=[
            _jwks_payload(old_key),
            _jwks_payload(new_key),
        ],
    )
    validator = IdTokenValidator(JwksCache(_http_client(transport), _JWKS_URI))
    token = _encode_id_token(new_key)

    claims = validator.validate(
        token,
        expected_iss=_ISSUER,
        expected_aud=_CLIENT_ID,
        expected_nonce=_NONCE,
    )

    assert transport.jwks_calls == 2
    assert claims["nonce"] == _NONCE


def test_oidc_toolkit_reuses_jwks_cache_per_uri() -> None:
    key = _rsa_key(kid="signing-key")
    transport = _MockOidcTransport(jwks_responses=[_jwks_payload(key)])
    toolkit = OidcToolkit(
        discovery=OidcDiscoveryClient(_http_client(transport)),
        _http_client=_http_client(transport),
    )

    first = toolkit.jwks_cache(_JWKS_URI)
    second = toolkit.jwks_cache(_JWKS_URI)

    assert first is second


def test_build_provider_runtime_wires_oidc_for_non_mock_provider() -> None:
    store = InMemoryVerificationSessionStore()
    config = provide_app_config()
    non_mock = AppConfig(**{**config.__dict__, "eid_provider": "eideasy", "db_backend": "in_memory"})
    with patch("core.providers.runtime_factory.httpx.Client") as mock_client:
        sentinel = httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(200)))
        mock_client.return_value = sentinel
        runtime = build_provider_runtime(config=non_mock, session_store=store)

    assert runtime.http_client is sentinel
    assert runtime.oidc is not None
    assert isinstance(runtime.oidc, OidcToolkit)


def test_build_provider_runtime_omits_oidc_in_mock_mode() -> None:
    store = InMemoryVerificationSessionStore()
    config = provide_app_config()
    mock_config = AppConfig(**{**config.__dict__, "eid_provider": "mock", "db_backend": "in_memory"})
    runtime = build_provider_runtime(config=mock_config, session_store=store)

    assert runtime.http_client is None
    assert runtime.oidc is None
