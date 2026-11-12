---
generated_utc: 2026-07-24T18:55:19Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000045-20260724-epic-ids-13-onb-01-email-in-me.yaml
window_mode: flat_slice
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --write-build-window --window-flat-start 1 --window-flat-end 4
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## Плоский срез 1–4 (как в --list)
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/task-ids-13-02-t01-me-response-email-and-email-verified/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/task-ids-13-02-t02-confirm-email-runbook-and-me-api-docs/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/task-ids-13-02-t03-me-profile-offline-tests-email-fields/README.md`
4. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/task-ids-13-02-t04-story-acceptance-verification/README.md`

