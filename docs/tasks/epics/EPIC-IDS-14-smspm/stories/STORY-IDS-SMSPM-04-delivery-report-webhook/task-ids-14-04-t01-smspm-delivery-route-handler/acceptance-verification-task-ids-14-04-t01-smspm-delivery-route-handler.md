# Acceptance verification — task-ids-14-04-t01-smspm-delivery-route-handler

- **Gate:** PASS
- **Wave:** pkg-000049
- **Story:** STORY-IDS-SMSPM-04-delivery-report-webhook
- **Date:** 2026-08-20T11:06:55Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| GET `/webhooks/smspm/delivery/{shared_secret}` registered; no `get_current_user` | PASS | [`asgi_app.py:411-423`](../../../../../../../src/core/api/asgi_app.py) |
| Valid secret → 200 plain `OK` | PASS | [`asgi_app.py:421`](../../../../../../../src/core/api/asgi_app.py) `Response(content="OK", media_type="text/plain")`; [`handlers.py:837`](../../../../../../../src/core/api/handlers.py) `return None, 200` |
| Secret mismatch → 401; no session update | PASS | [`handlers.py:776-791`](../../../../../../../src/core/api/handlers.py) `secrets.compare_digest`; tests `test_bad_secret_returns_401_and_session_unchanged` |
| Missing secret → 503 CONFIG_ERROR | PASS | [`handlers.py:766-773`](../../../../../../../src/core/api/handlers.py) |
| Optional field on settings; not in `SMSPM_REQUIRED_ENV` | PASS | [`config.py:12,27,37`](../../../../../../../src/core/phone/smspm/config.py) |
| No Ed25519 on this route | PASS | handler uses `compare_digest` only; no `verify_telnyx_webhook_signature` |
