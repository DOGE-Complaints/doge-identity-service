# Acceptance verification — task-ids-14-01-t06-audit-f1-smspm-test-count-docs

- **Gate:** PASS
- **Wave:** override `epic_ids_14_smspm_01_audit_2026_08_20`
- **Story:** STORY-IDS-SMSPM-01-provider-config-registry (audit F1)
- **Date:** 2026-08-20T10:13:10Z
- **Package:** pkg-000046 unchanged (immutable default)

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| t05 gate `# 12 passed` → `# 11 passed` | PASS | [`acceptance-verification-…t05…md:25`](../task-ids-14-01-t05-story-acceptance-verification/acceptance-verification-task-ids-14-01-t05-story-acceptance-verification.md) |
| run-summary `# 12 passed` → `# 11 passed` | PASS | [`run-summary-20260820-0959-epic-ids-14-smspm-01-pkg-000046.md:25`](../../../../../../run-reports/identity-build-windows/run-summary-20260820-0959-epic-ids-14-smspm-01-pkg-000046.md) |
| File still has 11 `def test_*` | PASS | [`tests/test_smspm_config.py`](../../../../../../../tests/test_smspm_config.py) — `rg -c '^def test_'` = 11 |
| No `src/` / pytest / 🟢 t01–t05 / story Done change | PASS | docs-only this P6 |
| t05 gate `Date:` not restamped | PASS | still `2026-08-20T09:59:19Z` |

## Commands (live verification 2026-08-20T10:13:10Z)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
rg -n '12 passed|11 passed' \
  doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-01-provider-config-registry/task-ids-14-01-t05-story-acceptance-verification/acceptance-verification-task-ids-14-01-t05-story-acceptance-verification.md \
  doge-identity-service/docs/tasks/run-reports/identity-build-windows/run-summary-20260820-0959-epic-ids-14-smspm-01-pkg-000046.md
rg -c '^def test_' doge-identity-service/tests/test_smspm_config.py
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
