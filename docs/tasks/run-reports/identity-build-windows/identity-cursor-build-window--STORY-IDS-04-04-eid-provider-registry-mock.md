---
generated_utc: 2026-05-30T09:43:08Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000005-20260529-epic-ids-04-soa-service-factory.yaml
window_mode: story_key
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project identity --write-build-window --story-key STORY-IDS-04-04-eid-provider-registry-mock
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## STORY-IDS-04-04-eid-provider-registry-mock
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-04-eid-provider-registry-mock/task-ids-04-04-t01-eid-provider-port-base/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-04-eid-provider-registry-mock/task-ids-04-04-t02-eid-registry-and-mock-provider/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-04-soa-service-factory/stories/STORY-IDS-04-04-eid-provider-registry-mock/task-ids-04-04-t03-story4-acceptance-verification/README.md`

