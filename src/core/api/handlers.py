from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from core.api.envelope import build_error_envelope, build_success_envelope
from core.api.me_response import build_me_data
from core.domain.models import EIDAuditEvent, ProfileConflictError
from core.security.hashing import hash_secret
from core.security.return_url import (
    InvalidReturnUrlError,
    parse_allowed_return_urls,
    validate_return_url,
)

from core.domain.contracts import VerificationSessionStore
from core.providers.base import EIDProviderError, EidErrorCode

if TYPE_CHECKING:
    from core.api.dependencies import ApiDependencies
    from core.api.security import UserClaims
    from core.domain.models import VerificationSession


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


def _format_utc_iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _log_eid_audit(
    deps: ApiDependencies,
    *,
    supabase_user_id: str | None,
    event_type: str,
    provider: str | None = None,
    method: str | None = None,
    success: bool,
    failure_reason: str | None = None,
    request_id: str | None = None,
) -> None:
    audit = deps.eid_audit_log_repository
    if audit is None:
        return
    audit.log_event(
        EIDAuditEvent(
            id=str(uuid.uuid4()),
            supabase_user_id=supabase_user_id,
            event_type=event_type,
            provider=provider,
            method=method,
            success=success,
            failure_reason=failure_reason,
            request_id=request_id,
            ip_hash=None,
            user_agent_hash=None,
            created_at=datetime.now(timezone.utc),
        )
    )


def handle_auth_eid_start(
    deps: ApiDependencies,
    *,
    current_user: UserClaims,
    trace_id: str,
    return_url: str | None = None,
    return_context: str | None = None,
    requested_action: str | None = None,
) -> tuple[dict, int]:
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

    if return_url is None or not return_url.strip():
        body = build_error_envelope(
            InvalidReturnUrlError.code,
            "return_url is required",
            trace_id=trace_id,
        )
        return body, 400

    registry = deps.eid_provider_registry
    if registry is None:
        body = build_error_envelope(
            "CONFIG_ERROR",
            "EID provider registry is not configured.",
            trace_id=trace_id,
        )
        return body, 500

    provider = registry.get_active(deps.config)
    result = provider.start_flow(
        supabase_user_id=current_user.supabase_user_id,
        return_url=return_url,
        return_context=return_context,
        requested_action=requested_action,
    )

    _log_eid_audit(
        deps,
        supabase_user_id=current_user.supabase_user_id,
        event_type="eid_verification_started",
        provider=provider.provider_name,
        success=True,
        request_id=trace_id,
    )

    payload = {
        "redirect_url": result.redirect_url,
        "expires_at": _format_utc_iso(result.expires_at),
        "session_id": result.session_id,
    }
    return build_success_envelope(payload), 200


def _resolve_verification_session(
    store: VerificationSessionStore,
    raw_params: dict[str, str],
) -> VerificationSession | None:
    state = raw_params.get("state")
    if state:
        return store.get_by_state(state)
    session_id = raw_params.get("session_id")
    if session_id:
        return store.get_by_id(session_id)
    return None


def handle_auth_eid_callback(
    deps: ApiDependencies,
    *,
    provider_name: str,
    raw_params: dict[str, str],
    trace_id: str,
) -> tuple[dict, int]:
    store = deps.verification_session_store
    profile_repo = deps.profile_repository
    registry = deps.eid_provider_registry
    if store is None or profile_repo is None or registry is None:
        body = build_error_envelope(
            "CONFIG_ERROR",
            "EID verification services are not configured.",
            trace_id=trace_id,
        )
        return body, 500

    session = _resolve_verification_session(store, raw_params)
    if session is None:
        body = build_error_envelope(
            "invalid_or_consumed_state",
            "Verification session not found or already consumed.",
            trace_id=trace_id,
        )
        return body, 400

    if session.provider != provider_name:
        body = build_error_envelope(
            "invalid_or_consumed_state",
            "Session provider mismatch.",
            trace_id=trace_id,
        )
        return body, 400

    if session.status == "consumed":
        return build_success_envelope({"status": "already_consumed"}), 200

    if session.status in {"failed", "expired"}:
        body = build_error_envelope(
            "invalid_or_consumed_state",
            "Verification session is no longer active.",
            trace_id=trace_id,
        )
        return body, 400

    now = datetime.now(timezone.utc)
    if session.status != "started":
        body = build_error_envelope(
            "invalid_or_consumed_state",
            "Verification session is not in started state.",
            trace_id=trace_id,
        )
        return body, 400

    if session.expires_at < now:
        store.mark_failed(session.id, "session_expired")
        _log_eid_audit(
            deps,
            supabase_user_id=session.supabase_user_id,
            event_type="eid_verification_failed",
            provider=provider_name,
            success=False,
            failure_reason="session_expired",
            request_id=trace_id,
        )
        body = build_error_envelope(
            "eid_session_expired",
            "Verification session has expired.",
            trace_id=trace_id,
        )
        return body, 400

    provider = registry.get(provider_name)
    try:
        verification = provider.handle_callback(raw_params=raw_params)
    except EIDProviderError as exc:
        reason = exc.code.value
        store.mark_failed(session.id, reason)
        _log_eid_audit(
            deps,
            supabase_user_id=session.supabase_user_id,
            event_type="eid_verification_failed",
            provider=provider_name,
            success=False,
            failure_reason=reason,
            request_id=trace_id,
        )
        body = build_error_envelope(
            "eid_verification_failed",
            "Provider callback processing failed.",
            trace_id=trace_id,
        )
        body["error"]["eid_error_code"] = reason
        return body, 400
    except Exception:
        reason = EidErrorCode.UNKNOWN.value
        store.mark_failed(session.id, reason)
        _log_eid_audit(
            deps,
            supabase_user_id=session.supabase_user_id,
            event_type="eid_verification_failed",
            provider=provider_name,
            success=False,
            failure_reason=reason,
            request_id=trace_id,
        )
        body = build_error_envelope(
            "eid_verification_failed",
            "Provider callback processing failed.",
            trace_id=trace_id,
        )
        return body, 400

    verified_person_hash = hash_secret(
        f"{verification.country}:{verification.subject_hash}",
        key=deps.config.eid_secret or "",
    )

    try:
        profile_repo.attach_eid_verification(
            session.supabase_user_id,
            provider=verification.provider,
            country=verification.country,
            method=verification.login_method,
            verified_person_hash=verified_person_hash,
            verified_at=verification.verified_at,
        )
    except ProfileConflictError as exc:
        store.mark_failed(session.id, "profile_conflict")
        _log_eid_audit(
            deps,
            supabase_user_id=session.supabase_user_id,
            event_type="eid_verification_failed",
            provider=provider_name,
            method=verification.login_method,
            success=False,
            failure_reason="profile_conflict",
            request_id=trace_id,
        )
        body = build_error_envelope(
            "profile_conflict",
            str(exc),
            trace_id=trace_id,
        )
        return body, 409

    store.mark_consumed(session.id)
    _log_eid_audit(
        deps,
        supabase_user_id=session.supabase_user_id,
        event_type="eid_verification_success",
        provider=verification.provider,
        method=verification.login_method,
        success=True,
        request_id=trace_id,
    )

    payload: dict[str, object] = {"status": "verified"}
    if session.return_url:
        payload["return_url"] = session.return_url
    return build_success_envelope(payload), 200


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
