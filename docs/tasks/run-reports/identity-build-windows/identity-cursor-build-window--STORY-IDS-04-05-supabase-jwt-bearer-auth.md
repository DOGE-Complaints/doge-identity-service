---
generated_utc: 2026-05-30T09:43:18Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000005-20260529-epic-ids-04-soa-service-factory.yaml
window_mode: story_key
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project identity --write-build-window --story-key STORY-IDS-04-05-supabase-jwt-bearer-auth
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## STORY-IDS-04-05-supabase-jwt-bearer-auth
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-05-supabase-jwt-bearer-auth/task-ids-04-05-t01-supabase-jwt-validator-impl/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-05-supabase-jwt-bearer-auth/task-ids-04-05-t02-supabase-jwt-bearer-token-auth/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-05-supabase-jwt-bearer-auth/task-ids-04-05-t03-story5-acceptance-verification/README.md`

