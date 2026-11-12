## Task workspace — `task-ids-16-01-t03-story-gate`

- Story: [`../STORY-IDS-REQ9-01-make-env-required.md`](../STORY-IDS-REQ9-01-make-env-required.md)
- Prerequisite: [`t01`](../task-ids-16-01-t01-makefile-serve-dev/README.md) · [`t02`](../task-ids-16-01-t02-env-example-runbook/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000053`  
**Skill declared:** devops-engineer  
**Decision Ref:** [`../../../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md`](../../../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md); [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-REQ9-01 parent acceptance criteria

### Цель
Story gate — закрыть AC-IDS-REQ901-01…04; sync epic/bullrun/backlog INDEX (P3).

### Почему это важно
Завершает pkg-000053 / EPIC-IDS-16 wave for REQ9-01 (unblocks REQ9-02).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-REQ9-01-make-env-required.md`](../STORY-IDS-REQ9-01-make-env-required.md).
2. Backlog source — [`STORY-IDS-REQ9-01-make-env-required.md`](../../../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md).
3. Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md).

### Gap / Проблема
Parent AC всё ещё `[ ]` до сверки t01–t02 (P3). Не ставить Done в P1.

### AC/DoD
- [x] (P0) AC-IDS-REQ901-01 — evidence t01 (required `.env` on serve/dev).
- [x] (P0) AC-IDS-REQ901-02 — probes `/health` `/ready` still registered (no rename).
- [x] (P0) AC-IDS-REQ901-03 — `SERVICE_API_TOKEN` unchanged — evidence t02.
- [x] (P0) AC-IDS-REQ901-04 — `API_BASE_URL`/`PORT` + runbook required wording — evidence t02.
- [x] (P1) `acceptance-verification-task-ids-16-01-t03-story-gate.md` PASS (`--print-utc-now` for Date at P3 only).
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story REQ9-01; bullrun + package INDEX + root backlog INDEX.

### Где менять код
- Docs/index sync only at gate

### Out of scope
- Implementing t01–t02; REQ9-02; P4 audit

### Проверка
```bash
rg -n 'if \[ -f \./\.env \]|set -a && \. \./\.env' doge-identity-service/Makefile
rg -n 'SERVICE_API_TOKEN|/health|/ready' doge-identity-service/.env.example doge-identity-service/src/core/api/asgi_app.py
rg -n 'required|\.env|подхватывает' doge-identity-service/docs/runbook/run-and-healthcheck.md
```
