# Story acceptance gate — STORY-IDS-SMSPM-01-provider-config-registry

- **Story:** Provider config + registry: `SMS_PROVIDER=smspm`
- **Package:** `pkg-000046-20260820-epic-ids-14-smspm-01-provider-config.yaml`
- **Result:** PASS
- **Date:** 2026-08-20T09:59:19Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `SMS_PROVIDER=smspm` принимается конфигом; неизвестное имя по-прежнему отклоняется. | PASS | t02 [`registry_builder.py:11-16`](../../../../../../../src/core/phone/registry_builder.py); t03 `test_smspm_sms_provider_loads_with_required_env`, `test_unknown_sms_provider_still_rejected` |
| При `smspm` без `SMSPM_HASH` / `SMSPM_TOKEN` / `SMSPM_FROM` сервис не стартует с ясной config-ошибкой. | PASS | t01 [`config.py:15-18`](../../../../../../../src/core/phone/smspm/config.py); t03 `test_smspm_sms_provider_requires_{hash,token,from}` |
| При `SMS_PROVIDER=mock\|file\|telnyx` поведение не регрессирует (SMSPM env не обязательны). | PASS | t03 `test_{mock,file,telnyx}_without_smspm_env_ok` |
| `.env.example` содержит блок SMSPM и обновлённый комментарий провайдеров. | PASS | t04 [`.env.example:60,80-84`](../../../../../../../.env.example) |
| T01–T04 закрыты; descriptor в `ALL_SMS_PROVIDER_DESCRIPTORS`. | PASS | t02 [`SMSPM_SMS_DESCRIPTOR`](../../../../../../../src/core/phone/smspm/descriptor.py); this gate t05 |

## Commands (live verification 2026-08-20)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
cd doge-identity-service
.venv/bin/python -m pytest tests/test_smspm_config.py -q
# 11 passed
.venv/bin/python -m pytest -q -m "not live_integration"
# 417 passed, 12 deselected (2026-08-20T09:59:19Z)
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
