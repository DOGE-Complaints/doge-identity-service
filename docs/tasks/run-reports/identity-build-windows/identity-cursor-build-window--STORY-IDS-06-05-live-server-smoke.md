---
generated_utc: 2026-06-02T12:50:29Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000008-20260602-epic-ids-06-testing-architecture.yaml
window_mode: story_key
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project identity --write-build-window --story-key STORY-IDS-06-05-live-server-smoke
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## STORY-IDS-06-05-live-server-smoke
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-05-live-server-smoke/task-ids-06-05-t01-smoke-conftest-and-local-server-tests/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-06-testing-architecture/stories/STORY-IDS-06-05-live-server-smoke/task-ids-06-05-t02-story5-acceptance-verification/README.md`

