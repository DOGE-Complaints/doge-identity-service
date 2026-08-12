# STORY-IDS-01-01: Инициализация пакета и зависимостей

## Meta
- Key: `STORY-IDS-01-01-init-package-and-dependencies`
- Parent Epic: [`../../../EPIC-IDS-01-scaffold-config-launch.md`](../../../EPIC-IDS-01-scaffold-config-launch.md)
- Type: Technical Story (NFR / Infrastructure)
- Status: Implemented (Waiting Acceptance)
- Decision Ref: [`../../../../../requirements/06-technical-scaffold.md`](../../../../../requirements/06-technical-scaffold.md) §Шаг 1–2; [`../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md`](../../../../../tech-requirements/impl-epic-01-scaffold-config-launch.md) §Story 1
- Operative queue: [`../../../../identity-active-packages/pkg-000001-20260527-epic-ids-01-scaffold.yaml`](../../../../identity-active-packages/pkg-000001-20260527-epic-ids-01-scaffold.yaml)

## Story Goal
Создать каркас `src/core/*`, `tests/`, `supabase/`, `pyproject.toml`, `pyrightconfig.json` и установить editable package с identity-specific deps (`joserfc`, `cryptography`).

## Scope
- T01 directory skeleton + реализованный `hashing.py`
- T02 `pyproject.toml` + `pyrightconfig.json`
- T03 `pip install -e ".[dev]"` + import/collect-only gates

## Out of scope
- `AppConfig` / dotenv (STORY-IDS-01-02, 01-03)
- FastAPI `asgi_app` (EPIC-IDS-02)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-ids-01-01-t01-package-directory-skeleton`](./task-ids-01-01-t01-package-directory-skeleton/README.md) | pkg-000001 |
| 2 | [`task-ids-01-01-t02-pyproject-and-pyright`](./task-ids-01-01-t02-pyproject-and-pyright/README.md) | pkg-000001 |
| 3 | [`task-ids-01-01-t03-editable-install-verify`](./task-ids-01-01-t03-editable-install-verify/README.md) | pkg-000001 |
| 4 | [`task-ids-01-01-t04-audit-f1-1-security-init`](./task-ids-01-01-t04-audit-f1-1-security-init/README.md) | override epic_ids_01_audit_2026_05_28 |
| 5 | [`task-ids-01-01-t05-audit-f1-2-story1-ac-collect-wording`](./task-ids-01-01-t05-audit-f1-2-story1-ac-collect-wording/README.md) | override epic_ids_01_audit_2026_05_28 |
| 6 | [`task-ids-01-01-t06-audit-f1-3-hashing-placeholder-doc-alignment`](./task-ids-01-01-t06-audit-f1-3-hashing-placeholder-doc-alignment/README.md) | override epic_ids_01_audit_2026_05_28 |
| 7 | [`task-ids-01-01-t07-audit-f1-4-dev-httpx-doc-alignment`](./task-ids-01-01-t07-audit-f1-4-dev-httpx-doc-alignment/README.md) | override epic_ids_01_audit_2026_05_28 |
| 8 | [`task-ids-01-01-t08-audit-f1-5-pyright-config-alignment`](./task-ids-01-01-t08-audit-f1-5-pyright-config-alignment/README.md) | override epic_ids_01_audit_2026_05_28 |

## AC / DoD (story level)
- [x] `python3.11 -c "import core"` — exit 0
- [x] `python3.11 -m pytest --collect-only -q` — без `ModuleNotFoundError`
- [x] `pip show doge-identity-service` — version `0.1.0`
