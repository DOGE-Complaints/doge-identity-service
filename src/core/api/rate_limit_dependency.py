from __future__ import annotations

from fastapi import Depends, Request

from core.api.security import UserClaims, get_current_user
from core.security.rate_limit import RateLimitExceeded
from core.security.rate_limit_config import (
    ROUTE_AUTH_CALLBACK,
    ROUTE_AUTH_EID_START,
    rate_limit_rules_for_config,
)


def _client_ip(request: Request) -> str:
    from core.api.asgi_app import get_api_dependencies

    trusted_proxy_count = get_api_dependencies().config.rate_limit_trusted_proxy_count
    if trusted_proxy_count > 0:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            hops = [hop.strip() for hop in forwarded.split(",") if hop.strip()]
            if hops:
                idx = len(hops) - trusted_proxy_count - 1
                if idx >= 0:
                    return hops[idx]
    if request.client is not None:
        return request.client.host
    return "unknown"


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
    _enforce_rate_limit(
        request=request,
        route_key=ROUTE_AUTH_CALLBACK,
        limit_key=f"ip:{_client_ip(request)}",
    )
