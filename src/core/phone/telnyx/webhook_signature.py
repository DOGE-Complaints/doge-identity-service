from __future__ import annotations

import base64
from collections.abc import Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

# Telnyx Ed25519 webhook signing — header names per Telnyx docs / SPIKE-IDS-PV-08.
_TIMESTAMP_HEADER = "telnyx-timestamp"
_SIGNATURE_HEADER = "telnyx-signature-ed25519"


def _header_value(headers: Mapping[str, str], name: str) -> str | None:
    target = name.lower()
    for key, value in headers.items():
        if key.lower() == target:
            return value
    return None


def verify_telnyx_webhook_signature(
    *,
    raw_body: bytes,
    headers: Mapping[str, str],
    public_key: str,
) -> bool:
    """Verify Telnyx webhook signature over ``{timestamp}|{body}`` using Ed25519."""
    timestamp = _header_value(headers, _TIMESTAMP_HEADER)
    signature_b64 = _header_value(headers, _SIGNATURE_HEADER)
    if not timestamp or not signature_b64 or not public_key:
        return False

    try:
        public_bytes = base64.b64decode(public_key)
        signature = base64.b64decode(signature_b64)
        key = Ed25519PublicKey.from_public_bytes(public_bytes)
        signed_payload = f"{timestamp}|".encode("utf-8") + raw_body
        key.verify(signature, signed_payload)
    except (InvalidSignature, ValueError, TypeError):
        return False
    return True
