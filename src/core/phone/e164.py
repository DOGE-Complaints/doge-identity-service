from __future__ import annotations

from core.phone.base import SmsErrorCode, SmsSenderError


def normalize_to_e164(raw: str) -> str:
    stripped = raw.strip()
    if not stripped:
        raise SmsSenderError("phone number is empty", code=SmsErrorCode.INVALID_PHONE)

    compact = "".join(ch for ch in stripped if ch not in " ()-\t")
    if not compact:
        raise SmsSenderError("phone number is empty", code=SmsErrorCode.INVALID_PHONE)

    if compact.startswith("+"):
        digits = compact[1:]
        if not digits.isdigit():
            raise SmsSenderError(
                f"invalid E.164 phone number: {raw!r}",
                code=SmsErrorCode.INVALID_PHONE,
            )
        return f"+{digits}"

    if compact.isdigit():
        return f"+{compact}"

    raise SmsSenderError(
        f"invalid E.164 phone number: {raw!r}",
        code=SmsErrorCode.INVALID_PHONE,
    )


def resolve_dial_prefix(e164: str, allowed_prefixes: tuple[str, ...]) -> str:
    if not allowed_prefixes:
        return e164[:4] if len(e164) >= 4 else e164
    matches = [prefix for prefix in allowed_prefixes if e164.startswith(prefix)]
    if not matches:
        raise SmsSenderError(
            f"dial prefix not allowed for {e164!r}",
            code=SmsErrorCode.COUNTRY_NOT_ALLOWED,
        )
    return max(matches, key=len)


def assert_allowed_dial_prefix(e164: str, allowed_prefixes: tuple[str, ...]) -> None:
    resolve_dial_prefix(e164, allowed_prefixes)
