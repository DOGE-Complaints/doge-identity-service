# Acceptance verification — task-ids-09-04-t02-authentigate-settings-config-spec

- **Gate:** PASS (2026-06-08)
- **Wave:** pkg-000017

| Criterion | Result |
|-----------|--------|
| AuthentigateSettings fields | PASS — `authentigate/config.py` |
| Full claim-URL default scopes | PASS — `DEFAULT_AUTHENTIGATE_SCOPES` |
| AUTHENTIGATE_CONFIG_SPEC + descriptor | PASS — `authentigate/descriptor.py` |
| Registered in ALL_EID_PROVIDER_DESCRIPTORS | PASS — `registry_builder.py` |
| Build stub (EID-02 deferred) | PASS — raises ProviderNotRegisteredError |
