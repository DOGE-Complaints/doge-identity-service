## Task workspace — `task-ids-12-05-t05-story-acceptance-verification`

- Story: [`../STORY-IDS-SEC-04-service-role-isolation.md`](../STORY-IDS-SEC-04-service-role-isolation.md)
- Prerequisite: [`task-ids-12-05-t01-service-role-boundary-docs-sync`](../task-ids-12-05-t01-service-role-boundary-docs-sync/README.md), [`task-ids-12-05-t02-no-expose-service-role-guard-tests`](../task-ids-12-05-t02-no-expose-service-role-guard-tests/README.md), [`task-ids-12-05-t03-service-role-rotation-runbook`](../task-ids-12-05-t03-service-role-rotation-runbook/README.md), [`task-ids-12-05-t04-spa-sec-01-coordination-checklist`](../task-ids-12-05-t04-spa-sec-01-coordination-checklist/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000043`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md); [`story-acceptance-gate-template.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-SEC-04 parent acceptance criteria

### Цель
Story gate — закрыть все 4 parent AC verbatim; sync epic/bullrun/backlog INDEX.

### Почему это важно
Завершает pkg-000043 wave; фиксирует service_role boundary как проверяемый NFR.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-SEC-04-service-role-isolation.md`](../STORY-IDS-SEC-04-service-role-isolation.md).
2. Tasks t01–t04 — docs, no-expose tests, runbook, spa checklist.
3. Backlog source — [`STORY-IDS-SEC-04-service-role-isolation.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md).

### Gap / Проблема
Story parent AC всё ещё `[ ]` до финальной сверки gates t01–t04.

### AC/DoD
- [x] (P0) Story AC #1: boundary docs — evidence t01.
- [x] (P0) Story AC #2: no-expose — evidence t02 (`pytest` + grep gate).
- [x] (P0) Story AC #3: rotation runbook — evidence t03.
- [x] (P0) Story AC #4: spa SEC-01 coordination — evidence t04.
- [x] (P0) `.venv/bin/python -m pytest -q -m "not live_integration"` green.
- [x] (P1) `acceptance-verification-task-ids-12-05-t05-story-acceptance-verification.md` PASS (`--print-utc-now` for Date at P3 only).
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 5; bullrun + backlog INDEX sync.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-04-service-role-isolation/` (acceptance doc at P3)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/EPIC-IDS-12-security-hardening.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- SEC-05 auth credential ADR
- Spa SEC-01 implementation

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -q -m "not live_integration"
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
