from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse, Response

from core.api.dependencies import ApiDependencies, build_api_dependencies
from core.api.eid_callback import (
    EidCallbackOutcome,
    append_eid_redirect_query,
    build_callback_json_envelope,
    has_safe_redirect_target,
)
from core.api.envelope import build_error_envelope, ensure_trace_id
from core.api.handlers import (
    handle_auth_eid_callback,
    handle_auth_eid_start,
    handle_bearer_stub,
    handle_health,
    handle_me,
    handle_phone_confirm,
    handle_phone_request,
    handle_readiness,
)
from core.api.security import UnauthorizedError, UserClaims, get_current_user
from core.config import AppConfig, ConfigError, provide_app_config
from core.logging_setup import configure_logging, log_runtime_exception

PROTECTED_OPTIONS_PATHS: tuple[str, ...] = (
    "/me",
    "/auth/eid/start",
    "/auth/phone/request",
    "/auth/phone/confirm",
    "/oauth/authorize",
    "/oauth/authorize/complete",
    "/oauth/token",
)


def _trace_id_from_request(request: Request) -> str:
    return ensure_trace_id(request.headers.get("x-trace-id"))


async def _phone_payload_from_request(request: Request) -> dict[str, str]:
    payload: dict[str, str] = {"phone": "", "code": ""}
    content_type = request.headers.get("content-type", "")
    if content_type.startswith("application/json"):
        try:
            body = await request.json()
        except Exception:
            body = None
        if isinstance(body, dict):
            phone = body.get("phone")
            if isinstance(phone, str):
                payload["phone"] = phone
            code = body.get("code")
            if isinstance(code, str):
                payload["code"] = code
    return payload


async def _eid_start_payload_from_request(request: Request) -> dict[str, str | None]:
    payload: dict[str, str | None] = {
        "return_url": None,
        "return_context": None,
        "requested_action": None,
    }
    content_type = request.headers.get("content-type", "")
    if content_type.startswith("application/json"):
        try:
            body = await request.json()
        except Exception:
            body = None
        if isinstance(body, dict):
            for key in payload:
                value = body.get(key)
                if isinstance(value, str):
                    payload[key] = value
    if payload["return_url"] is None:
        query_value = request.query_params.get("return_url")
        if isinstance(query_value, str):
            payload["return_url"] = query_value
    return payload


def _query_params_as_strings(request: Request) -> dict[str, str]:
    return {key: value for key, value in request.query_params.items()}


def _json_envelope(body: dict, status_code: int) -> JSONResponse:
    return JSONResponse(content=body, status_code=status_code)


def _wants_json_response(request: Request) -> bool:
    accept = request.headers.get("accept", "")
    return "application/json" in accept


def _render_eid_callback_outcome(
    request: Request,
    outcome: EidCallbackOutcome,
    *,
    trace_id: str,
) -> Response:
    if _wants_json_response(request):
        body, status = build_callback_json_envelope(outcome, trace_id=trace_id)
        return _json_envelope(body, status)

    if has_safe_redirect_target(outcome):
        location = append_eid_redirect_query(outcome, outcome.return_url or "")
        return RedirectResponse(url=location, status_code=303)

    body, status = build_callback_json_envelope(outcome, trace_id=trace_id)
    return _json_envelope(body, status)


@lru_cache(maxsize=1)
def _cached_dependencies() -> ApiDependencies:
    return build_api_dependencies()


def get_api_dependencies() -> ApiDependencies:
    return _cached_dependencies()


def _clear_api_dependencies_cache() -> None:
    _cached_dependencies.cache_clear()


def create_app(config: AppConfig) -> FastAPI:
    """Build FastAPI app; CORS uses ``config``, DI reads env via ``provide_app_config()``.

    NOTE: ``config`` is used only for ``CORSMiddleware`` ``allow_origins``.
    The DI container loads its own config through ``build_api_dependencies()``
    -> ``provide_app_config()`` from ``os.environ``. Mirror env in tests with
    ``monkeypatch.setenv`` (see ``tests/conftest.py``).
    """
    _clear_api_dependencies_cache()

    app = FastAPI(
        title="doge-identity-service",
        version="0.1.0",
        lifespan=_lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in config.cors_allowed_origins.split(",") if o.strip()],
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["authorization", "content-type", "x-trace-id"],
    )
    _register_exception_handlers(app)
    _register_middleware(app)
    _register_routes(app)
    return app


@asynccontextmanager
async def _lifespan(app: FastAPI):
    deps = get_api_dependencies()
    configure_logging(
        deps.config.log_level,
        log_format=deps.config.log_format,
    )
    logging.getLogger(__name__).info(
        "startup.persistence_backend backend=%s db_ready=%s db_checks=%s",
        deps.db_backend,
        deps.db_ready,
        dict(deps.db_checks),
    )
    yield


def _register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(UnauthorizedError)
    async def unauthorized_handler(
        request: Request, exc: UnauthorizedError
    ) -> JSONResponse:
        trace_id = _trace_id_from_request(request)
        body = build_error_envelope(
            exc.code,
            exc.message,
            trace_id=trace_id,
        )
        return _json_envelope(body, 401)

    @app.exception_handler(ConfigError)
    async def config_error_handler(request: Request, exc: ConfigError) -> JSONResponse:
        trace_id = _trace_id_from_request(request)
        body = build_error_envelope("CONFIG_ERROR", str(exc), trace_id=trace_id)
        return _json_envelope(body, 500)


