---
generated_utc: 2026-08-20T10:23:02Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000047-20260820-epic-ids-14-smspm-02-sms-sender.yaml
window_mode: story_key
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --write-build-window --story-key STORY-IDS-SMSPM-02-sms-sender
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## STORY-IDS-SMSPM-02-sms-sender
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/task-ids-14-02-t01-smspm-sms-sender-send/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/task-ids-14-02-t02-smspm-error-mapping/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/task-ids-14-02-t03-smspm-descriptor-wire/README.md`
4. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/task-ids-14-02-t04-smspm-sender-offline-tests/README.md`
5. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/task-ids-14-02-t05-smspm-sender-live-skip-without-creds/README.md`
6. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-14-smspm/stories/STORY-IDS-SMSPM-02-sms-sender/task-ids-14-02-t06-story-acceptance-verification/README.md`

