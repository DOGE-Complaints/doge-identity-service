# Acceptance verification — task-ids-10-10-t08-audit-f1-pipeline-story-timestamp-example-sync

- **Gap:** F1 — pipeline story ms timestamps vs code seconds
- **Wave:** override `epic_ids_10_pv_10_audit_2026_06_28`
- **Result:** PASS
- **Date:** 2026-06-28T18:11:05Z

## AC checklist

| AC | Status | Evidence |
|----|--------|----------|
| Pipeline example second-precision timestamps | 🟢 Done | backlog + pipeline both `T10:01:02Z` / `T10:03:40Z` |
| No `345Z`/`118Z` in pipeline story | 🟢 Done | grep exit 1 (no matches) |

## Verification commands (live)

```bash
grep -n "345Z\|118Z" doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/STORY-IDS-PV-10-file-sms-sink-dev.md
# exit 1 — no matches
grep -n "T10:01:02Z" doge-identity-service/docs/tasks/backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md \
  doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/STORY-IDS-PV-10-file-sms-sink-dev.md
# both files line match
```
