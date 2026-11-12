# Story acceptance gate — STORY-IDS-SMSPM-03-operator-runbook-smoke

- **Story:** Operator runbook + live smoke (smspm)
- **Package:** `pkg-000048-20260820-epic-ids-14-smspm-03-operator-runbook-smoke.yaml`
- **Result:** BLOCKED
- **Date:** 2026-08-20T10:48:00Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| В `phone-sms-verification.md` есть режим C `SMS_PROVIDER=smspm` с env-чеклистом (T01). | PASS | t01 [`phone-sms-verification.md:4,54-62`](../../../../../../../runbook/phone-sms-verification.md) |
| Описан live-smoke curl-путь (T02); Telnyx и mock по-прежнему описаны (D-03-2). | PASS | t02 §6C [`:145-163`](../../../../../../../runbook/phone-sms-verification.md); §5 A; §6 B |
| Troubleshooting rows добавлены (T03). | PASS | t03 §7 [`:176-177`](../../../../../../../runbook/phone-sms-verification.md) |
| Live-smoke на тестовом EE-номере выполнен; summary в `docs/tasks/run-reports/` без секретов/PII (T04, D-03-3). | BLOCKED | t04 gate BLOCKED; [`run-summary-20260820-1048-epic-ids-14-smspm-03-live-ee-smoke.md`](../../../../../run-reports/identity-build-windows/run-summary-20260820-1048-epic-ids-14-smspm-03-live-ee-smoke.md) `result: BLOCKED` |

Story Meta remains ⚪ Todo. Dashboard Remaining **not** updated to Done. t01–t03 🟢.

## Commands (live verification 2026-08-20T10:48:00Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
rg -n 'режим C|Режим C|SMS_PROVIDER=smspm' doge-identity-service/docs/runbook/phone-sms-verification.md
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
