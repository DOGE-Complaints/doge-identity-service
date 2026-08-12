# STORY-IDS-01-03: Кастомный dotenv-парсер

## Meta
- Key: `STORY-IDS-01-03-custom-dotenv-parser`
- Parent Epic: [`../../../EPIC-IDS-01-scaffold-config-launch.md`](../../../EPIC-IDS-01-scaffold-config-launch.md)
- Type: Technical Story (NFR / Infrastructure)
- Status: Implemented (Waiting Acceptance)
- Depends on: STORY-IDS-01-02
- Decision Ref: [`../../../../../requirements/06-technical-scaffold.md`](../../../../../requirements/06-technical-scaffold.md) §Шаг 2 (no python-dotenv); [`../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md`](../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md) §Story 3
- Operative queue: [`../../../../identity-active-packages/pkg-000001-20260527-epic-ids-01-scaffold.yaml`](../../../../identity-active-packages/pkg-000001-20260527-epic-ids-01-scaffold.yaml)

## Story Goal
Копия паттерна complaints-gateway: `env_file.py` + `provide_app_config`; shell env приоритетнее `.env`; default `API_BASE_URL=http://localhost:8100`.

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-ids-01-03-t01-env-file-merge`](./task-ids-01-03-t01-env-file-merge/README.md) | pkg-000001 |
| 2 | [`task-ids-01-03-t02-provide-app-config`](./task-ids-01-03-t02-provide-app-config/README.md) | pkg-000001 |
| 3 | [`task-ids-01-03-t03-dotenv-parser-tests`](./task-ids-01-03-t03-dotenv-parser-tests/README.md) | pkg-000001 |
| 4 | [`task-ids-01-03-t04-audit-f3-1-parse-dotenv-file-test`](./task-ids-01-03-t04-audit-f3-1-parse-dotenv-file-test/README.md) | override epic_ids_01_audit_2026_05_28 |

## AC / DoD (story level)
- [x] Shell priority: ключ из `priority` не перезаписывается `.env`
- [x] Комментарии/пустые строки игнорируются; кавычки снимаются
- [x] `provide_app_config({...})` работает без файла `.env`
