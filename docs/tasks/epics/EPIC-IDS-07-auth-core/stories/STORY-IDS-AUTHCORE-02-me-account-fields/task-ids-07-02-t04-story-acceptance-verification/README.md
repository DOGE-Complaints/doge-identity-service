## Task workspace — `task-ids-07-02-t04-story-acceptance-verification`

- Story: [`../STORY-IDS-AUTHCORE-02-me-account-fields.md`](../STORY-IDS-AUTHCORE-02-me-account-fields.md)
- Prerequisite: [`task-ids-07-02-t01-me-response-created-at-account-status`](../task-ids-07-02-t01-me-response-created-at-account-status/README.md), [`task-ids-07-02-t02-me-api-docs-created-at-account-status`](../task-ids-07-02-t02-me-api-docs-created-at-account-status/README.md), [`task-ids-07-02-t03-me-profile-offline-tests-account-fields`](../task-ids-07-02-t03-me-profile-offline-tests-account-fields/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000044`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md`](../../../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md); [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-AUTHCORE-02 parent acceptance criteria

### Цель
Story gate — закрыть все 5 parent AC verbatim; sync epic/bullrun/backlog INDEX; dashboard Remaining после Done (P3).

### Почему это важно
Завершает pkg-000044 wave; фиксирует CAB-02 identity-поля в `/me` как проверяемый контракт.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-AUTHCORE-02-me-account-fields.md`](../STORY-IDS-AUTHCORE-02-me-account-fields.md).
2. Tasks t01–t03 — me_response, API docs, offline tests.
3. Backlog source — [`STORY-IDS-AUTHCORE-02-me-account-fields.md`](../../../../../../backlog-stories/auth-core/STORY-IDS-AUTHCORE-02-me-account-fields.md).

### Gap / Проблема
Story parent AC всё ещё `[ ]` до финальной сверки gates t01–t03.

### AC/DoD
- [x] (P0) Story AC #1: `account_status == "active"` always — evidence t01+t03.
- [x] (P0) Story AC #2: `created_at` ISO/null; no Auth; no DB write — evidence t01+t03.
- [x] (P0) Story AC #3: no migration — `grep account_status supabase/bootstrap/` empty — evidence t01 DoD.
- [x] (P0) Story AC #4: openapi + API_REFERENCE — evidence t02.
- [x] (P0) Story AC #5: `test_me_profile` + offline suite green — evidence t03.
- [x] (P0) `.venv/bin/python -m pytest -q -m "not live_integration"` green.
- [x] (P1) `acceptance-verification-task-ids-07-02-t04-story-acceptance-verification.md` PASS (`--print-utc-now` for Date at P3 only).
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 2; bullrun + backlog INDEX sync; identity-mvp-dashboard Remaining refresh at Done.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-07-auth-core/stories/STORY-IDS-AUTHCORE-02-me-account-fields/` (acceptance doc at P3)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-07-auth-core/EPIC-IDS-07-auth-core.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`
- `doge-identity-service/docs/tasks/identity-mvp-dashboard.md` (Remaining — at P3 Done)

### Out of scope
- Spa CAB-api §0 note (backlog T04)
- ONB-01 email materialize/execute

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -q -m "not live_integration"
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
