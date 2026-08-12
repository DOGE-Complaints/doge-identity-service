# Acceptance verification — task-ids-10-01-t06-story-acceptance-verification

- **Gate:** PASS (2026-06-11)
- **Wave:** pkg-000022
- **Story:** STORY-IDS-PV-01-phone-provider-backbone

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| Есть `SmsSenderPort` + `SmsSendResult` + `SmsSenderError`/`SmsErrorCode` + дескриптор + `SmsProviderRuntime` + реестр с guard | PASS | t01–t03 — `src/core/phone/base.py`, `descriptor.py`, `runtime.py`, `registry.py` |
| `MockSmsSender` собирается через дескриптор; реестр строит активный + `mock` | PASS | t04 — `mock/descriptor.py`; t05 — `test_build_sms_registry_registers_mock` |
| `SMS_PROVIDER=<незарегистрированный>` → `SmsProviderNotRegisteredError`/`ConfigError` с перечислением доступных | PASS | t03/t05 — `registry.py:16-21`; `test_get_active_unknown_provider_raises_guard_error` |
| Добавление провайдера = +1 дескриптор, без правок ядра реестра | PASS | t03 — `ALL_SMS_PROVIDER_DESCRIPTORS` tuple in `registry_builder.py` |
| Offline-тесты зелёные (guard + сборка реестра + mock.send) | PASS | t05 — 259 pytest offline (+6) |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
# 259 passed; ok 6 paths
```
