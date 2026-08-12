# STORY-IDS-05-03: 5-уровневый healthcheck

## Meta
- Key: `STORY-IDS-05-03-five-level-healthcheck`
- Parent Epic: [`../../../EPIC-IDS-05-supabase-persistence.md`](../../../EPIC-IDS-05-supabase-persistence.md)
- Type: Technical Story (Supabase Infrastructure)
- Status: Done
- Decision Ref: [`../../../EPIC-IDS-05-supabase-persistence.md`](../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 3

## Story Goal
5-уровневый healthcheck identity-таблиц на `SupabaseDatabase` + интеграция `db_checks`/`db_ready` в `build_api_dependencies()`.

## AC / DoD (из EPIC-IDS-05 §6 Story 3)
- [x] Все 5 healthcheck-методов возвращают `bool`, никогда не raise (внутри `try/except Exception: return False`).
- [x] При сетевой ошибке → `False`.
- [x] `GET /ready` при `db_backend=supabase` + `db_ready=False` → HTTP 503, envelope `{"data": {"status": "degraded", ..., "db_checks": {...}}}`.
- [x] Startup-лог содержит `db_checks={'connectivity': True/False, ...}` (после `configure_logging`).

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-05-03-t01-supabase-database-healthcheck-methods`](./task-ids-05-03-t01-supabase-database-healthcheck-methods/README.md) | pkg-000006 |
| 2 | [`task-ids-05-03-t02-build-api-dependencies-db-checks`](./task-ids-05-03-t02-build-api-dependencies-db-checks/README.md) | pkg-000006 |
| 3 | [`task-ids-05-03-t03-story3-acceptance-verification`](./task-ids-05-03-t03-story3-acceptance-verification/README.md) | pkg-000006 |

## Re-audit gap overlay (2026-06-02)

Source: [`../../re-audit-report-2026-06-02.md`](../../re-audit-report-2026-06-02.md) · activation: `run_mode=epic_ids_05_reaudit_2026_06_02` · pkg: [`pkg-000007`](../../../../identity-active-packages/pkg-000007-20260602-epic-ids-05-reaudit-gaps.yaml)

| Gap ID | Task folder | Status |
|--------|-------------|--------|
| S3-1 | [`task-ids-05-03-t04-audit-s3-1-dual-health-db-comment`](./task-ids-05-03-t04-audit-s3-1-dual-health-db-comment/README.md) | 🟢 Done |
| S3-2 | [`task-ids-05-03-t05-audit-s3-2-health-db-request-timeout`](./task-ids-05-03-t05-audit-s3-2-health-db-request-timeout/README.md) | 🟢 Done |
