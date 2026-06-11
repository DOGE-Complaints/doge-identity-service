from __future__ import annotations

import pytest

from core.phone.base import SmsErrorCode, SmsSenderError
from core.phone.e164 import assert_allowed_dial_prefix, normalize_to_e164


def test_normalize_strips_spaces_and_parens() -> None:
    assert normalize_to_e164("+372 (5555) 5555") == "+37255555555"
    assert normalize_to_e164("372 5555 5555") == "+37255555555"


def test_normalize_without_plus_prefix() -> None:
    assert normalize_to_e164("37255555555") == "+37255555555"


def test_prefix_gate_allows_estonia() -> None:
    e164 = normalize_to_e164("+37255555555")
    assert_allowed_dial_prefix(e164, ("+372",))


def test_prefix_gate_rejects_us() -> None:
    e164 = normalize_to_e164("+15551234567")
    with pytest.raises(SmsSenderError) as exc_info:
        assert_allowed_dial_prefix(e164, ("+372",))
    assert exc_info.value.code is SmsErrorCode.COUNTRY_NOT_ALLOWED


def test_invalid_phone_raises() -> None:
    with pytest.raises(SmsSenderError) as exc_info:
        normalize_to_e164("not-a-phone")
    assert exc_info.value.code is SmsErrorCode.INVALID_PHONE
