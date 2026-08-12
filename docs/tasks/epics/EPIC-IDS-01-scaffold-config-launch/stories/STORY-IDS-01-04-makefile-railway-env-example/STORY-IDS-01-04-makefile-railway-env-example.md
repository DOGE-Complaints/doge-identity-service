# STORY-IDS-01-04: Makefile, Railway-конфиг, `.env.example`

## Meta
- Key: `STORY-IDS-01-04-makefile-railway-env-example`
- Parent Epic: [`../../../EPIC-IDS-01-scaffold-config-launch.md`](../../../EPIC-IDS-01-scaffold-config-launch.md)
- Type: Technical Story (NFR / Infrastructure)
- Status: Implemented (Waiting Acceptance)
- Depends on: STORY-IDS-01-01 (Makefile targets), STORY-IDS-01-03 (`.env` load pattern)
- Decision Ref: [`../../../../../requirements/06-technical-scaffold.md`](../../../../../requirements/06-technical-scaffold.md) §Шаг 4; [`../../../../../requirements/07-env-configuration-spec.md`](../../../../../requirements/07-env-configuration-spec.md); оператор P1: **`.env.example`** (не `example.env`)
- Operative queue: [`../../../../identity-active-packages/pkg-000001-20260527-epic-ids-01-scaffold.yaml`](../../../../identity-active-packages/pkg-000001-20260527-epic-ids-01-scaffold.yaml)

## Story Goal
`make serve`/`dev`/`check-env`/`test`/`test-live`, `railpack.json` для Railway, полный `.env.example` для identity vars.

## Out of scope
- Рабочий HTTP `/health` — EPIC-IDS-02 (`make serve` может `ImportError` на `core.api.asgi_app` — ожидаемо)

## Nested tasks

| Order | Task folder | Wave |
|-------|-------------|------|
| 1 | [`task-ids-01-04-t01-makefile-targets`](./task-ids-01-04-t01-makefile-targets/README.md) | pkg-000001 |
| 2 | [`task-ids-01-04-t02-railpack-json`](./task-ids-01-04-t02-railpack-json/README.md) | pkg-000001 |
| 3 | [`task-ids-01-04-t03-env-example`](./task-ids-01-04-t03-env-example/README.md) | pkg-000001 |
| 4 | [`task-ids-01-04-t04-audit-f4-1-test-live-flags-cleanup`](./task-ids-01-04-t04-audit-f4-1-test-live-flags-cleanup/README.md) | override epic_ids_01_audit_2026_05_28 |
| 5 | [`task-ids-01-04-t05-audit-f4-2-dotenv-secret-section-placement`](./task-ids-01-04-t05-audit-f4-2-dotenv-secret-section-placement/README.md) | override epic_ids_01_audit_2026_05_28 |

## AC / DoD (story level)
- [x] `make check-env` печатает identity-vars (включая `SUPABASE_JWT_SECRET`, `EID_PROVIDER`)
- [x] `railpack.json` валиден; `${PORT:-8100}`, `--app-dir src`
- [x] `.env.example` покрывает req-07 + req-17/18 (`EID_PROVIDER=mock`)
