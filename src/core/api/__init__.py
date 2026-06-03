"""API layer package."""

from typing import Any

from core.api.asgi_app import get_api_dependencies
from core.api.dependencies import ApiDependencies, HandlerDependencies, build_api_dependencies

__all__ = [
    "ApiDependencies",
    "HandlerDependencies",
    "app",
    "build_api_dependencies",
    "get_api_dependencies",
]


def __getattr__(name: str) -> Any:
    if name == "app":
        from core.api.asgi_app import app as asgi_app

        return asgi_app
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
