---
generated_utc: 2026-05-31T10:25:26Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000006-20260530-epic-ids-05-supabase-persistence.yaml
window_mode: story_key
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project identity --write-build-window --story-key STORY-IDS-05-06-backend-switch-provide-service-factory
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## STORY-IDS-05-06-backend-switch-provide-service-factory
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-06-backend-switch-provide-service-factory/task-ids-05-06-t01-provide-service-factory-supabase-branch/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-06-backend-switch-provide-service-factory/task-ids-05-06-t02-supabase-fallback-test-migration/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-06-backend-switch-provide-service-factory/task-ids-05-06-t03-story6-acceptance-verification/README.md`

**Status:** 🟢 Done 2026-05-31 — t01–t03 closed; 154 pytest (`not live_integration`); run summary [`run-summary-20260531-epic-ids-05-story06-pkg-000006.md`](./run-summary-20260531-epic-ids-05-story06-pkg-000006.md)

