---
generated_utc: 2026-07-04T10:31:23Z
builder_project: identity
identity_input_package: doge-identity-service/docs/tasks/identity-active-packages/pkg-000042-20260704-epic-ids-12-sec-06-jwks-es256-hardening.yaml
window_mode: flat_slice
artifact_kind: identity_cursor_build_window
pkg_schema_version: 1
---

# Identity Cursor build window

**Не SSOT.** Очередь и порядок задаёт только YAML-пакет в `identity_input_package`. Не менять список `@…README.md` вручную — перегенерируйте файл командой ниже.

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --write-build-window --window-flat-start 1 --window-flat-end 8
```

Исполнение: [`ids-epic-execution-pipeline.md`](../../ids-epic-execution-pipeline.md) + `@.cursor/commands/bullrun-start.md` / `run-task.md`.

## Плоский срез 1–8 (как в --list)
1. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t01-change-propagation-audit/README.md`
2. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t02-jwks-only-validator/README.md`
3. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t03-jwks-cache-di-wiring/README.md`
4. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t04-remove-supabase-jwt-secret/README.md`
5. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t05-es256-mock-jwks-test-harness/README.md`
6. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t06-offline-jwks-validator-tests/README.md`
7. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t07-jwks-only-docs-sync/README.md`
8. `@doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-06-supabase-jwks-es256-hardening/task-ids-12-06-t08-story-acceptance-verification/README.md`

