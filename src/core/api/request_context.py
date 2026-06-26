"""HTTP request context helpers (client IP, User-Agent)."""

from __future__ import annotations

from fastapi import Request


def client_ip(request: Request, *, trusted_proxy_count: int) -> str:
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


def user_agent(request: Request) -> str | None:
    value = request.headers.get("user-agent")
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None
