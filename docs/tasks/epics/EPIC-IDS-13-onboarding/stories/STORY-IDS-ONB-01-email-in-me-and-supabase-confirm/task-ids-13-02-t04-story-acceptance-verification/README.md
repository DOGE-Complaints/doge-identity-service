## Task workspace — `task-ids-13-02-t04-story-acceptance-verification`

- Story: [`../STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md`](../STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md)
- Prerequisite: [`task-ids-13-02-t01-me-response-email-and-email-verified`](../task-ids-13-02-t01-me-response-email-and-email-verified/README.md), [`task-ids-13-02-t02-confirm-email-runbook-and-me-api-docs`](../task-ids-13-02-t02-confirm-email-runbook-and-me-api-docs/README.md), [`task-ids-13-02-t03-me-profile-offline-tests-email-fields`](../task-ids-13-02-t03-me-profile-offline-tests-email-fields/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000045`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md`](../../../../../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md); [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-ONB-01 parent acceptance criteria

### Цель
Story gate — закрыть все 5 parent AC verbatim; sync epic/bullrun/backlog INDEX; dashboard Remaining после Done (P3).

### Почему это важно
Завершает pkg-000045; закрывает CAB-02 identity 3/3 (`email` + AUTHCORE-02 fields).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md`](../STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md).
2. Tasks t01–t03 — me_response, runbook+API docs, offline tests.
3. Backlog source — [`STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md`](../../../../../../backlog-stories/identity-onboarding/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm.md).

### Gap / Проблема
Story parent AC всё ещё `[ ]` до финальной сверки gates t01–t03.

### AC/DoD
- [x] (P0) Story AC #1: `email` from token / null — evidence t01+t03.
- [x] (P0) Story AC #2: `email_verified: true` — evidence t01+t03.
- [x] (P0) Story AC #3: Confirm email in runbook — evidence t02.
- [x] (P0) Story AC #4: openapi + API_REFERENCE — evidence t02.
- [x] (P0) Story AC #5: test_me_profile + offline; AUTHCORE-02 intact — evidence t03.
- [x] (P0) `.venv/bin/python -m pytest -q -m "not live_integration"` green.
- [x] (P1) `acceptance-verification-task-ids-13-02-t04-story-acceptance-verification.md` PASS (`--print-utc-now` for Date at P3 only).
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 2; bullrun + backlog INDEX; identity-mvp-dashboard Remaining at Done.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-13-onboarding/stories/STORY-IDS-ONB-01-email-in-me-and-supabase-confirm/` (acceptance doc at P3)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-13-onboarding/EPIC-IDS-13-onboarding.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`
- `doge-identity-service/docs/tasks/identity-mvp-dashboard.md` (Remaining — at P3 Done)

### Out of scope
- Spa CAB-api note; hard email gate

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -q -m "not live_integration"
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
