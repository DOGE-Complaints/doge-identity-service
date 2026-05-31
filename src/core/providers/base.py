from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class EIDVerificationResult:
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
    code: str = "EID_PROVIDER_ERROR"

    def __init__(self, message: str, *, code: str = "EID_PROVIDER_ERROR") -> None:
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
