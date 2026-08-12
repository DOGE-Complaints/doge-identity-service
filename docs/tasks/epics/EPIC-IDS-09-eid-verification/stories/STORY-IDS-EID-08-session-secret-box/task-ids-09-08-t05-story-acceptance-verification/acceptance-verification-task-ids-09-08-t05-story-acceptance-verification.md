# Acceptance verification — task-ids-09-08-t05-story-acceptance-verification

- **Gate:** PASS (2026-06-11)
- **Wave:** pkg-000021
- **Story:** STORY-IDS-EID-08-session-secret-box

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| Есть `SessionSecretBox` (порт + Fernet-реализация); `seal`/`open` обратимы; round-trip-тест | PASS | t01 — `session_secret.py`; t04 — `test_fernet_session_secret_box_round_trip` |
| `EID_SESSION_ENC_KEY` обязателен в `pilot` (понятная `ConfigError` при отсутствии), допустим дефолт в `demo` | PASS | t02 — `schema.py:130-147`; t04 — `test_pilot_missing_*`, `test_demo_profile_*` |
| `secret_box` доступен провайдерам через `ProviderRuntime` | PASS | t03 — `runtime_factory.py`; t04 — `test_build_provider_runtime_wires_secret_box` |
| Ключ шифрования отделён от `eid_secret` (разные назначения) | PASS | t01/t02 — separate env/field; t04 — `test_runtime_secret_box_uses_eid_session_enc_key_not_eid_secret` |
| Offline-набор зелёный | PASS | t04 — 253 pytest offline |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
# 253 passed
```
