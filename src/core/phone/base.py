from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol, runtime_checkable


class SmsErrorCode(StrEnum):
    INVALID_PHONE = "INVALID_PHONE"
    COUNTRY_NOT_ALLOWED = "COUNTRY_NOT_ALLOWED"
    RATE_LIMITED = "RATE_LIMITED"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    SEND_FAILED = "SEND_FAILED"
    CODE_MISMATCH = "CODE_MISMATCH"
    CODE_EXPIRED = "CODE_EXPIRED"
    TOO_MANY_ATTEMPTS = "TOO_MANY_ATTEMPTS"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class SmsSendResult:
    provider_message_id: str | None
    accepted: bool


class SmsSenderError(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: SmsErrorCode = SmsErrorCode.UNKNOWN,
    ) -> None:
        self.code = code
        super().__init__(message)


@runtime_checkable
class SmsSenderPort(Protocol):
    @property
    def provider_name(self) -> str: ...

    def send(self, *, to_e164: str, text: str) -> SmsSendResult: ...
