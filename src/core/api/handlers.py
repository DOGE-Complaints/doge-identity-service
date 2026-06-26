from __future__ import annotations

import dataclasses
import json
import uuid
from collections.abc import Mapping
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

from core.api.eid_callback import EidCallbackOutcome
from core.api.envelope import build_error_envelope, build_success_envelope
from core.api.me_response import build_me_data
from core.domain.models import EIDAuditEvent, PhoneAuditEvent, ProfileConflictError
from core.phone.base import SmsErrorCode, SmsSenderError
from core.phone.e164 import normalize_to_e164, resolve_dial_prefix
from core.config.providers import resolve_config_env
from core.phone.otp_engine import create_phone_verification_session, verify_phone_code
from core.phone.sms_text import build_verification_sms_text
from core.phone.telnyx.delivery_ingest import apply_delivery_update, parse_telnyx_messaging_webhook
from core.phone.telnyx.webhook_signature import verify_telnyx_webhook_signature
from core.providers.config_spec import _env_value
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


def _sms_error_http_status(code: SmsErrorCode) -> int:
    if code in {SmsErrorCode.PROVIDER_UNAVAILABLE, SmsErrorCode.SEND_FAILED}:
        return 503
    return 400


def _phone_error_response(
    exc: SmsSenderError,
    *,
    trace_id: str,
) -> tuple[dict, int]:
    body = build_error_envelope(exc.code.value, str(exc), trace_id=trace_id)
    return body, _sms_error_http_status(exc.code)


def _log_phone_audit(
    deps: ApiDependencies,
    *,
    supabase_user_id: str | None,
    event_type: str,
    provider: str | None = None,
    success: bool,
    failure_reason: str | None = None,
    request_id: str | None = None,
) -> None:
    audit = deps.phone_audit_log_repository
    if audit is None:
        return
    audit.log_event(
        PhoneAuditEvent(
            id=str(uuid.uuid4()),
            supabase_user_id=supabase_user_id,
            event_type=event_type,
            provider=provider,
            success=success,
            failure_reason=failure_reason,
            request_id=request_id,
            created_at=datetime.now(timezone.utc),
        )
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
) -> EidCallbackOutcome:
    store = deps.verification_session_store
    profile_repo = deps.profile_repository
    registry = deps.eid_provider_registry
    if store is None or profile_repo is None or registry is None:
        return EidCallbackOutcome(
            outcome="failed",
            return_url=None,
            error_code=None,
            json_status=500,
            envelope_code="CONFIG_ERROR",
            envelope_message="EID verification services are not configured.",
        )

    session = _resolve_verification_session(store, raw_params)
    if session is None:
        return EidCallbackOutcome(
            outcome="failed",
            return_url=None,
            error_code=None,
            json_status=400,
            envelope_code="invalid_or_consumed_state",
            envelope_message="Verification session not found or already consumed.",
        )

    if session.provider != provider_name:
        return EidCallbackOutcome(
            outcome="failed",
            return_url=session.return_url,
            error_code=None,
            json_status=400,
            envelope_code="invalid_or_consumed_state",
            envelope_message="Session provider mismatch.",
        )

    if session.status == "consumed":
        return EidCallbackOutcome(
            outcome="already_verified",
            return_url=session.return_url,
            error_code=None,
            json_status=200,
        )

    if session.status in {"failed", "expired"}:
        return EidCallbackOutcome(
            outcome="failed",
            return_url=session.return_url,
            error_code=None,
            json_status=400,
            envelope_code="invalid_or_consumed_state",
            envelope_message="Verification session is no longer active.",
        )

    now = datetime.now(timezone.utc)
    if session.status != "started":
        return EidCallbackOutcome(
            outcome="failed",
            return_url=session.return_url,
            error_code=None,
            json_status=400,
            envelope_code="invalid_or_consumed_state",
            envelope_message="Verification session is not in started state.",
        )

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
        return EidCallbackOutcome(
            outcome="failed",
            return_url=session.return_url,
            error_code=None,
            json_status=400,
            envelope_code="eid_session_expired",
            envelope_message="Verification session has expired.",
        )

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
        return EidCallbackOutcome(
            outcome="failed",
            return_url=session.return_url,
            error_code=exc.code,
            json_status=400,
            envelope_code="eid_verification_failed",
            envelope_message="Provider callback processing failed.",
        )
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
        return EidCallbackOutcome(
            outcome="failed",
            return_url=session.return_url,
            error_code=EidErrorCode.UNKNOWN,
            json_status=400,
            envelope_code="eid_verification_failed",
            envelope_message="Provider callback processing failed.",
        )

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
        return EidCallbackOutcome(
            outcome="failed",
            return_url=session.return_url,
            error_code=None,
            json_status=409,
            envelope_code="profile_conflict",
            envelope_message=str(exc),
        )

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

    return EidCallbackOutcome(
        outcome="verified",
        return_url=session.return_url,
        error_code=None,
        json_status=200,
    )


