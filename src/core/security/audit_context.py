"""Audit request context: hashed IP and User-Agent for storage."""

from __future__ import annotations

from dataclasses import dataclass

from fastapi import Request

from core.api.request_context import client_ip, user_agent
from core.security.hashing import hash_secret


@dataclass(frozen=True)
class AuditHashes:
    ip_hash: str | None
    user_agent_hash: str | None


def hash_audit_value(plaintext: str | None, *, key: str) -> str | None:
    if plaintext is None or not plaintext.strip():
        return None
    return hash_secret(plaintext, key=key)


def audit_hashes_from_request(
    request: Request,
    *,
    hashing_key: str,
    trusted_proxy_count: int,
) -> AuditHashes:
    key = hashing_key or ""
    ip = client_ip(request, trusted_proxy_count=trusted_proxy_count)
    ua = user_agent(request)
    return AuditHashes(
        ip_hash=hash_audit_value(ip, key=key),
        user_agent_hash=hash_audit_value(ua, key=key),
    )
