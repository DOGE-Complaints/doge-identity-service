"""Stateless HS256 access-token JWT helpers (OAUTH-01/OAUTH-03)."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time

from core.config.schema import AppConfig
from core.domain.models import OAuthTokenClaims


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def encode_access_token_jwt(config: AppConfig, payload: dict[str, object]) -> str:
    secret = config.oauth_access_token_secret or "demo-key"
    header = {"alg": "HS256", "typ": "JWT"}
    header_segment = b64url_encode(
        json.dumps(header, separators=(",", ":")).encode("utf-8")
    )
    payload_segment = b64url_encode(
        json.dumps(payload, separators=(",", ":")).encode("utf-8")
    )
    signing_input = f"{header_segment}.{payload_segment}".encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    return f"{header_segment}.{payload_segment}.{b64url_encode(signature)}"


def decode_access_token_jwt(config: AppConfig, token: str) -> dict[str, object]:
    secret = config.oauth_access_token_secret or "demo-key"
    try:
        header_segment, payload_segment, signature_segment = token.split(".")
    except ValueError as exc:
        raise ValueError("invalid_token") from exc
    signing_input = f"{header_segment}.{payload_segment}".encode("utf-8")
    expected_sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(b64url_encode(expected_sig), signature_segment):
        raise ValueError("invalid_token")
    payload = json.loads(b64url_decode(payload_segment))
    if int(payload["exp"]) < int(time.time()):
        raise ValueError("invalid_token")
    return payload


def claims_from_access_token_jwt(config: AppConfig, token: str) -> OAuthTokenClaims:
    payload = decode_access_token_jwt(config, token)
    scope_raw = payload.get("scope", "")
    scopes = scope_raw.split() if scope_raw else []
    return OAuthTokenClaims(
        sub=str(payload["sub"]),
        scopes=scopes,
        exp=int(payload["exp"]),
        client_id=str(payload.get("client_id", "")),
    )
