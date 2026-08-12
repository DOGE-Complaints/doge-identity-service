# Acceptance verification — task-ids-09-04-t05-offline-provider-config-tests

- **Gate:** PASS (2026-06-08)
- **Wave:** pkg-000017

| Criterion | Result |
|-----------|--------|
| authentigate missing CLIENT_ID → ConfigError | PASS — `test_authentigate_provider_requires_client_id` |
| Default scopes full claim-URLs | PASS — `test_authentigate_settings_default_scopes_use_full_claim_urls` |
| eideasy regression | PASS — `test_eideasy_provider_requires_credentials` |
| Offline suite green | PASS — 222 passed |
