from __future__ import annotations

from typing import TYPE_CHECKING

from core.api.envelope import build_error_envelope, build_success_envelope
from core.api.me_response import build_me_data
from core.security.return_url import (
    InvalidReturnUrlError,
    parse_allowed_return_urls,
    validate_return_url,
)

if TYPE_CHECKING:
    from core.api.dependencies import ApiDependencies
    from core.api.security import UserClaims


def handle_health(deps: ApiDependencies, *, trace_id: str) -> tuple[dict, int]:
    del deps
    return build_success_envelope({"status": "ok", "trace_id": trace_id}), 200


def handle_readiness(deps: ApiDependencies, *, trace_id: str) -> tuple[dict, int]:
    ready = deps.db_ready
    payload = {
        "status": "ready" if ready else "degraded",
        "db_backend": deps.db_backend,
        "db_ready": ready,
        "db_checks": deps.db_checks,
        "trace_id": trace_id,
    }
    return build_success_envelope(payload), 200 if ready else 503


def _not_implemented(
    message: str,
    *,
    trace_id: str,
    next_epic: str,
) -> tuple[dict, int]:
    body = build_error_envelope("NOT_IMPLEMENTED", message, trace_id=trace_id)
    body["error"]["next_epic"] = next_epic
    return body, 501


def handle_me(
    deps: ApiDependencies,
    *,
    current_user: UserClaims,
    trace_id: str,
) -> tuple[dict, int]:
    """GET /me — profile + eid_verified + role from JWT.

    Missing profile (t01): 200, no DB write; ``eid_verified=false``, profile fields null.
    """
    repo = deps.profile_repository
    if repo is None:
        body = build_error_envelope(
            "CONFIG_ERROR",
            "Profile repository is not configured.",
            trace_id=trace_id,
        )
        return body, 500

    profile = repo.get_by_supabase_user_id(current_user.supabase_user_id)
    payload = build_me_data(profile, current_user)
    return build_success_envelope(payload), 200


def handle_auth_eid_start_stub(
    deps: ApiDependencies,
    *,
    current_user: UserClaims,
    trace_id: str,
    return_url: str | None = None,
) -> tuple[dict, int]:
    del current_user
    allowed = parse_allowed_return_urls(deps.config.allowed_return_urls)
    try:
        validate_return_url(return_url, allowed)
    except InvalidReturnUrlError as exc:
        body = build_error_envelope(
            InvalidReturnUrlError.code,
            str(exc),
            trace_id=trace_id,
        )
        return body, 400
    return _not_implemented(
        "POST /auth/eid/start implemented in EPIC-IDS-EID",
        trace_id=trace_id,
        next_epic="EPIC-IDS-EID",
    )


def handle_public_stub(
    deps: ApiDependencies,
    *,
    path: str,
    next_epic: str,
    trace_id: str,
) -> tuple[dict, int]:
    del deps
    return _not_implemented(
        f"{path} not implemented yet",
        trace_id=trace_id,
        next_epic=next_epic,
    )


def handle_bearer_stub(
    deps: ApiDependencies,
    *,
    path: str,
    method: str,
    current_user: UserClaims,
    trace_id: str,
    next_epic: str,
) -> tuple[dict, int]:
    del deps, current_user
    return _not_implemented(
        f"{method} {path} not implemented yet",
        trace_id=trace_id,
        next_epic=next_epic,
    )
