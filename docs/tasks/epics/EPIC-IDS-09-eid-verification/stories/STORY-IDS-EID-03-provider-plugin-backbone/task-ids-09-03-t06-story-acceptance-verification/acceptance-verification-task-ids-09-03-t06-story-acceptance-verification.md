# Acceptance verification — task-ids-09-03-t06-story-acceptance-verification

- **Gate:** PASS (2026-06-08)
- **Wave:** pkg-000016
- **Story:** STORY-IDS-EID-03-provider-plugin-backbone

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| EIDProviderDescriptor + ProviderRuntime; mock via descriptor | PASS | `descriptor.py`, `runtime.py`, `mock/descriptor.py` |
| Registry from descriptors; +provider = +descriptor | PASS | `registry_builder.py`, `ALL_EID_PROVIDER_DESCRIPTORS` |
| Unregistered → ProviderNotRegisteredError/ConfigError | PASS | `registry.py`; `test_get_unknown_provider_raises_config_error_with_available_list` |
| mock/in-memory no network clients | PASS | `runtime_factory.py`; httpx tests |
| offline green; guard + registry tests | PASS | 218 passed |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
# 218 passed, 10 deselected
```
