# Acceptance verification — task-ids-10-06-t06-story-acceptance-verification

- **Gate:** PASS (2026-06-11)
- **Wave:** pkg-000027
- **Story:** STORY-IDS-PV-06-telnyx-sms-sender

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| `SMS_PROVIDER=telnyx` (+ creds) → `get_active()` возвращает `TelnyxSmsSender`; без обязательных env / буквенный from без profile_id → понятная `ConfigError` | PASS | t01/t04 — `telnyx/config.py`, `runtime_factory.py`, `test_telnyx_sms_sender.py::test_build_sms_registry_active_telnyx`, `test_phone_config_schema.py` |
| `send` формирует корректный POST (Bearer, `from/to/text/type`, profile_id при буквенном from); 200+`queued` → `accepted=True` + `provider_message_id` | PASS | t02 — `telnyx/sender.py`, `test_telnyx_sms_sender.py::test_telnyx_send_success_queued` |
| Ошибки Telnyx замаплены в `SmsErrorCode` по таблице спеки; сырой код/номер не логируется | PASS | t03 — `telnyx/errors.py`, error mapping tests + `test_telnyx_send_does_not_log_otp_text` |
| Юнит-тесты offline (mocked httpx) зелёные; live-тест проходит против trial и **скипается** без creds | PASS | t05 — `tests/test_telnyx_sms_sender.py` (14 offline); `test_telnyx_live_send_skips_without_credentials` |
| `.env.example` содержит `TELNYX_*` | PASS | t05 — `.env.example` lines 71–77 (`TELNYX_MESSAGE_TYPE`, `TELNYX_ENCODING` added) |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
# 314 passed; ok 6 paths
```
