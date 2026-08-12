# Acceptance verification — task-ids-09-04-t08-audit-f2-eid-provider-membership-from-descriptors

- **Wave:** `override epic_ids_09_eid_04_audit_2026_06_08`
- **Audit:** F2 ([`epic-ids-09-eid-04-audit-2026-06-08.md`](../../../../../../analysis/epic-ids-09-eid-04-audit-2026-06-08.md))

## Evidence

```bash
cd doge-identity-service
grep -n '"mock", "eideasy", "authentigate"' src/core/config/schema.py || echo "no hardcoded literal"
.venv/bin/python -m pytest tests/test_provider_owned_config.py tests/test_config_schema.py -m "not live_integration" -q
.venv/bin/python -m pytest -m "not live_integration" -q
```

- `registered_eid_provider_names()` в [`registry_builder.py`](../../../../../../../src/core/providers/registry_builder.py)
- `load_config_from_env` использует каталог; нет хардкод-литерала в `schema.py`
- `test_unknown_eid_provider_rejected` — PASS
- `test_schema_has_no_provider_specific_ifs` — расширен (literal + `registered_eid_provider_names`)
- Offline suite: **222 passed**

## AC/DoD

| Criterion | Result |
|-----------|--------|
| `registered_eid_provider_names()` из каталога | PASS |
| Membership через каталог, без literal в schema | PASS |
| Unknown `EID_PROVIDER` → `ConfigError` | PASS |
| Тест на отсутствие дублирования membership | PASS |
| Offline suite green | PASS |
