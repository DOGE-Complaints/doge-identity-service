---
generated_utc: 2026-06-28T17:44:42Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000041-20260628-epic-ids-10-pv-10-file-sms-sink-dev.yaml
window_mode: flat_slice
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --write-build-window --window-flat-start 1 --window-flat-end 7
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## Плоский срез 1–7 (как в --list)
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t01-file-sms-sender-core/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t02-file-sms-config-spec/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t03-file-descriptor-registry-runtime/README.md`
4. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t04-pilot-file-provider-fail-fast/README.md`
5. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t05-dev-hygiene-gitignore-env-example/README.md`
6. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t06-offline-file-sms-tests/README.md`
7. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/task-ids-10-10-t07-story-acceptance-verification/README.md`

