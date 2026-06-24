from __future__ import annotations

import secrets
from dataclasses import dataclass
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


def _lower_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {str(k).lower(): str(v) for k, v in headers.items()}


def extract_service_token(headers: Mapping[str, str]) -> str | None:
    """Read token from Authorization: Bearer … or X-Service-Token."""
    h = _lower_headers(headers)
    auth = h.get("authorization")
    if auth and auth.lower().startswith("bearer "):
        token = auth[7:].strip()
        return token if token else None
    xst = h.get("x-service-token")
    if xst:
        t = xst.strip()
        return t if t else None
    return None


@dataclass(frozen=True)
class ServiceTokenAuth:
    """Service-to-service gate: optional; when disabled, require() is a no-op."""

    _expected: str | None

    @classmethod
    def disabled(cls) -> ServiceTokenAuth:
        return cls(_expected=None)

    @classmethod
    def from_secret(cls, secret: str) -> ServiceTokenAuth:
        s = secret.strip()
        if not s:
            return cls.disabled()
        return cls(_expected=s)

    def is_enabled(self) -> bool:
        return self._expected is not None

    def require(self, headers: Mapping[str, str]) -> None:
        if not self.is_enabled():
            return
        assert self._expected is not None
        got = extract_service_token(headers)
        if got is None:
            raise UnauthorizedError("Missing service API token.")
        if not secrets.compare_digest(got, self._expected):
            raise UnauthorizedError("Invalid service API token.")


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


def require_service_token(
    request: Request,
    deps: ApiDependencies = Depends(_get_api_dependencies),
) -> None:
    headers = {name: value for name, value in request.headers.items()}
    deps.service_token_auth.require(headers)
