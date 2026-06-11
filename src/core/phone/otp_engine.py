from __future__ import annotations

import hmac
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from core.config.schema import AppConfig
from core.domain.contracts import PhoneVerificationSessionStore
from core.domain.models import PhoneVerificationResult, PhoneVerificationSession
from core.phone.base import SmsErrorCode, SmsSenderError
from core.security.hashing import hash_secret


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _hashing_key(config: AppConfig) -> str:
    return config.eid_secret or ""


def _generate_otp_code(length: int) -> str:
    return "".join(secrets.choice("0123456789") for _ in range(length))


def _code_matches(*, submitted_code: str, code_hash: str, key: str) -> bool:
    expected = hash_secret(submitted_code, key=key)
    return hmac.compare_digest(expected, code_hash)


def create_phone_verification_session(
    *,
    store: PhoneVerificationSessionStore,
    config: AppConfig,
    supabase_user_id: str,
    e164: str,
    dial_prefix: str,
    provider: str,
    now: datetime | None = None,
) -> tuple[PhoneVerificationSession, str]:
    current = now or _utcnow()
    key = _hashing_key(config)

    active = store.get_active_by_user(supabase_user_id, now=current)
    if active is not None:
        store.mark_failed(active.id, "superseded")

    plaintext_code = _generate_otp_code(config.phone_code_length)
    session = PhoneVerificationSession(
        id=str(uuid.uuid4()),
        supabase_user_id=supabase_user_id,
        phone_hash=hash_secret(e164, key=key),
        dial_prefix=dial_prefix,
        code_hash=hash_secret(plaintext_code, key=key),
        status="started",
        attempts=0,
        created_at=current,
        expires_at=current + timedelta(seconds=config.phone_code_ttl_s),
        provider=provider,
        provider_message_id=None,
    )
    store.create(session)
    return session, plaintext_code


def verify_phone_code(
    *,
    store: PhoneVerificationSessionStore,
    config: AppConfig,
    session_id: str,
    submitted_code: str,
    e164: str,
    now: datetime | None = None,
) -> PhoneVerificationResult:
    current = now or _utcnow()
    key = _hashing_key(config)

    session = store.get_by_id(session_id)
    if session is None:
        raise SmsSenderError("phone verification session not found", code=SmsErrorCode.UNKNOWN)

    if session.status != "started":
        raise SmsSenderError("phone verification session is not active", code=SmsErrorCode.UNKNOWN)

    if session.expires_at < current:
        store.mark_expired(session_id)
        raise SmsSenderError("verification code expired", code=SmsErrorCode.CODE_EXPIRED)

    if _code_matches(submitted_code=submitted_code, code_hash=session.code_hash, key=key):
        store.mark_consumed(session_id)
        verified_at = current
        return PhoneVerificationResult(
            provider=session.provider,
            dial_prefix=session.dial_prefix,
            subject_hash=hash_secret(e164, key=key),
            verified_at=verified_at,
        )

    attempts = session.attempts + 1
    if attempts >= config.phone_max_attempts:
        updated = PhoneVerificationSession(
            id=session.id,
            supabase_user_id=session.supabase_user_id,
            phone_hash=session.phone_hash,
            dial_prefix=session.dial_prefix,
            code_hash=session.code_hash,
            status="failed",
            attempts=attempts,
            created_at=session.created_at,
            expires_at=session.expires_at,
            provider=session.provider,
            provider_message_id=session.provider_message_id,
        )
        store.replace(updated)
        raise SmsSenderError("too many verification attempts", code=SmsErrorCode.TOO_MANY_ATTEMPTS)

    updated = PhoneVerificationSession(
        id=session.id,
        supabase_user_id=session.supabase_user_id,
        phone_hash=session.phone_hash,
        dial_prefix=session.dial_prefix,
        code_hash=session.code_hash,
        status="started",
        attempts=attempts,
        created_at=session.created_at,
        expires_at=session.expires_at,
        provider=session.provider,
        provider_message_id=session.provider_message_id,
    )
    store.replace(updated)
    raise SmsSenderError("verification code mismatch", code=SmsErrorCode.CODE_MISMATCH)
