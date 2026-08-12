# Acceptance verification — task-ids-09-04-t06-story-acceptance-verification

- **Gate:** PASS (2026-06-08)
- **Wave:** pkg-000017
- **Story:** STORY-IDS-EID-04-provider-owned-config

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| Authentigate-поля в `AuthentigateSettings`/`config_spec`, не в `load_config_from_env` | PASS | `authentigate/config.py`, `authentigate/descriptor.py` |
| `EID_PROVIDER=authentigate` без required → `ConfigError` с именем поля | PASS | `test_authentigate_provider_requires_client_id` |
| Новый провайдер без правок `schema.py` | PASS | eideasy/authentigate config_spec; no provider-if in schema |
| `scopes` default full claim-URL (SPIKE-09 live deferred) | PASS | `test_authentigate_settings_default_scopes_use_full_claim_urls` |
| `.env.example` актуален; offline green; missing required test | PASS | `.env.example`; 222 pytest |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
# 222 passed, 10 deselected
```
