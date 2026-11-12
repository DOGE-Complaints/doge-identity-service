## Task workspace — `task-ids-16-02-t02-story-gate`

- Story: [`../STORY-IDS-REQ9-02-check-env-required.md`](../STORY-IDS-REQ9-02-check-env-required.md)
- Prerequisite: [`t01`](../task-ids-16-02-t01-check-env-source/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000054`  
**Skill declared:** devops-engineer  
**Decision Ref:** [`../../../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md`](../../../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md); [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-REQ9-02 parent acceptance criteria

### Цель
Story gate — закрыть AC-IDS-REQ902-01…03; cite REQ9-01 Done evidence (dep); sync epic/bullrun/backlog INDEX (P3).

### Почему это важно
Завершает pkg-000054 / EPIC-IDS-16 REQ9-02; closes package check-env parity.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-REQ9-02-check-env-required.md`](../STORY-IDS-REQ9-02-check-env-required.md).
2. Hard dep evidence — [`../STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md`](../STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md) Meta 🟢; [`Makefile:4-11`](../../../../../../../Makefile).
3. Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md).

### Gap / Проблема
Parent AC всё ещё `[ ]` до t01 + gate (P3). Не ставить Done в P1.

### AC/DoD
- [x] (P0) AC-IDS-REQ902-01 — evidence t01 (required `.env` on check-env).
- [x] (P0) AC-IDS-REQ902-02 — pattern matches serve/dev — evidence t01.
- [x] (P0) AC-IDS-REQ902-03 — REQ9-01 Done cited in acceptance (pipeline Meta 🟢 / Makefile serve/dev).
- [x] (P1) `acceptance-verification-task-ids-16-02-t02-story-gate.md` PASS (`--print-utc-now` at P3).
- [x] (P1) Pipeline Meta 🟢 Done; epic §REQ9-02; bullrun + INDEX sync.

### Где менять код
- Docs/index sync only at gate

### Out of scope
- Implementing t01; P4 audit

### Проверка
```bash
rg -n 'check-env:|if \[ -f \./\.env \]|set -a && \. \./\.env' doge-identity-service/Makefile
rg -n 'Status:|P3 Done|pkg-000053' doge-identity-service/docs/tasks/epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md
```
