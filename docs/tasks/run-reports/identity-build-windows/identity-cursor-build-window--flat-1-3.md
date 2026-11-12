---
generated_utc: 2026-05-29T10:20:25Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000003-20260528-epic-ids-02-fastapi-transport.yaml
window_mode: flat_slice
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project identity --write-build-window --window-flat-start 1 --window-flat-end 3
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## Плоский срез 1–3 (как в --list)
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-01-response-envelope-error-trace-id/task-ids-02-01-t01-envelope-core/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-01-response-envelope-error-trace-id/task-ids-02-01-t02-idempotency-key-resolver/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-01-response-envelope-error-trace-id/task-ids-02-01-t03-envelope-acceptance-tests/README.md`

