from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from core.config.schema import AppConfig


class RateLimitScope(str, Enum):
    USER = "user"
    IP = "ip"


@dataclass(frozen=True)
class RateLimitRule:
    requests: int
    window_s: int
    per: RateLimitScope


ROUTE_AUTH_EID_START = "POST /auth/eid/start"
ROUTE_AUTH_CALLBACK = "GET /auth/{provider}/callback"
ROUTE_AUTH_PHONE_REQUEST = "POST /auth/phone/request"


def rate_limit_rules_for_config(config: AppConfig) -> dict[str, RateLimitRule]:
    return {
        ROUTE_AUTH_EID_START: RateLimitRule(
            requests=config.rate_limit_eid_start_requests,
            window_s=config.rate_limit_eid_start_window_s,
            per=RateLimitScope.USER,
        ),
        ROUTE_AUTH_CALLBACK: RateLimitRule(
            requests=config.rate_limit_callback_requests,
            window_s=config.rate_limit_callback_window_s,
            per=RateLimitScope.IP,
        ),
        ROUTE_AUTH_PHONE_REQUEST: RateLimitRule(
            requests=config.rate_limit_phone_request_requests,
            window_s=config.rate_limit_phone_request_window_s,
            per=RateLimitScope.USER,
        ),
    }
