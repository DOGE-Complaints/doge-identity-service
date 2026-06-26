from __future__ import annotations

from joserfc import jwt
from joserfc.errors import JoseError
from joserfc.jwk import OctKey

from core.domain.models import JwtValidationError, UserClaims

__all__ = ["JwtValidationError", "SupabaseJwtValidatorImpl", "UserClaims"]


class SupabaseJwtValidatorImpl:
    def __init__(self, *, jwt_secret: str, supabase_url: str) -> None:
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

    def validate(self, token: str) -> UserClaims:
        try:
            token_obj = jwt.decode(token, self._key, algorithms=["HS256"])
            self._claims_registry.validate(token_obj.claims)
        except JoseError as exc:
            raise JwtValidationError(f"JWT validation failed: {exc}") from exc
        except Exception as exc:
            raise JwtValidationError(f"JWT validation failed: {exc}") from exc

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