def handle_phone_request(
    deps: ApiDependencies,
    *,
    current_user: UserClaims,
    phone: str,
    trace_id: str,
) -> tuple[dict, int]:
    registry = deps.sms_sender_registry
    session_store = deps.phone_verification_session_store
    if registry is None or session_store is None:
        body = build_error_envelope(
            "CONFIG_ERROR",
            "Phone verification services are not configured.",
            trace_id=trace_id,
        )
        return body, 500

    user_id = current_user.supabase_user_id
    now = datetime.now(timezone.utc)

    try:
        e164 = normalize_to_e164(phone)
        dial_prefix = resolve_dial_prefix(e164, deps.config.phone_allowed_dial_prefixes)

        active = session_store.get_active_by_user(user_id, now=now)
        if active is not None:
            # Domain OTP cooldown (400 RATE_LIMITED) — separate from HTTP 429 rate_limit_exceeded
            # enforced in rate_limit_dependency before this handler (SEC-01).
            cooldown_end = active.created_at + timedelta(
                seconds=deps.config.phone_resend_cooldown_s
            )
            if now < cooldown_end:
                _log_phone_audit(
                    deps,
                    supabase_user_id=user_id,
                    event_type="phone_verification_request_failed",
                    success=False,
                    failure_reason=SmsErrorCode.RATE_LIMITED.value,
                    request_id=trace_id,
                )
                raise SmsSenderError(
                    "phone verification resend is rate limited",
                    code=SmsErrorCode.RATE_LIMITED,
                )

        sender = registry.get_active(deps.config)
        session, plaintext_code = create_phone_verification_session(
            store=session_store,
            config=deps.config,
            supabase_user_id=user_id,
            e164=e164,
            dial_prefix=dial_prefix,
            provider=sender.provider_name,
            now=now,
        )
        send_result = sender.send(to_e164=e164, text=build_verification_sms_text(plaintext_code))
        if send_result.provider_message_id:
            session = dataclasses.replace(session, provider_message_id=send_result.provider_message_id)
            session_store.replace(session)
    except SmsSenderError as exc:
        if exc.code is not SmsErrorCode.RATE_LIMITED:
            _log_phone_audit(
                deps,
                supabase_user_id=user_id,
                event_type="phone_verification_request_failed",
                success=False,
                failure_reason=exc.code.value,
                request_id=trace_id,
            )
        return _phone_error_response(exc, trace_id=trace_id)

    _log_phone_audit(
        deps,
        supabase_user_id=user_id,
        event_type="phone_verification_requested",
        provider=sender.provider_name,
        success=True,
        request_id=trace_id,
    )
    payload = {
        "sent": True,
        "expires_at": _format_utc_iso(session.expires_at),
    }
    return build_success_envelope(payload), 200


