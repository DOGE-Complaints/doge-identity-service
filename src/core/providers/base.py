from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol, runtime_checkable


class EidErrorCode(StrEnum):
    USER_CANCELLED = "USER_CANCELLED"
    STATE_MISMATCH = "STATE_MISMATCH"
    TOKEN_EXCHANGE_FAILED = "TOKEN_EXCHANGE_FAILED"
    IDENTITY_VALIDATION_FAILED = "IDENTITY_VALIDATION_FAILED"
    MISSING_REQUIRED_CLAIM = "MISSING_REQUIRED_CLAIM"
    COUNTRY_NOT_ALLOWED = "COUNTRY_NOT_ALLOWED"
    METHOD_NOT_ALLOWED = "METHOD_NOT_ALLOWED"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class EIDVerificationResult:
    """Provider callback result. `provider` is provenance only."""

    provider: str
    country: str
    subject_hash: str
    login_method: str
    verified_at: datetime


@dataclass
class EIDStartResult:
    redirect_url: str
    session_id: str
    expires_at: datetime


class EIDProviderError(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: EidErrorCode = EidErrorCode.UNKNOWN,
    ) -> None:
        self.code = code
        super().__init__(message)


@runtime_checkable
class EIDProviderPort(Protocol):
    @property
    def provider_name(self) -> str: ...

    @property
    def callback_path(self) -> str: ...

    def start_flow(
        self,
        *,
        supabase_user_id: str,
        return_url: str,
        return_context: str | None = None,
        requested_action: str | None = None,
    ) -> EIDStartResult: ...

    def handle_callback(
        self,
        *,
        raw_params: dict[str, str],
    ) -> EIDVerificationResult: ...
