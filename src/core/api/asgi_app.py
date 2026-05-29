from __future__ import annotations

from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

from core.api.dependencies import ApiDependencies, build_api_dependencies
from core.api.envelope import build_error_envelope, ensure_trace_id
from core.api.handlers import (
    handle_auth_eid_start_stub,
    handle_bearer_stub,
    handle_health,
    handle_me_stub,
    handle_public_stub,
    handle_readiness,
)
from core.api.security import UnauthorizedError, UserClaims, get_current_user
from core.config import AppConfig, ConfigError, provide_app_config
from core.logging_setup import configure_logging, log_runtime_exception

_config_for_dependencies: AppConfig | None = None

PROTECTED_OPTIONS_PATHS: tuple[str, ...] = (
    "/me",
    "/auth/eid/start",
    "/oauth/authorize",
    "/oauth/authorize/complete",
    "/oauth/token",
    "/story-drafts",
    "/story-drafts/{draft_id}/submit",
    "/stories",
    "/gpt/actions/submit-story",
)


def _trace_id_from_request(request: Request) -> str:
    return ensure_trace_id(request.headers.get("x-trace-id"))


def _json_envelope(body: dict, status_code: int) -> JSONResponse:
    return JSONResponse(content=body, status_code=status_code)


@lru_cache(maxsize=1)
def _cached_dependencies() -> ApiDependencies:
    config = _config_for_dependencies or provide_app_config()
    return build_api_dependencies(config)


def get_api_dependencies() -> ApiDependencies:
    return _cached_dependencies()


def _clear_api_dependencies_cache() -> None:
    _cached_dependencies.cache_clear()


def create_app(config: AppConfig) -> FastAPI:
    global _config_for_dependencies
    _clear_api_dependencies_cache()
    _config_for_dependencies = config

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
        body, status = handle_me_stub(
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
        body, status = handle_auth_eid_start_stub(
            deps, current_user=current_user, trace_id=trace_id
        )
        return _json_envelope(body, status)

    @app.get("/auth/eideasy/callback")
    async def auth_eideasy_callback(request: Request) -> JSONResponse:
        deps = get_api_dependencies()
        trace_id = _trace_id_from_request(request)
        body, status = handle_public_stub(
            deps,
            path="/auth/eideasy/callback",
            next_epic="EPIC-IDS-EID",
            trace_id=trace_id,
        )
        return _json_envelope(body, status)

    @app.get("/auth/authentigate/callback")
    async def auth_authentigate_callback(request: Request) -> JSONResponse:
        deps = get_api_dependencies()
        trace_id = _trace_id_from_request(request)
        body, status = handle_public_stub(
            deps,
            path="/auth/authentigate/callback",
            next_epic="EPIC-IDS-EID",
            trace_id=trace_id,
        )
        return _json_envelope(body, status)

    @app.get("/auth/mock/callback")
    async def auth_mock_callback(request: Request) -> JSONResponse:
        deps = get_api_dependencies()
        trace_id = _trace_id_from_request(request)
        body, status = handle_public_stub(
            deps,
            path="/auth/mock/callback",
            next_epic="EPIC-IDS-EID",
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

    @app.post("/story-drafts")
    async def story_drafts_create(
        request: Request,
        current_user: UserClaims = Depends(get_current_user),
    ) -> JSONResponse:
        return _bearer_route(
            request,
            current_user,
            path="/story-drafts",
            method="POST",
            next_epic="EPIC-IDS-STORIES",
        )

    @app.post("/story-drafts/{draft_id}/submit")
    async def story_drafts_submit(
        request: Request,
        draft_id: str,
        current_user: UserClaims = Depends(get_current_user),
    ) -> JSONResponse:
        del draft_id
        return _bearer_route(
            request,
            current_user,
            path="/story-drafts/{draft_id}/submit",
            method="POST",
            next_epic="EPIC-IDS-STORIES",
        )

    @app.post("/stories")
    async def stories_create(
        request: Request,
        current_user: UserClaims = Depends(get_current_user),
    ) -> JSONResponse:
        return _bearer_route(
            request,
            current_user,
            path="/stories",
            method="POST",
            next_epic="EPIC-IDS-STORIES",
        )

    @app.post("/gpt/actions/submit-story")
    async def gpt_submit_story(
        request: Request,
        current_user: UserClaims = Depends(get_current_user),
    ) -> JSONResponse:
        return _bearer_route(
            request,
            current_user,
            path="/gpt/actions/submit-story",
            method="POST",
            next_epic="EPIC-IDS-STORIES",
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


_config = provide_app_config()
app = create_app(_config)
