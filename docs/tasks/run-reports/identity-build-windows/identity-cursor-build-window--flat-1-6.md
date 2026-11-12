---
generated_utc: 2026-06-26T12:47:12Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000038-20260626-epic-ids-12-sec-03-jwt-validation-hardening.yaml
window_mode: flat_slice
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --write-build-window --window-flat-start 1 --window-flat-end 6
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## Плоский срез 1–6 (как в --list)
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/task-ids-12-04-t01-live-supabase-jwt-aud-decision-record/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/task-ids-12-04-t02-confirm-octkey-import-form-live-token/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/task-ids-12-04-t03-aud-claim-registry-or-spec-waiver/README.md`
4. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/task-ids-12-04-t04-offline-jwt-aud-key-regression-tests/README.md`
5. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/task-ids-12-04-t05-spec-09-g5-gap-closure-docs/README.md`
6. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/task-ids-12-04-t06-story-acceptance-verification/README.md`

