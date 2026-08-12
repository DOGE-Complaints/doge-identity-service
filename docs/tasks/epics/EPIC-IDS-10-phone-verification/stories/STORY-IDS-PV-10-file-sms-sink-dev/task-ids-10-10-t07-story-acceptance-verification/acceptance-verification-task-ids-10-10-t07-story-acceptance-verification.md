# Story acceptance gate — STORY-IDS-PV-10-file-sms-sink-dev

- **Story:** STORY-IDS-PV-10 — File SMS sink (dev)
- **Package:** `pkg-000041-20260628-epic-ids-10-pv-10-file-sms-sink-dev.yaml`
- **Result:** PASS
- **Date:** 2026-06-28

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `SMS_PROVIDER=file` → `FileSmsSender`; request appends `{utc}\t{text}` to outbox | PASS | `file/descriptor.py`, `registry_builder.py`; `test_phone_request_with_file_provider_writes_outbox_log` |
| Append same number; different numbers → different files | PASS | `file_sender.py`; `test_file_sender_appends_two_lines_same_number`, `test_file_sender_uses_different_files_for_different_numbers` |
| `tail -f` DX for manual test | PASS | append log format `{utc_iso}\t{text}` in `file_sender.py:38-41`; manual via `FILE_SMS_OUTBOX_DIR` |
| Filename sanitize (`+` and digits only) | PASS | `sanitize_phone_log_basename` in `file_sender.py:19-21`; `test_sanitize_phone_log_basename_strips_unsafe_chars` |
| `APP_PROFILE=pilot` + `SMS_PROVIDER=file` → `ConfigError` | PASS | `schema.py:180-183`; `test_pilot_profile_rejects_file_sms_provider` |
| `file` does not create `httpx.Client` | PASS | `runtime_factory.py:14-15`; `test_build_sms_provider_runtime_file_skips_http_client` |
| outbox in `.gitignore`; `.env.example` updated | PASS | `.gitignore` `var/sms-outbox/`; `.env.example:63,71-72` |
| Offline pytest green | PASS | `.venv/bin/python -m pytest -m "not live_integration" -q` → 394 passed |

## Commands (live verification 2026-06-28)

```bash
cd doge-identity-service
.venv/bin/python -m pytest tests/test_phone_file_sms_sender.py -q
# 8 passed
.venv/bin/python -m pytest -m "not live_integration" -q
# 394 passed
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
# ok 7 paths · ok date-check
```
