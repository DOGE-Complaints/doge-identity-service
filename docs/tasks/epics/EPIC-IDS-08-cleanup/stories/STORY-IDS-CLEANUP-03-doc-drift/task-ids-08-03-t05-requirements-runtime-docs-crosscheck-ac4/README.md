## Task workspace — `task-ids-08-03-t05-requirements-runtime-docs-crosscheck-ac4`

- Story: [`../STORY-IDS-CLEANUP-03-doc-drift.md`](../STORY-IDS-CLEANUP-03-doc-drift.md)
- Decision Ref: [`../../../../../../backlog-stories/STORY-IDS-CLEANUP-03-doc-drift.md`](../../../../../../backlog-stories/cleanup/STORY-IDS-CLEANUP-03-doc-drift.md) AC #4; [`../../../../../../runtime-docs/`](../../../../../../runtime-docs/)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000014`  
**Skill declared:** python-pro  
---

## Task: fix/docs — requirements vs runtime-docs cross-check (AC#4)

### Цель
Устранить противоречия между requirements (post t01–t04) и [`runtime-docs/`](../../../../../../../docs/runtime-docs/) — story scope, migrations, routes, `/ready` facts.

### Почему это важно
Story AC #4; runtime-docs — onboarding SSOT alongside requirements; stale paragraphs mislead after CLEANUP-01/02.

### Факты из кода
1. [`02-data-bootstrap.md:49`](../../../../../../../docs/runtime-docs/02-data-bootstrap.md) — claims `story_drafts` in `/ready` required tables; [`db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py) — `grep story_drafts` = **0**.
2. [`01-api.md:40`](../../../../../../../docs/runtime-docs/01-api.md) — references story routes at `asgi_app.py:258-310`; `grep story-drafts asgi_app.py` = **0**.
3. [`05-data-model.md:58`](../../../../../../../docs/runtime-docs/05-data-model.md) — describes live `story_drafts` code/model (post CLEANUP-01 removed from `src/`).
4. [`02-data-bootstrap.md:33`](../../../../../../../docs/runtime-docs/02-data-bootstrap.md) — DOC-3 note may be removable after t01 updates req-08.

### Gap / Проблема
Runtime-docs contain stale SB-1/SB-2 narratives contradicting current code and updated requirements.

### AC/DoD
- [x] (P0) Story AC #4: no contradictions between requirements and runtime-docs on migrations count, callback routes, story scope.
- [x] (P0) Update stale paragraphs in [`02-data-bootstrap.md`](../../../../../../../docs/runtime-docs/02-data-bootstrap.md), [`01-api.md`](../../../../../../../docs/runtime-docs/01-api.md), and [`05-data-model.md`](../../../../../../../docs/runtime-docs/05-data-model.md) as needed.
- [x] (P0) No broken internal links to removed modules/routes.
- [x] (P1) Optional: align [`07-env-configuration-spec.md`](../../../../../../../docs/requirements/07-env-configuration-spec.md) redirect URI if still contradicts `.env.example` (CFG-3 consistency).
- [x] (P1) BULLRUN-PHASE-LOG + acceptance-verification в этой папке (P3).

### Где менять код
- [`docs/runtime-docs/02-data-bootstrap.md`](../../../../../../../docs/runtime-docs/02-data-bootstrap.md)
- [`docs/runtime-docs/01-api.md`](../../../../../../../docs/runtime-docs/01-api.md)
- [`docs/runtime-docs/05-data-model.md`](../../../../../../../docs/runtime-docs/05-data-model.md)
- Optionally [`docs/requirements/07-env-configuration-spec.md`](../../../../../../../docs/requirements/07-env-configuration-spec.md)

### Out of scope
- `src/` code changes
- Full rewrite of all runtime-docs (only contradiction fixes)
- Epic gate EPIC-IDS-08

### Проверка
```bash
cd doge-identity-service
grep -rn "story_drafts\|story-drafts" docs/runtime-docs/ docs/requirements/
grep -rn "eid/callback" docs/runtime-docs/ docs/requirements/ .env.example
grep -rn "3 миграц" docs/runtime-docs/ docs/requirements/
```
