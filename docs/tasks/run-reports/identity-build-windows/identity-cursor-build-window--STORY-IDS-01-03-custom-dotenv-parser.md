---
generated_utc: 2026-05-27T11:29:37Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000001-20260527-epic-ids-01-scaffold.yaml
window_mode: story_key
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project identity --write-build-window --story-key STORY-IDS-01-03-custom-dotenv-parser
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## STORY-IDS-01-03-custom-dotenv-parser
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-03-custom-dotenv-parser/task-ids-01-03-t01-env-file-merge/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-03-custom-dotenv-parser/task-ids-01-03-t02-provide-app-config/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-01-scaffold-config-launch/stories/STORY-IDS-01-03-custom-dotenv-parser/task-ids-01-03-t03-dotenv-parser-tests/README.md`

