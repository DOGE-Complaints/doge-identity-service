# Acceptance verification — task-ids-10-03-t06-story-acceptance-verification

- **Gate:** PASS (2026-06-11)
- **Wave:** pkg-000024
- **Story:** STORY-IDS-PV-03-otp-engine-session

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| `PhoneVerificationSession` + store (in-memory + supabase-совместимый интерфейс) с `attempts` | PASS | t01/t02 — `models.py`, `contracts.py`, `InMemoryPhoneVerificationSessionStore`; t05 — `test_phone_verification_session_store.py` |
| OTP криптослучайно, только хэш; код не логируется | PASS | t03 — `otp_engine.py`; t05 — `test_create_returns_plaintext_code_and_stores_hash_only`, `test_plaintext_code_not_logged` |
| Сверка: ok / `CODE_MISMATCH` / `TOO_MANY_ATTEMPTS` / `CODE_EXPIRED` | PASS | t04 — `verify_phone_code`; t05 — mismatch/limit/expired tests |
| Повторный `request` инвалидирует прежний код | PASS | t03/t05 — `test_repeat_create_invalidates_previous_session` |
| `subject_hash = hash_secret(e164)` без провайдер-префикса | PASS | t04/t05 — `test_verify_success_returns_subject_hash_without_provider_prefix` |
| Offline-тесты: успех/несовпадение/просрочка/лимит/повтор-инвалидация | PASS | t05 — 12 tests; full suite 280 passed |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
# 280 passed; ok 6 paths
```
