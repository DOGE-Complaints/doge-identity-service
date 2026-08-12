# Acceptance verification — task-ids-09-03-t04-registry-guard-config-error

- **Wave:** pkg-000016

| Criterion | Result |
|-----------|--------|
| get() guard with available list | PASS — `registry.py:17-21` |
| get_active uses same guard | PASS |
| ConfigError subclass | PASS — `ProviderNotRegisteredError` |
| Message contains «доступны» | PASS — `test_get_unknown_provider_raises_config_error_with_available_list` |
