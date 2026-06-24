from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.api.dependencies import ApiDependencies


def handle_oauth_introspect(
    deps: ApiDependencies,
    *,
    token: str,
) -> tuple[dict[str, object], int]:
    """RFC 7662-style introspection: always HTTP 200; inactive tokens return active=false."""
    oauth_token_service = deps.oauth_token_service
    profile_repository = deps.profile_repository
    if not token.strip() or oauth_token_service is None:
        return {"active": False}, 200
    try:
        claims = oauth_token_service.validate_access_token(token)
    except ValueError:
        return {"active": False}, 200
    phone_verified = False
    if profile_repository is not None:
        profile = profile_repository.get_by_supabase_user_id(claims.sub)
        if profile is not None:
            phone_verified = profile.phone_verified
    return {
        "active": True,
        "sub": claims.sub,
        "phone_verified": phone_verified,
    }, 200
