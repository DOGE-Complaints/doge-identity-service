# Acceptance verification — task-ids-14-01-t03-smspm-config-tests

- **Gate:** PASS
- **Wave:** pkg-000046
- **Story:** STORY-IDS-SMSPM-01-provider-config-registry
- **Date:** 2026-08-20T09:59:19Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| Accept `smspm` + HASH/TOKEN/FROM | PASS | `test_smspm_sms_provider_loads_with_required_env` |
| Fail missing required when active=`smspm` | PASS | `test_smspm_sms_provider_requires_{hash,token,from}` |
| mock\|file\|telnyx without SMSPM env | PASS | `test_{mock,file,telnyx}_without_smspm_env_ok` |
| `"smspm" in registered names`; unknown rejected | PASS | `test_registered_sms_provider_names_includes_smspm`; `test_unknown_sms_provider_still_rejected` |
| No live HTTP tests | PASS | stub send raises; no SMSPM API calls |
| Related SMS tests green | PASS | 45 passed on smspm+telnyx+file+registry slice; full offline 417 passed, 12 deselected |

Commands: `.venv/bin/python -m pytest -q tests/test_smspm_config.py tests/test_phone_config_schema.py tests/test_telnyx_sms_sender.py tests/test_phone_file_sms_sender.py tests/test_sms_provider_registry.py -m "not live_integration"`
