---
generated_utc: 2026-05-29T10:52:39Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000003-20260528-epic-ids-02-fastapi-transport.yaml
window_mode: flat_slice
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/builder-queue/builder_resolve_queue.py --project identity --write-build-window --window-flat-start 1 --window-flat-end 14
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## Плоский срез 1–14 (как в --list)
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-01-response-envelope-error-trace-id/task-ids-02-01-t01-envelope-core/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-01-response-envelope-error-trace-id/task-ids-02-01-t02-idempotency-key-resolver/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-01-response-envelope-error-trace-id/task-ids-02-01-t03-envelope-acceptance-tests/README.md`
4. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-02-logging-setup/task-ids-02-02-t01-configure-logging-runtime/README.md`
5. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-02-logging-setup/task-ids-02-02-t02-logging-verification/README.md`
6. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-03-auth-security-primitives-bearer-stub/task-ids-02-03-t01-unauthorized-error-and-protocol/README.md`
7. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-03-auth-security-primitives-bearer-stub/task-ids-02-03-t02-stub-bearer-auth-and-current-user/README.md`
8. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-03-auth-security-primitives-bearer-stub/task-ids-02-03-t03-auth-primitives-verification/README.md`
9. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware/task-ids-02-04-t01-create-app-and-lifespan/README.md`
10. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware/task-ids-02-04-t02-runtime-middleware-and-exception-handlers/README.md`
11. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-04-fastapi-app-lifespan-cors-middleware/task-ids-02-04-t03-api-dependencies-cache-hooks/README.md`
12. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-05-routes-contract-health-ready-identity-stubs/task-ids-02-05-t01-health-and-readiness-handlers/README.md`
13. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-05-routes-contract-health-ready-identity-stubs/task-ids-02-05-t02-identity-route-contract-stubs/README.md`
14. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-02-fastapi-transport/stories/STORY-IDS-02-05-routes-contract-health-ready-identity-stubs/task-ids-02-05-t03-options-preflight-contract/README.md`

