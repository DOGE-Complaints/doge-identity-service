from __future__ import annotations

from urllib.parse import urlencode

from core.config.schema import AppConfig


def resolve_spa_login_base_url(config: AppConfig) -> str:
    origins = [
        origin.strip()
        for origin in config.cors_allowed_origins.split(",")
        if origin.strip() and origin.strip() != "*"
    ]
    if origins:
        return origins[0].rstrip("/")
    return "http://localhost:3000"


def build_spa_oauth_login_url(config: AppConfig, *, oauth_request_id: str) -> str:
    base = resolve_spa_login_base_url(config)
    query = urlencode({"oauth_request_id": oauth_request_id})
    return f"{base}/login?{query}"


def build_spa_verify_url(config: AppConfig, *, return_context: str | None) -> str:
    base = resolve_spa_login_base_url(config)
    if return_context:
        query = urlencode({"context": return_context})
        return f"{base}/verify?{query}"
    return f"{base}/verify"
