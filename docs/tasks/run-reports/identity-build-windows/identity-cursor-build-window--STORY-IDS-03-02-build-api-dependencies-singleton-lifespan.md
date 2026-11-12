---
generated_utc: 2026-05-29T14:44:31Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000004-20260529-epic-ids-03-dependency-injection.yaml
window_mode: story_key
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project identity --write-build-window --story-key STORY-IDS-03-02-build-api-dependencies-singleton-lifespan
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## STORY-IDS-03-02-build-api-dependencies-singleton-lifespan
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-02-build-api-dependencies-singleton-lifespan/task-ids-03-02-t01-build-api-dependencies-factory/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-02-build-api-dependencies-singleton-lifespan/task-ids-03-02-t02-asgi-singleton-lifespan-integration/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-03-dependency-injection/stories/STORY-IDS-03-02-build-api-dependencies-singleton-lifespan/task-ids-03-02-t03-singleton-behavior-verification/README.md`

