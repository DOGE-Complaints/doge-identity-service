# Acceptance verification — task-ids-12-02-t06-story-acceptance-verification

- **Gate:** PASS
- **Date:** 2026-06-26
- **Wave:** pkg-000036
- **Story:** STORY-IDS-SEC-01b-phone-request-http-rate-limit

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| phone/request wired per-user + config | PASS | `rate_limit_config.py` ROUTE_AUTH_PHONE_REQUEST; `schema.py` RATE_LIMIT_PHONE_REQUEST_*; `asgi_app.py` Depends |
| HTTP 429 vs cooldown 400 | PASS | `test_phone_request_rate_limit_returns_429_with_retry_after`; `test_phone_otp_cooldown_still_domain_400_not_http_429` |
| Coexistence policy documented | PASS | `04-security.md` §8; `19-phone-verification-flow.md` G-3; `handlers.py` comment |
| Offline both scenarios | PASS | `tests/test_rate_limiting.py` (5 tests) |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
# 371 passed
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
