---
generated_utc: 2026-07-09T19:36:29Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000043-20260709-epic-ids-12-sec-04-service-role-isolation.yaml
window_mode: flat_slice
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --write-build-window --window-flat-start 1 --window-flat-end 5
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## Плоский срез 1–5 (как в --list)
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t01-service-role-boundary-docs-sync/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t02-no-expose-service-role-guard-tests/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t03-service-role-rotation-runbook/README.md`
4. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t04-spa-sec-01-coordination-checklist/README.md`
5. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/task-ids-12-05-t05-story-acceptance-verification/README.md`

