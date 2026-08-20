from __future__ import annotations

import logging

import httpx

from core.phone.base import SmsErrorCode, SmsSenderError

logger = logging.getLogger(__name__)


def extract_smspm_error_text(response: httpx.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return ""
    if not isinstance(body, dict):
        return ""
    error = body.get("error")
    if isinstance(error, str):
        return error
    return ""


def map_smspm_error(*, status_code: int, error_text: str = "") -> SmsSenderError:
    lowered = error_text.lower()
    if status_code >= 500:
        code = SmsErrorCode.PROVIDER_UNAVAILABLE
        label = "http_5xx"
    elif status_code == 401:
        code = SmsErrorCode.SEND_FAILED
        label = "http_401"
    elif "invalid phone" in lowered:
        code = SmsErrorCode.INVALID_PHONE
        label = "invalid_phone"
    elif status_code >= 400:
        code = SmsErrorCode.SEND_FAILED
        label = "http_4xx"
    else:
        code = SmsErrorCode.UNKNOWN
        label = "unknown"

    logger.warning(
        "SMSPM SMS error mapped to %s (http_status=%s, reason=%s)",
        code.value,
        status_code,
        label,
    )
    return SmsSenderError("SMSPM request failed", code=code)


def map_smspm_timeout() -> SmsSenderError:
    logger.warning("SMSPM SMS request timed out")
    return SmsSenderError("SMSPM request timed out", code=SmsErrorCode.PROVIDER_UNAVAILABLE)
