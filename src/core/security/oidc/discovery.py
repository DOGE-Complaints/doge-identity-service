from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

__all__ = ["OidcDiscoveryClient", "OidcDiscoveryDocument"]


@dataclass(frozen=True)
class OidcDiscoveryDocument:
    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    jwks_uri: str


class OidcDiscoveryClient:
    """Fetch and cache OpenID Provider Configuration documents."""

    def __init__(self, http_client: httpx.Client) -> None:
        self._http_client = http_client
        self._cache: dict[str, OidcDiscoveryDocument] = {}

    def get_discovery(self, issuer: str) -> OidcDiscoveryDocument:
        normalized_issuer = issuer.rstrip("/")
        cached = self._cache.get(normalized_issuer)
        if cached is not None:
            return cached

        url = f"{normalized_issuer}/.well-known/openid-configuration"
        response = self._http_client.get(url)
        response.raise_for_status()
        payload: dict[str, Any] = response.json()

        document = OidcDiscoveryDocument(
            issuer=str(payload["issuer"]).rstrip("/"),
            authorization_endpoint=str(payload["authorization_endpoint"]),
            token_endpoint=str(payload["token_endpoint"]),
            jwks_uri=str(payload["jwks_uri"]),
        )
        self._cache[normalized_issuer] = document
        return document
