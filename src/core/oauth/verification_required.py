from __future__ import annotations

from core.config.schema import AppConfig
from core.oauth.spa_login import build_spa_verify_url

# Verify-need uses HTTP 403 + this payload — not SmsErrorCode (400) from phone OTP paths.
VERIFICATION_REQUIRED_HTTP_STATUS = 403
VERIFICATION_REQUIRED_ERROR = "verification_required"
DEFAULT_VERIFICATION_REQUIRED_REASON = (
    "Phone verification is required before this action can proceed."
)


def build_verification_required_body(
    *,
    verify_url: str,
    reason: str = DEFAULT_VERIFICATION_REQUIRED_REASON,
) -> dict[str, str]:
    return {
        "error": VERIFICATION_REQUIRED_ERROR,
        "reason": reason,
        "verify_url": verify_url,
    }


def build_verification_required_response(
    config: AppConfig,
    *,
    return_context: str | None,
    reason: str = DEFAULT_VERIFICATION_REQUIRED_REASON,
) -> tuple[dict[str, str], int]:
    verify_url = build_spa_verify_url(config, return_context=return_context)
    body = build_verification_required_body(verify_url=verify_url, reason=reason)
    return body, VERIFICATION_REQUIRED_HTTP_STATUS
