## Task workspace — `task-ids-11-03-t07-story-acceptance-verification`

- Story: [`../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000033`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md); [`story-acceptance-gate-template.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-OAUTH-03 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim (6 checkboxes): migration, Supabase stores, DI backend, durability, stateless JWT, offline tests.

### Почему это важно
Story gate для pkg-000033; разблокирует OAUTH-04 verify-gate intake.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../STORY-IDS-OAUTH-03-persistent-token-store-supabase.md) (6 checkboxes verbatim).
2. Tasks t01–t06 — implementation + tests.
3. Backlog SSOT — [`STORY-IDS-OAUTH-03-persistent-token-store-supabase.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-03-persistent-token-store-supabase.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [x] (P0) Story AC #1: migration tables + TTL index + single-use — evidence t01, t05.
- [x] (P0) Story AC #2: `SupabaseOAuthTokenService` + request-state; TTL/consumed in DB — evidence t02, t03, t05.
- [x] (P0) Story AC #3: `DB_BACKEND=supabase` vs `in_memory` — evidence t04, t05, t06.
- [x] (P0) Story AC #4: durability redeploy test — evidence t06.
- [x] (P0) Story AC #5: access token valid after store recreate without DB — evidence t06.
- [x] (P0) Story AC #6: offline tests + `test_supabase_migrations_sql` — evidence t05.
- [x] (P1) `acceptance-verification-task-ids-11-03-t07-story-acceptance-verification.md` создан с PASS (P3 gate; `--print-utc-now` for Date).
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 3; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-03-persistent-token-store-supabase/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-11-oauth-server/EPIC-IDS-11-oauth-server.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- Runtime-docs bulk sync (optional post-audit)
- Backlog file deletion
- OAUTH-04

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```
