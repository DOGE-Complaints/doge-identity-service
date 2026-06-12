from __future__ import annotations

import base64
import json

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from core.phone.telnyx.webhook_signature import verify_telnyx_webhook_signature


def _sign_body(*, body: bytes, timestamp: str, private_key: Ed25519PrivateKey) -> dict[str, str]:
    signed_payload = f"{timestamp}|".encode("utf-8") + body
    signature = private_key.sign(signed_payload)
    return {
        "telnyx-timestamp": timestamp,
        "telnyx-signature-ed25519": base64.b64encode(signature).decode("ascii"),
    }


def test_verify_telnyx_webhook_signature_valid() -> None:
    private_key = Ed25519PrivateKey.generate()
    public_key = base64.b64encode(private_key.public_key().public_bytes_raw()).decode("ascii")
    body = json.dumps({"data": {"event_type": "message.sent"}}).encode("utf-8")
    headers = _sign_body(body=body, timestamp="1700000000", private_key=private_key)

    assert verify_telnyx_webhook_signature(raw_body=body, headers=headers, public_key=public_key)


def test_verify_telnyx_webhook_signature_tampered_body_fails() -> None:
    private_key = Ed25519PrivateKey.generate()
    public_key = base64.b64encode(private_key.public_key().public_bytes_raw()).decode("ascii")
    body = json.dumps({"data": {"event_type": "message.sent"}}).encode("utf-8")
    headers = _sign_body(body=body, timestamp="1700000000", private_key=private_key)
    tampered = body + b"tamper"

    assert not verify_telnyx_webhook_signature(raw_body=tampered, headers=headers, public_key=public_key)


def test_verify_telnyx_webhook_signature_wrong_key_fails() -> None:
    private_key = Ed25519PrivateKey.generate()
    other_key = Ed25519PrivateKey.generate()
    public_key = base64.b64encode(other_key.public_key().public_bytes_raw()).decode("ascii")
    body = json.dumps({"ok": True}).encode("utf-8")
    headers = _sign_body(body=body, timestamp="1700000000", private_key=private_key)

    assert not verify_telnyx_webhook_signature(raw_body=body, headers=headers, public_key=public_key)
