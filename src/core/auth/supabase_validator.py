from __future__ import annotations

import base64
import json

import httpx
from joserfc import jwt
from joserfc.errors import InvalidKeyIdError, JoseError
from joserfc.jwk import OctKey

from core.domain.models import JwtValidationError, UserClaims
from core.security.oidc.jwks_cache import JwksCache

__all__ = ["JwtValidationError", "SupabaseJwtValidatorImpl", "UserClaims"]

_JWKS_ALGORITHMS = frozenset({"ES256", "RS256", "ES384", "ES512"})


def _header_alg(token: str) -> str | None:
    try:
        header_segment = token.split(".", 1)[0]
        padding = "=" * (-len(header_segment) % 4)
        header_json = base64.urlsafe_b64decode(header_segment + padding)
        header = json.loads(header_json.decode("utf-8"))
        alg = header.get("alg")
        return str(alg) if alg else None
    except (IndexError, ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return None


class SupabaseJwtValidatorImpl:
    def __init__(
        self,
        *,
        jwt_secret: str,
        supabase_url: str,
        http_client: httpx.Client | None = None,
        request_timeout_s: float = 15.0,
    ) -> None:
        self._jwt_secret = jwt_secret
        self._supabase_url = supabase_url.rstrip("/")
        self._expected_iss = f"{self._supabase_url}/auth/v1"
        self._key = OctKey.import_key(jwt_secret)
        self._claims_registry = jwt.JWTClaimsRegistry(
            iss={"essential": True, "value": self._expected_iss},
            sub={"essential": True},
            exp={"essential": True},
            aud={"essential": True, "value": "authenticated"},
        )
        self._jwks_cache: JwksCache | None = None
        if self._supabase_url and not self._supabase_url.endswith("demo.local"):
            jwks_uri = f"{self._supabase_url}/auth/v1/.well-known/jwks.json"
            client = http_client or httpx.Client(timeout=request_timeout_s)
            self._jwks_cache = JwksCache(client, jwks_uri)

    def _claims_from_token(self, token_obj: jwt.Token) -> UserClaims:
        self._claims_registry.validate(token_obj.claims)
        claims = token_obj.claims
        if claims.get("role") != "authenticated":
            raise JwtValidationError("Token role is not 'authenticated'")

        sub = claims.get("sub")
        if not sub:
            raise JwtValidationError("JWT sub missing")

        return UserClaims(
            supabase_user_id=str(sub),
            email=claims.get("email"),
            role=str(claims["role"]),
        )

    def _validate_hs256(self, token: str) -> UserClaims:
        token_obj = jwt.decode(token, self._key, algorithms=["HS256"])
        return self._claims_from_token(token_obj)

    def _validate_jwks(self, token: str, alg: str) -> UserClaims:
        if self._jwks_cache is None:
            raise JwtValidationError(f"JWKS validation unavailable for alg={alg}")

        token_obj = None
        for force_refresh in (False, True):
            key_set = self._jwks_cache.get_key_set(force_refresh=force_refresh)
            try:
                token_obj = jwt.decode(token, key_set, algorithms=[alg])
                break
            except InvalidKeyIdError as exc:
                if force_refresh:
                    raise JwtValidationError(
                        f"JWT signing key not found: {exc}"
                    ) from exc
            except JoseError as exc:
                raise JwtValidationError(f"JWT validation failed: {exc}") from exc

        if token_obj is None:
            raise JwtValidationError("JWT validation failed")
        return self._claims_from_token(token_obj)

    def validate(self, token: str) -> UserClaims:
        alg = _header_alg(token)
        try:
            if alg == "HS256":
                return self._validate_hs256(token)
            if alg in _JWKS_ALGORITHMS:
                return self._validate_jwks(token, alg)
            raise JwtValidationError(f"Unsupported JWT algorithm: {alg!r}")
        except JwtValidationError:
            raise
        except JoseError as exc:
            raise JwtValidationError(f"JWT validation failed: {exc}") from exc
        except Exception as exc:
            raise JwtValidationError(f"JWT validation failed: {exc}") from exc
