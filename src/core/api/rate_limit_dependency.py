from __future__ import annotations

from fastapi import Depends, Request

from core.api.security import UserClaims, get_current_user
from core.security.rate_limit import RateLimitExceeded
from core.security.rate_limit_config import (
    ROUTE_AUTH_CALLBACK,
    ROUTE_AUTH_EID_START,
    ROUTE_AUTH_PHONE_REQUEST,
    rate_limit_rules_for_config,
)


from core.api.request_context import client_ip
def _enforce_rate_limit(*, request: Request, route_key: str, limit_key: str) -> None:
    from core.api.asgi_app import get_api_dependencies

    deps = get_api_dependencies()
    rule = rate_limit_rules_for_config(deps.config)[route_key]
    result = deps.rate_limiter.check(limit_key, rule)
    if not result.allowed:
        raise RateLimitExceeded(result.retry_after_s)


async def require_eid_start_rate_limit(
    request: Request,
    current_user: UserClaims = Depends(get_current_user),
) -> None:
    _enforce_rate_limit(
        request=request,
        route_key=ROUTE_AUTH_EID_START,
        limit_key=f"user:{current_user.supabase_user_id}",
    )


async def require_callback_rate_limit(request: Request) -> None:
    from core.api.asgi_app import get_api_dependencies

    deps = get_api_dependencies()
    _enforce_rate_limit(
        request=request,
        route_key=ROUTE_AUTH_CALLBACK,
        limit_key=f"ip:{client_ip(request, trusted_proxy_count=deps.config.rate_limit_trusted_proxy_count)}",
    )


async def require_phone_request_rate_limit(
    request: Request,
    current_user: UserClaims = Depends(get_current_user),
) -> None:
    _enforce_rate_limit(
        request=request,
        route_key=ROUTE_AUTH_PHONE_REQUEST,
        limit_key=f"user:{current_user.supabase_user_id}",
    )
