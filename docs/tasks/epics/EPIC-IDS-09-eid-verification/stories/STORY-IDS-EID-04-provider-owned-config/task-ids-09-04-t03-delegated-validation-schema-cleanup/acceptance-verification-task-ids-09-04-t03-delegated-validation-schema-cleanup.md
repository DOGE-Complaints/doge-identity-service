# Acceptance verification — task-ids-09-04-t03-delegated-validation-schema-cleanup

- **Gate:** PASS (2026-06-08)
- **Wave:** pkg-000017

| Criterion | Result |
|-----------|--------|
| Delegated validate on active provider | PASS — `_validate_active_eid_provider_config` in `schema.py` |
| eideasy if removed from schema | PASS — grep + `test_schema_has_no_provider_specific_ifs` |
| eideasy validation via config_spec | PASS — `eideasy/config.py`; `test_eideasy_provider_requires_credentials` |
