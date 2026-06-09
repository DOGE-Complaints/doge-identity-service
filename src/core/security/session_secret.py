from __future__ import annotations

from typing import Protocol, runtime_checkable

from cryptography.fernet import Fernet, InvalidToken

__all__ = [
    "FernetSessionSecretBox",
    "SessionSecretBox",
    "SessionSecretError",
    "build_session_secret_box",
]


class SessionSecretError(Exception):
    """Session secret seal/open failure."""


@runtime_checkable
class SessionSecretBox(Protocol):
    """Provider-agnostic reversible encryption for server-side session secrets."""

    def seal(self, plaintext: str) -> str: ...

    def open(self, token: str) -> str: ...


class FernetSessionSecretBox:
    """Fernet-backed SessionSecretBox using a dedicated encryption key."""

    def __init__(self, fernet: Fernet) -> None:
        self._fernet = fernet

    @classmethod
    def from_key_string(cls, key: str) -> FernetSessionSecretBox:
        return cls(Fernet(key.encode("utf-8")))

    def seal(self, plaintext: str) -> str:
        return self._fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")

    def open(self, token: str) -> str:
        try:
            return self._fernet.decrypt(token.encode("utf-8")).decode("utf-8")
        except InvalidToken as exc:
            raise SessionSecretError("session secret token is invalid or tampered") from exc


def build_session_secret_box(*, encryption_key: str) -> SessionSecretBox:
    """Build a SessionSecretBox from the dedicated session encryption key."""
    return FernetSessionSecretBox.from_key_string(encryption_key)
