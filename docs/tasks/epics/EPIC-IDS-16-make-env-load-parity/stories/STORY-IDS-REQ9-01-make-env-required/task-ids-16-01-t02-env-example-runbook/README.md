## Task workspace — `task-ids-16-01-t02-env-example-runbook`

- Story: [`../STORY-IDS-REQ9-01-make-env-required.md`](../STORY-IDS-REQ9-01-make-env-required.md)
- Prerequisite: [`t01`](../task-ids-16-01-t01-makefile-serve-dev/README.md) (Make pattern in place or concurrent)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000053`  
**Skill declared:** devops-engineer  
**Decision Ref:** [`../../../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md`](../../../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md) (Scope #2–3; AC-IDS-REQ901-03, AC-IDS-REQ901-04)  
---

## Task: docs — unchanged env names + runbook G8 wording for Make start

### Цель
Document that `SERVICE_API_TOKEN`, `API_BASE_URL`, `PORT` names stay (Makefile comment and/or `.env.example`). Update `run-and-healthcheck.md` Make section: required `./.env` for `serve`/`dev`, not optional «подхватывает».

### Почему это важно
AC-IDS-REQ901-03/04 — ops parity docs must match G8 fail-closed start.

### Факты из кода
1. [`.env.example:9-10`](../../../../../../../.env.example) — `PORT` / `API_BASE_URL`.
2. [`.env.example:135`](../../../../../../../.env.example) — `SERVICE_API_TOKEN=`.
3. [`run-and-healthcheck.md:43`](../../../../../../runbook/run-and-healthcheck.md) — table row «подхватывает `./.env`».
4. [`run-and-healthcheck.md:35`](../../../../../../runbook/run-and-healthcheck.md) — notes auto-merge of cwd `.env` (clarify vs Make required source).

### Gap / Проблема
Runbook describes optional Make env pickup; names need explicit “unchanged” documentation for G8.

### AC/DoD
- [x] (P0) `SERVICE_API_TOKEN` still present / unchanged in `.env.example` (no rename in Makefile).
- [x] (P0) `API_BASE_URL` / `PORT` names documented as staying (comment and/or `.env.example`).
- [x] (P0) Runbook Make section states required `./.env` for `serve`/`dev` (G8).

### Где менять код
- `doge-identity-service/.env.example` (comments only if needed)
- `doge-identity-service/Makefile` (optional comment near serve/dev)
- `doge-identity-service/docs/runbook/run-and-healthcheck.md`

### Out of scope
- Make `serve`/`dev` logic (t01); `check-env` fail-closed (REQ9-02); story gate (t03)

### Проверка
```bash
rg -n 'SERVICE_API_TOKEN|API_BASE_URL|^PORT' doge-identity-service/.env.example doge-identity-service/Makefile
rg -n 'подхватывает|required|\.env|make serve|make dev' doge-identity-service/docs/runbook/run-and-healthcheck.md
```
