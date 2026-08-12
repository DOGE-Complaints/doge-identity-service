## Task workspace — `task-ids-11-02-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../STORY-IDS-OAUTH-02-introspection-and-service-token.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000030`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md); [`story-acceptance-gate-template.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-OAUTH-02 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim (4 checkboxes): introspection active/inactive, service token gate, profile-sourced `phone_verified`, offline tests + gateway contract.

### Почему это важно
Story gate для pkg-000030; разблокирует OAUTH-04 verify-gate в backlog.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../STORY-IDS-OAUTH-02-introspection-and-service-token.md) (4 checkboxes verbatim).
2. Tasks t01–t05 — implementation + tests.
3. Backlog SSOT — [`STORY-IDS-OAUTH-02-introspection-and-service-token.md`](../../../../../../backlog-stories/oauth/STORY-IDS-OAUTH-02-introspection-and-service-token.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [x] (P0) Story AC #1: valid token → `{active:true, sub, phone_verified}`; invalid → `{active:false}` — evidence t03, t04, t05.
- [x] (P0) Story AC #2: no service token → 401/403 — evidence t02, t04, t05.
- [x] (P0) Story AC #3: `phone_verified` from profile — evidence t03, t05.
- [x] (P0) Story AC #4: offline tests + gateway contract — evidence t05.
- [x] (P1) `acceptance-verification-task-ids-11-02-t06-story-acceptance-verification.md` создан с PASS.
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic Story 2; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-11-oauth-server/stories/STORY-IDS-OAUTH-02-introspection-and-service-token/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-11-oauth-server/EPIC-IDS-11-oauth-server.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- Runtime-docs bulk sync (optional post-audit)
- Backlog file deletion

### Проверка
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
cd doge-identity-service && .venv/bin/python -m pytest -m "not live_integration" -q
```
