from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from core.phone.base import SmsSendResult


@dataclass
class MockSmsSender:
    """Dev SMS sender: captures messages in memory, always accepts."""

    _sent: list[tuple[str, str]] = field(default_factory=list)

    @property
    def provider_name(self) -> str:
        return "mock"

    @property
    def sent_messages(self) -> list[tuple[str, str]]:
        return list(self._sent)

    def send(self, *, to_e164: str, text: str) -> SmsSendResult:
        self._sent.append((to_e164, text))
        return SmsSendResult(provider_message_id=f"mock-{uuid.uuid4()}", accepted=True)
