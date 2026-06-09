from __future__ import annotations

import secrets
import uuid
from datetime import datetime, timedelta, timezone

from core.domain.contracts import VerificationSessionStore
from core.domain.models import VerificationSession
from core.providers.base import EIDStartResult, EIDVerificationResult


class MockEIDProvider:
    def __init__(self, verification_session_store: VerificationSessionStore) -> None:
        self._verification_session_store = verification_session_store

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def callback_path(self) -> str:
        return "/auth/mock/callback"

    def start_flow(
        self,
        *,
        supabase_user_id: str,
        return_url: str,
        return_context: str | None = None,
        requested_action: str | None = None,
    ) -> EIDStartResult:
        session_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=10)
        session = VerificationSession(
            id=session_id,
            supabase_user_id=supabase_user_id,
            state=secrets.token_urlsafe(16),
            nonce=None,
            code_verifier_encrypted=None,
            code_verifier_hash=None,
            return_context=return_context,
            return_url=return_url,
            requested_action=requested_action,
            status="started",
            created_at=now,
            expires_at=expires_at,
            provider="mock",
            provider_session_data={},
        )
        self._verification_session_store.create(session)
        redirect_url = f"{self.callback_path}?session_id={session_id}"
        return EIDStartResult(
            redirect_url=redirect_url,
            session_id=session_id,
            expires_at=expires_at,
        )

    def handle_callback(
        self,
        *,
        raw_params: dict[str, str],
    ) -> EIDVerificationResult:
        del raw_params
        return EIDVerificationResult(
            provider="mock",
            country="EE",
            subject_hash=secrets.token_hex(16),
            login_method="mock",
            verified_at=datetime.now(timezone.utc),
        )
