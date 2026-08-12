# Acceptance verification — task-ids-11-04-t07-story-acceptance-verification

- **Gate:** PASS
- **Date:** 2026-06-24
- **Wave:** pkg-000034
- **Story:** STORY-IDS-OAUTH-04-verify-gate-and-verification-required

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| `requested_action`/`return_context` проходят authorize→complete и доступны после логина | PASS | `handlers.py` relay + `tests/test_oauth_verify_gate.py::test_oauth_authorize_relay_persists_*` |
| При действии, требующем verify, и `phone_verified=false` — identity сигналит «нужен verify», без «зелёного» статуса | PASS | `handle_oauth_authorize_complete` verify-gate; `test_oauth_complete_unverified_stories_submit_returns_verification_required` |
| Зафиксирован канон `verification_required` (403) с `verify_url`; под `phone_verified` | PASS | `verification_required.py`; contract test in `test_oauth_verify_gate.py` |
| verify-need (403) явно отделён от OTP-ошибок (`SmsErrorCode`, 400) | PASS | `VERIFICATION_REQUIRED_HTTP_STATUS=403`; `test_verification_required_separate_from_sms_error_http_mapping` |
| Покрыто offline-тестами; контракт описан для gateway | PASS | `tests/test_oauth_verify_gate.py` (6 tests); `09-gateway-expectations.md` §verification_required |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
# 366 passed
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
# ok 7 paths · ok date-check
```
