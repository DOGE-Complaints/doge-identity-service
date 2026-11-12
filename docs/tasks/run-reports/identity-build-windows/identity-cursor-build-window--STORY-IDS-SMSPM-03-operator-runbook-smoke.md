---
generated_utc: 2026-08-20T10:46:31Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000048-20260820-epic-ids-14-smspm-03-operator-runbook-smoke.yaml
window_mode: story_key
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --write-build-window --story-key STORY-IDS-SMSPM-03-operator-runbook-smoke
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## STORY-IDS-SMSPM-03-operator-runbook-smoke
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/task-ids-14-03-t01-runbook-mode-c-env-table/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/task-ids-14-03-t02-runbook-curl-smoke/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/task-ids-14-03-t03-runbook-troubleshooting/README.md`
4. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/task-ids-14-03-t04-live-ee-smoke-run-summary/README.md`
5. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-03-operator-runbook-smoke/task-ids-14-03-t05-story-acceptance-verification/README.md`

