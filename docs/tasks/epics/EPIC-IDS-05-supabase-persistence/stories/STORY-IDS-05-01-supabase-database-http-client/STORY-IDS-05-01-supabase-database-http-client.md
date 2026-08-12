# STORY-IDS-05-01: `SupabaseDatabase` HTTP-клиент

## Meta
- Key: `STORY-IDS-05-01-supabase-database-http-client`
- Parent Epic: [`../../../EPIC-IDS-05-supabase-persistence.md`](../../../EPIC-IDS-05-supabase-persistence.md)
- Type: Technical Story (Supabase Infrastructure)
- Status: Done
- Decision Ref: [`../../../EPIC-IDS-05-supabase-persistence.md`](../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 1

## Story Goal
PostgREST HTTP-клиент `SupabaseDatabase` через httpx без Supabase SDK: `from_http`, `_headers`, `_request`, PostgREST filter docstring.

## AC / DoD (из EPIC-IDS-05 §6 Story 1)
- [x] `SupabaseDatabase.from_http("", "key")` → `ValueError`.
- [x] `SupabaseDatabase.from_http("https://x.co/", "key").base_url == "https://x.co"` (без trailing slash).
- [x] `_headers()["apikey"] == _headers()["Authorization"].split()[-1]` (одинаковое значение).
- [x] `_request` при HTTP 5xx логирует через `logger.error` и пробрасывает `httpx.HTTPError`.

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-05-01-t01-supabase-database-http-client`](./task-ids-05-01-t01-supabase-database-http-client/README.md) | pkg-000006 |
| 2 | [`task-ids-05-01-t02-story1-acceptance-verification`](./task-ids-05-01-t02-story1-acceptance-verification/README.md) | pkg-000006 |

## Re-audit gap overlay (2026-06-02)

Source: [`../../re-audit-report-2026-06-02.md`](../../re-audit-report-2026-06-02.md) · activation: `run_mode=epic_ids_05_reaudit_2026_06_02` · pkg: [`pkg-000007`](../../../../identity-active-packages/pkg-000007-20260602-epic-ids-05-reaudit-gaps.yaml)

| Gap ID | Task folder | Status |
|--------|-------------|--------|
| S1-1 | [`task-ids-05-01-t03-audit-s1-1-empty-service-role-key-test`](./task-ids-05-01-t03-audit-s1-1-empty-service-role-key-test/README.md) | 🟢 Done |
