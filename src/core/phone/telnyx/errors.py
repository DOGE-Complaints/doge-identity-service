from __future__ import annotations

import logging

import httpx

from core.phone.base import SmsErrorCode, SmsSenderError

logger = logging.getLogger(__name__)

_COUNTRY_NOT_ALLOWED_CODES = frozenset({"40309", "40331"})
_RATE_LIMITED_CODES = frozenset({"10011", "40318"})
_INVALID_PHONE_CODES = frozenset({"10002", "10016", "40310", "40012", "40001", "40008"})
_SEND_FAILED_CODES = frozenset(
    {
        "40305",
        "40306",
        "40307",
        "40312",
        "40314",
        "40315",
        "40320",
        "40321",
        "40323",
        "40325",
        "40333",
        "40100",
        "40009",
        "40302",
        "40316",
        "40322",
    }
)


def extract_telnyx_error_codes(response: httpx.Response) -> list[str]:
    try:
        body = response.json()
    except ValueError:
        return []
    errors = body.get("errors") or []
    codes: list[str] = []
    for item in errors:
        if not isinstance(item, dict):
            continue
        code = item.get("code")
        if code is not None:
            codes.append(str(code))
    return codes


def map_telnyx_error(
    *,
    status_code: int,
    error_codes: list[str],
    reason: str = "Telnyx request failed",
) -> SmsSenderError:
    if status_code == 429 or any(code in _RATE_LIMITED_CODES for code in error_codes):
        code = SmsErrorCode.RATE_LIMITED
    elif status_code >= 500:
        code = SmsErrorCode.PROVIDER_UNAVAILABLE
    elif any(item in _COUNTRY_NOT_ALLOWED_CODES for item in error_codes):
        code = SmsErrorCode.COUNTRY_NOT_ALLOWED
    elif any(item in _INVALID_PHONE_CODES for item in error_codes):
        code = SmsErrorCode.INVALID_PHONE
    elif any(item in _SEND_FAILED_CODES for item in error_codes):
        code = SmsErrorCode.SEND_FAILED
    else:
        code = SmsErrorCode.UNKNOWN

    safe_codes = ",".join(error_codes) if error_codes else str(status_code)
    logger.warning("Telnyx SMS error mapped to %s (provider_codes=%s)", code.value, safe_codes)
    return SmsSenderError(reason, code=code)


def map_telnyx_timeout() -> SmsSenderError:
    logger.warning("Telnyx SMS request timed out")
    return SmsSenderError("Telnyx request timed out", code=SmsErrorCode.PROVIDER_UNAVAILABLE)