def handle_phone_confirm(
    deps: ApiDependencies,
    *,
    current_user: UserClaims,
    phone: str,
    code: str,
    trace_id: str,
) -> tuple[dict, int]:
    session_store = deps.phone_verification_session_store
    profile_repo = deps.profile_repository
    if session_store is None or profile_repo is None:
        body = build_error_envelope(
            "CONFIG_ERROR",
            "Phone verification services are not configured.",
            trace_id=trace_id,
        )
        return body, 500

    user_id = current_user.supabase_user_id
    now = datetime.now(timezone.utc)
    audit_provider: str | None = None

    try:
        e164 = normalize_to_e164(phone)
        session = session_store.get_latest_for_confirm(user_id)
        if session is None:
            raise SmsSenderError(
                "no active phone verification session",
                code=SmsErrorCode.UNKNOWN,
            )
        if session.status == "failed":
            raise SmsSenderError(
                "too many verification attempts",
                code=SmsErrorCode.TOO_MANY_ATTEMPTS,
            )

        audit_provider = session.provider
        expected_phone_hash = hash_secret(e164, key=deps.config.eid_secret or "")
        if session.phone_hash != expected_phone_hash:
            raise SmsSenderError(
                "phone number does not match verification session",
                code=SmsErrorCode.UNKNOWN,
            )

        verification = verify_phone_code(
            store=session_store,
            config=deps.config,
            session_id=session.id,
            submitted_code=code,
            e164=e164,
            now=now,
        )
    except SmsSenderError as exc:
        _log_phone_audit(
            deps,
            supabase_user_id=user_id,
            event_type="phone_verification_confirm_failed",
            provider=audit_provider,
            success=False,
            failure_reason=exc.code.value,
            request_id=trace_id,
        )
        return _phone_error_response(exc, trace_id=trace_id)

    try:
        profile_repo.attach_phone_verification(
            user_id,
            provider=verification.provider,
            dial_prefix=verification.dial_prefix,
            verified_phone_hash=verification.subject_hash,
            verified_at=verification.verified_at,
            one_account_per_number=deps.config.phone_one_account_per_number,
        )
    except ProfileConflictError as exc:
        _log_phone_audit(
            deps,
            supabase_user_id=user_id,
            event_type="phone_verification_confirm_failed",
            provider=verification.provider,
            success=False,
            failure_reason="profile_conflict",
            request_id=trace_id,
        )
        body = build_error_envelope("profile_conflict", str(exc), trace_id=trace_id)
        return body, 409

    _log_phone_audit(
        deps,
        supabase_user_id=user_id,
        event_type="phone_verification_confirmed",
        provider=verification.provider,
        success=True,
        request_id=trace_id,
    )
    return build_success_envelope({"status": "verified"}), 200


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


def handle_telnyx_messaging_webhook(
    deps: ApiDependencies,
    *,
    raw_body: bytes,
    headers: Mapping[str, str],
    trace_id: str,
) -> tuple[dict | None, int]:
    webhook_public_key = _env_value(resolve_config_env(), "TELNYX_WEBHOOK_PUBLIC_KEY")
    if not webhook_public_key:
        body = build_error_envelope(
            "CONFIG_ERROR",
            "TELNYX_WEBHOOK_PUBLIC_KEY is not configured.",
            trace_id=trace_id,
        )
        return body, 503

    if not verify_telnyx_webhook_signature(
        raw_body=raw_body,
        headers=headers,
        public_key=webhook_public_key,
    ):
        _log_phone_audit(
            deps,
            supabase_user_id=None,
            event_type="telnyx_delivery_status_updated",
            provider="telnyx",
            success=False,
            failure_reason="invalid_signature",
            request_id=trace_id,
        )
        body = build_error_envelope(
            "UNAUTHORIZED",
            "invalid telnyx webhook signature",
            trace_id=trace_id,
        )
        return body, 401

    session_store = deps.phone_verification_session_store
    if session_store is None:
        body = build_error_envelope(
            "CONFIG_ERROR",
            "phone verification session store is not configured.",
            trace_id=trace_id,
        )
        return body, 500

    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        _log_phone_audit(
            deps,
            supabase_user_id=None,
            event_type="telnyx_delivery_status_updated",
            provider="telnyx",
            success=False,
            failure_reason="invalid_json",
            request_id=trace_id,
        )
        body = build_error_envelope(
            "BAD_REQUEST",
            "invalid telnyx webhook json",
            trace_id=trace_id,
        )
        return body, 400

    try:
        event = parse_telnyx_messaging_webhook(payload)
    except ValueError as exc:
        _log_phone_audit(
            deps,
            supabase_user_id=None,
            event_type="telnyx_delivery_status_updated",
            provider="telnyx",
            success=False,
            failure_reason="invalid_payload",
            request_id=trace_id,
        )
        body = build_error_envelope(
            "BAD_REQUEST",
            str(exc),
            trace_id=trace_id,
        )
        return body, 400

    result = apply_delivery_update(
        session_store,
        provider_message_id=event.provider_message_id,
        new_status=event.delivery_status,
        occurred_at=event.occurred_at,
    )

    user_id = result.session.supabase_user_id if result.session is not None else None
    _log_phone_audit(
        deps,
        supabase_user_id=user_id,
        event_type="telnyx_delivery_status_updated",
        provider="telnyx",
        success=result.outcome in {"updated", "noop", "not_found"},
        failure_reason=None if result.outcome != "not_found" else "session_not_found",
        request_id=trace_id,
    )
    return None, 204


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
