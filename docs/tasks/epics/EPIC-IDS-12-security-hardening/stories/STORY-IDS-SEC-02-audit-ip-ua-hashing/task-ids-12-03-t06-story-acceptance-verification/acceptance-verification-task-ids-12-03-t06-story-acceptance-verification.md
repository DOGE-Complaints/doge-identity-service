# Acceptance verification — task-ids-12-03-t06-story-acceptance-verification

- **Gate:** PASS
- **Date:** 2026-06-26
- **Wave:** pkg-000037
- **Story:** STORY-IDS-SEC-02-audit-ip-ua-hashing

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| Request context reaches audit (eID + phone) | PASS | `asgi_app.py` `_audit_hashes_from_request`; `handlers.py` `_log_eid_audit` / `_log_phone_audit` with `audit=` |
| IP/UA stored as hash only | PASS | `audit_context.py` `hash_secret`; `test_audit_ip_ua_hashing.py` |
| PhoneAuditEvent ip_hash/user_agent_hash fields | PASS | `models.py` PhoneAuditEvent; wired in `_log_phone_audit` |
| No PII in audit invariant | PASS | `test_phone_audit_events_contain_no_pii`; `test_audit_ip_ua_hashing.py` |
| HMAC algorithm documented vs spec 16 | PASS | `16-security-privacy-observability.md`; `04-security.md` §9 |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
# 375 passed
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
