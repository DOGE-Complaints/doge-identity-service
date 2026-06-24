from __future__ import annotations

from typing import Mapping

from fastapi import Depends, Request

from core.api.dependencies import ApiDependencies
from core.domain.contracts import SupabaseJwtValidator
from core.domain.models import JwtValidationError, UserClaims


class UnauthorizedError(Exception):
    code: str = "AUTHENTICATION_REQUIRED"

    def __init__(self, message: str = "Authentication required") -> None:
        self.message = message
        super().__init__(message)


class SupabaseJwtBearerTokenAuth:
    def __init__(self, *, validator: SupabaseJwtValidator) -> None:
        self._validator = validator

    def validate(self, headers: Mapping[str, str]) -> UserClaims:
        token = _extract_bearer_token(headers)
        if token is None:
            raise UnauthorizedError("Bearer token required")
        try:
            return self._validator.validate(token)
        except JwtValidationError as exc:
            raise UnauthorizedError("AUTHENTICATION_REQUIRED") from exc


class CompositeBearerTokenAuth:
    """Accept Supabase JWT or OAuth access tokens issued by this service."""

    def __init__(
        self,
        *,
        supabase_auth: SupabaseJwtBearerTokenAuth,
        oauth_token_service: object | None,
    ) -> None:
        self._supabase_auth = supabase_auth
        self._oauth_token_service = oauth_token_service

    def validate(self, headers: Mapping[str, str]) -> UserClaims:
        token = _extract_bearer_token(headers)
        if token is None:
            raise UnauthorizedError("Bearer token required")
        try:
            return self._supabase_auth._validator.validate(token)
        except JwtValidationError:
            pass
        oauth_service = self._oauth_token_service
        if oauth_service is not None:
            try:
                claims = oauth_service.validate_access_token(token)
            except ValueError as exc:
                raise UnauthorizedError("AUTHENTICATION_REQUIRED") from exc
            return UserClaims(
                supabase_user_id=claims.sub,
                email=None,
                role="authenticated",
            )
        raise UnauthorizedError("AUTHENTICATION_REQUIRED")


def _extract_bearer_token(headers: Mapping[str, str]) -> str | None:
    for key, value in headers.items():
        if key.lower() != "authorization":
            continue
        if not value.lower().startswith("bearer "):
            continue
        token = value[7:].strip()
        return token if token else None
    return None


def _get_api_dependencies() -> ApiDependencies:
    from core.api.asgi_app import get_api_dependencies

    return get_api_dependencies()


def get_current_user(
    request: Request,
    deps: ApiDependencies = Depends(_get_api_dependencies),
) -> UserClaims:
    headers = {name: value for name, value in request.headers.items()}
    return deps.bearer_token_auth.validate(headers)
