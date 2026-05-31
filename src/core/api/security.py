from __future__ import annotations

from typing import Mapping

from fastapi import Depends, Request

from core.api.dependencies import ApiDependencies
from core.domain.contracts import BearerTokenAuth, SupabaseJwtValidator
from core.domain.models import JwtValidationError, UserClaims

STUB_SUPABASE_USER_ID = "00000000-0000-0000-0000-000000000000"


class UnauthorizedError(Exception):
    code: str = "AUTHENTICATION_REQUIRED"

    def __init__(self, message: str = "Authentication required") -> None:
        self.message = message
        super().__init__(message)


class StubBearerTokenAuth:
    def validate(self, headers: Mapping[str, str]) -> UserClaims:
        token = _extract_bearer_token(headers)
        if token is None:
            raise UnauthorizedError("Bearer token required")
        return UserClaims(
            supabase_user_id=STUB_SUPABASE_USER_ID,
            email=None,
            role="authenticated",
        )


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
