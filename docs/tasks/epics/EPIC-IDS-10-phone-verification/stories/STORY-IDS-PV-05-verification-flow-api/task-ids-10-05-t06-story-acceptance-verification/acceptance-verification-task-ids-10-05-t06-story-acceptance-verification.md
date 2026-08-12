# Acceptance verification — task-ids-10-05-t06-story-acceptance-verification

- **Gate:** PASS (2026-06-11)
- **Wave:** pkg-000026
- **Story:** STORY-IDS-PV-05-verification-flow-api

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| `POST /auth/phone/request` (валидный JWT, разрешённый префикс) → создаёт сессию `started`, шлёт SMS через активный провайдер, возвращает `expires_at` | PASS | t03/t05 — `handle_phone_request`, `test_phone_request_creates_session_sends_sms_and_returns_expires_at` |
| Неразрешённый префикс → `COUNTRY_NOT_ALLOWED`; повтор раньше cooldown → `RATE_LIMITED` (старый код инвалидирован при новом) | PASS | t03/t05 — `test_phone_request_country_not_allowed`, `test_phone_request_rate_limited_before_cooldown`, `test_phone_request_after_cooldown_invalidates_previous_code` |
| `POST /auth/phone/confirm` верный код → `phone_verified=true`; неверный/просрочка/лимит → корректные `SmsErrorCode`; дубль номера → 409 | PASS | t04/t05 — `handle_phone_confirm`, confirm mismatch/expiry/attempts/409 tests |
| Все события в аудите без PII (нет сырого номера/кода) | PASS | t01/t03/t04 — `PhoneAuditEvent`, `_log_phone_audit`, `test_phone_audit_events_contain_no_pii` |
| Полный флоу проходит на `MockSmsSender` офлайн-тестом | PASS | t05 — `tests/test_phone_verification_flow.py` (10 tests) |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
# 298 passed; ok 6 paths
```
