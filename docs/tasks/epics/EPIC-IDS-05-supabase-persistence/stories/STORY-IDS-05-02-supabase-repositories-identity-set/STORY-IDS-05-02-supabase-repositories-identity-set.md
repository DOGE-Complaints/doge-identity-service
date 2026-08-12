# STORY-IDS-05-02: Supabase-репозитории (identity-набор)

## Meta
- Key: `STORY-IDS-05-02-supabase-repositories-identity-set`
- Parent Epic: [`../../../EPIC-IDS-05-supabase-persistence.md`](../../../EPIC-IDS-05-supabase-persistence.md)
- Type: Technical Story (Supabase Infrastructure)
- Status: Done
- Decision Ref: [`../../../EPIC-IDS-05-supabase-persistence.md`](../../../EPIC-IDS-05-supabase-persistence.md) §6 Story 2

## Story Goal
Supabase-реализации Protocols из EPIC-IDS-04 в `db_supabase.py`: Profile, VerificationSession, Audit, OAuth, StoryDraft, HealthRepository + `_jsonb_normalize`.

## AC / DoD (из EPIC-IDS-05 §6 Story 2)
- [x] `SupabaseProfileRepository(db).get_by_supabase_user_id("u1")` — GET с `eq.u1&limit=1`; пустой результат → `None`.
- [x] `SupabaseProfileRepository(db).attach_eid_verification(...)` с уже занятым `verified_person_hash` → доменная ошибка conflict (не bare httpx exception).
- [x] `SupabaseVerificationSessionStore.create(session)` — body содержит `provider`, `provider_session_data` (даже пустой `{}`).
- [x] `SupabaseEIDAuditLogRepository.log_event(event)` идемпотентен на app-уровне: повторный вызов с тем же event объектом не падает (audit append-only).
- [x] `SupabaseHealthRepository(db).ping()` делегирует на `db.healthcheck()`; `isinstance(SupabaseHealthRepository(db), HealthRepository)` — True (runtime Protocol check из EPIC-IDS-04).
- [x] JSONB поля при чтении — всегда `dict` (или `list`), никогда `str`.

## Nested tasks
| Order | Task folder | Wave |
|---|---|---|
| 1 | [`task-ids-05-02-t01-profile-and-verification-session-repos`](./task-ids-05-02-t01-profile-and-verification-session-repos/README.md) | pkg-000006 |
| 2 | [`task-ids-05-02-t02-audit-oauth-story-health-repos`](./task-ids-05-02-t02-audit-oauth-story-health-repos/README.md) | pkg-000006 |
| 3 | [`task-ids-05-02-t03-story2-acceptance-verification`](./task-ids-05-02-t03-story2-acceptance-verification/README.md) | pkg-000006 |

## Re-audit gap overlay (2026-06-02)

Source: [`../../re-audit-report-2026-06-02.md`](../../re-audit-report-2026-06-02.md) · activation: `run_mode=epic_ids_05_reaudit_2026_06_02` · pkg: [`pkg-000007`](../../../../identity-active-packages/pkg-000007-20260602-epic-ids-05-reaudit-gaps.yaml)

| Gap ID | Task folder | Status |
|--------|-------------|--------|
| S2-1 | [`task-ids-05-02-t04-audit-s2-1-oauth-store-env-doc`](./task-ids-05-02-t04-audit-s2-1-oauth-store-env-doc/README.md) | 🟢 Done |
| S2-2 | [`task-ids-05-02-t05-audit-s2-2-mark-consumed-started-guard`](./task-ids-05-02-t05-audit-s2-2-mark-consumed-started-guard/README.md) | 🟢 Done |
