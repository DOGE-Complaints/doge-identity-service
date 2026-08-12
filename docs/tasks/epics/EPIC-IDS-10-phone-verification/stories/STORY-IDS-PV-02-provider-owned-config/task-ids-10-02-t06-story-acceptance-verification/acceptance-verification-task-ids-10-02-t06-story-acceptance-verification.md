# Acceptance verification — task-ids-10-02-t06-story-acceptance-verification

- **Gate:** PASS (2026-06-11)
- **Wave:** pkg-000023
- **Story:** STORY-IDS-PV-02-provider-owned-config

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| `SMS_PROVIDER` валидируется по реестру; неизвестный → понятная `ConfigError` | PASS | t02/t05 — `schema.py` membership + `tests/test_phone_config_schema.py::test_unknown_sms_provider_rejected` |
| `PHONE_ALLOWED_DIAL_PREFIXES` парсится; `+372` ok / `+1` → `COUNTRY_NOT_ALLOWED` | PASS | t02/t03/t05 — `e164.py::assert_allowed_dial_prefix`; `tests/test_phone_e164.py` |
| Нормализация E.164 (пробелы/скобки/без `+`) | PASS | t03/t05 — `e164.py::normalize_to_e164`; `tests/test_phone_e164.py` |
| Ядровые phone-параметры в ядре; провайдер-поля не в `AppConfig` | PASS | t01/t02/t05 — `AppConfig` phone fields; `SmsProviderConfigSpec` on descriptor |
| `.env.example` phone-блок; offline green | PASS | t04 — `.env.example`; t05 — 268 pytest offline |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
# 268 passed; ok 6 paths
```
