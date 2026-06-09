from __future__ import annotations

from dataclasses import dataclass, field

import httpx

from core.security.oidc.discovery import OidcDiscoveryClient
from core.security.oidc.id_token import IdTokenValidator
from core.security.oidc.jwks_cache import JwksCache

__all__ = ["OidcToolkit", "build_oidc_toolkit"]


@dataclass
class OidcToolkit:
    discovery: OidcDiscoveryClient
    _http_client: httpx.Client
    _jwks_caches: dict[str, JwksCache] = field(default_factory=dict)

    def jwks_cache(self, jwks_uri: str) -> JwksCache:
        cached = self._jwks_caches.get(jwks_uri)
        if cached is not None:
            return cached
        cache = JwksCache(self._http_client, jwks_uri)
        self._jwks_caches[jwks_uri] = cache
        return cache

    def id_token_validator(self, jwks_uri: str) -> IdTokenValidator:
        return IdTokenValidator(self.jwks_cache(jwks_uri))


def build_oidc_toolkit(http_client: httpx.Client) -> OidcToolkit:
    return OidcToolkit(
        discovery=OidcDiscoveryClient(http_client),
        _http_client=http_client,
    )