def _register_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def runtime_exception_diagnostics(request: Request, call_next: Any) -> Response:
        trace_id = _trace_id_from_request(request)
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            log_runtime_exception(
                exc,
                trace_id=trace_id,
                path=request.url.path,
            )
            body = build_error_envelope(
                "INTERNAL_ERROR",
                "Unexpected internal error.",
                trace_id=trace_id,
            )
            return _json_envelope(body, 500)


def _register_routes(app: FastAPI) -> None:
    @app.get("/health")
    async def health(request: Request) -> JSONResponse:
        deps = get_api_dependencies()
        trace_id = _trace_id_from_request(request)
        body, status = handle_health(deps, trace_id=trace_id)
        return _json_envelope(body, status)

    @app.get("/ready")
    async def ready(request: Request) -> JSONResponse:
        deps = get_api_dependencies()
        trace_id = _trace_id_from_request(request)
        body, status = handle_readiness(deps, trace_id=trace_id)
        return _json_envelope(body, status)

    @app.get("/me")
    async def me(
        request: Request,
        current_user: UserClaims = Depends(get_current_user),
    ) -> JSONResponse:
        deps = get_api_dependencies()
        trace_id = _trace_id_from_request(request)
        body, status = handle_me(
            deps, current_user=current_user, trace_id=trace_id
        )
        return _json_envelope(body, status)

    @app.post("/auth/eid/start")
    async def auth_eid_start(
        request: Request,
        current_user: UserClaims = Depends(get_current_user),
    ) -> JSONResponse:
        deps = get_api_dependencies()
        trace_id = _trace_id_from_request(request)
        start_payload = await _eid_start_payload_from_request(request)
        body, status = handle_auth_eid_start(
            deps,
            current_user=current_user,
            trace_id=trace_id,
            return_url=start_payload["return_url"],
            return_context=start_payload["return_context"],
            requested_action=start_payload["requested_action"],
        )
        return _json_envelope(body, status)

    @app.get("/auth/{provider}/callback")
    async def auth_eid_callback(request: Request, provider: str) -> Response:
        deps = get_api_dependencies()
        trace_id = _trace_id_from_request(request)
        registry = deps.eid_provider_registry
        if registry is None:
            body = build_error_envelope(
                "CONFIG_ERROR",
                "EID provider registry is not configured.",
                trace_id=trace_id,
            )
            return _json_envelope(body, 500)
        registry.get(provider)
        outcome = handle_auth_eid_callback(
            deps,
            provider_name=provider,
            raw_params=_query_params_as_strings(request),
            trace_id=trace_id,
        )
        return _render_eid_callback_outcome(request, outcome, trace_id=trace_id)

    @app.post("/auth/phone/request")
    async def auth_phone_request(
        request: Request,
        current_user: UserClaims = Depends(get_current_user),
    ) -> JSONResponse:
        deps = get_api_dependencies()
        trace_id = _trace_id_from_request(request)
        phone_payload = await _phone_payload_from_request(request)
        body, status = handle_phone_request(
            deps,
            current_user=current_user,
            phone=phone_payload["phone"],
            trace_id=trace_id,
        )
        return _json_envelope(body, status)

    @app.post("/auth/phone/confirm")
    async def auth_phone_confirm(
        request: Request,
        current_user: UserClaims = Depends(get_current_user),
    ) -> JSONResponse:
        deps = get_api_dependencies()
        trace_id = _trace_id_from_request(request)
        phone_payload = await _phone_payload_from_request(request)
        body, status = handle_phone_confirm(
            deps,
            current_user=current_user,
            phone=phone_payload["phone"],
            code=phone_payload["code"],
            trace_id=trace_id,
        )
        return _json_envelope(body, status)

    @app.get("/oauth/authorize")
    async def oauth_authorize(
        request: Request,
        current_user: UserClaims = Depends(get_current_user),
    ) -> JSONResponse:
        return _bearer_route(
            request,
            current_user,
            path="/oauth/authorize",
            method="GET",
            next_epic="EPIC-IDS-OAUTH",
        )

    @app.post("/oauth/authorize/complete")
    async def oauth_authorize_complete(
        request: Request,
        current_user: UserClaims = Depends(get_current_user),
    ) -> JSONResponse:
        return _bearer_route(
            request,
            current_user,
            path="/oauth/authorize/complete",
            method="POST",
            next_epic="EPIC-IDS-OAUTH",
        )

    @app.post("/oauth/token")
    async def oauth_token(
        request: Request,
        current_user: UserClaims = Depends(get_current_user),
    ) -> JSONResponse:
        return _bearer_route(
            request,
            current_user,
            path="/oauth/token",
            method="POST",
            next_epic="EPIC-IDS-OAUTH",
        )

    for options_path in PROTECTED_OPTIONS_PATHS:
        app.add_api_route(
            options_path,
            _options_handler,
            methods=["OPTIONS"],
            include_in_schema=False,
        )


async def _options_handler() -> Response:
    return Response(status_code=200)


def _bearer_route(
    request: Request,
    current_user: UserClaims,
    *,
    path: str,
    method: str,
    next_epic: str,
) -> JSONResponse:
    deps = get_api_dependencies()
    trace_id = _trace_id_from_request(request)
    body, status = handle_bearer_stub(
        deps,
        path=path,
        method=method,
        current_user=current_user,
        trace_id=trace_id,
        next_epic=next_epic,
    )
    return _json_envelope(body, status)


@lru_cache(maxsize=1)
def _default_production_app() -> FastAPI:
    """Uvicorn entry (`core.api.asgi_app:app`); evaluated on first access, not at import."""
    return create_app(provide_app_config())


def __getattr__(name: str) -> FastAPI:
    if name == "app":
        return _default_production_app()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
