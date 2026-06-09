from __future__ import annotations

from typing import Any

from joserfc import jwt
from joserfc.errors import InvalidKeyIdError, JoseError

from core.providers.base import EidErrorCode
from core.security.oidc.jwks_cache import JwksCache

__all__ = ["IdTokenValidator", "OidcIdTokenValidationError"]


class OidcIdTokenValidationError(Exception):
    """OIDC id_token validation failure mapped to canonical EID error codes."""

    def __init__(
        self,
        message: str,
        *,
        code: EidErrorCode = EidErrorCode.IDENTITY_VALIDATION_FAILED,
    ) -> None:
        self.code = code
        super().__init__(message)


class IdTokenValidator:
    """Validate OIDC id_token signatures and standard claims."""

    def __init__(self, jwks_cache: JwksCache) -> None:
        self._jwks_cache = jwks_cache

    def validate(
        self,
        id_token: str,
        *,
        expected_iss: str,
        expected_aud: str,
        expected_nonce: str,
    ) -> dict[str, Any]:
        token = None
        for force_refresh in (False, True):
            key_set = self._jwks_cache.get_key_set(force_refresh=force_refresh)
            try:
                token = jwt.decode(id_token, key_set, algorithms=["RS256"])
                break
            except InvalidKeyIdError as exc:
                if force_refresh:
                    raise OidcIdTokenValidationError(
                        f"id_token signing key not found: {exc}",
                    ) from exc
            except JoseError as exc:
                raise OidcIdTokenValidationError(
                    f"id_token signature validation failed: {exc}",
                ) from exc

        if token is None:
            raise OidcIdTokenValidationError("id_token validation failed")

        claims_registry = jwt.JWTClaimsRegistry(
            iss={"essential": True, "value": expected_iss.rstrip("/")},
            aud={"essential": True, "value": expected_aud},
            exp={"essential": True},
            iat={"essential": True},
            nonce={"essential": True, "value": expected_nonce},
        )
        try:
            claims_registry.validate(token.claims)
        except JoseError as exc:
            raise OidcIdTokenValidationError(
                f"id_token claims validation failed: {exc}",
            ) from exc

        return dict(token.claims)
