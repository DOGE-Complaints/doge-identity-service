from __future__ import annotations

import time
from collections.abc import Callable

import httpx
from joserfc.errors import InvalidKeyIdError
from joserfc.jwk import KeySet

__all__ = ["JwksCache"]


class JwksCache:
    """TTL cache for JWKS with refresh-on-unknown-kid."""

    def __init__(
        self,
        http_client: httpx.Client,
        jwks_uri: str,
        *,
        ttl_seconds: int = 3600,
        clock: Callable[[], float] | None = None,
    ) -> None:
        self._http_client = http_client
        self._jwks_uri = jwks_uri
        self._ttl_seconds = ttl_seconds
        self._clock = clock or time.time
        self._key_set: KeySet | None = None
        self._fetched_at: float | None = None

    def get_key_set(self, *, force_refresh: bool = False) -> KeySet:
        now = self._clock()
        if (
            not force_refresh
            and self._key_set is not None
            and self._fetched_at is not None
            and (now - self._fetched_at) < self._ttl_seconds
        ):
            return self._key_set

        response = self._http_client.get(self._jwks_uri)
        response.raise_for_status()
        self._key_set = KeySet.import_key_set(response.json())
        self._fetched_at = now
        return self._key_set

    def resolve_key_set_for_kid(self, kid: str) -> KeySet:
        key_set = self.get_key_set()
        try:
            key_set.get_by_kid(kid)
            return key_set
        except InvalidKeyIdError:
            refreshed = self.get_key_set(force_refresh=True)
            refreshed.get_by_kid(kid)
            return refreshed
