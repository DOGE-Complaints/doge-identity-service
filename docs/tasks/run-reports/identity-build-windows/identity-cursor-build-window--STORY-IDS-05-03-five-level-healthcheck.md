---
generated_utc: 2026-06-02T10:54:38Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000006-20260530-epic-ids-05-supabase-persistence.yaml
window_mode: story_key
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project identity --write-build-window --story-key STORY-IDS-05-03-five-level-healthcheck
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## STORY-IDS-05-03-five-level-healthcheck
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/task-ids-05-03-t01-supabase-database-healthcheck-methods/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/task-ids-05-03-t02-build-api-dependencies-db-checks/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-05-supabase-persistence/stories/STORY-IDS-05-03-five-level-healthcheck/task-ids-05-03-t03-story3-acceptance-verification/README.md`

