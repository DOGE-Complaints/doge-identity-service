## Task workspace — `task-ids-16-02-t01-check-env-source`

- Story: [`../STORY-IDS-REQ9-02-check-env-required.md`](../STORY-IDS-REQ9-02-check-env-required.md)
- Prerequisite: REQ9-01 🟢 Done (pkg-000053)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000054`  
**Skill declared:** devops-engineer  
**Decision Ref:** [`../../../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md`](../../../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md) (Scope #1–2; AC-IDS-REQ902-01/02; TODO-DEP-01…03)  
---

## Task: implement — require shell-source `./.env` on `make check-env`

### Цель
Remove optional `if [ -f ./.env ]` on `check-env`; use the **exact** post-REQ9-01 `serve`/`dev` stanza (`set -a && . ./.env && set +a`). Fail closed if absent. Keep print/diagnostic target (no new env keys). Comment must not claim optional load.

### Почему это важно
AC-IDS-REQ902-01/02 — one Make ritual; no divergence from serve/dev.

### Факты из кода
1. Post-01 `serve`/`dev`: [`Makefile:4-11`](../../../../../../../Makefile) — `set -a && . ./.env && set +a && \`.
2. `check-env` still optional: [`Makefile:14-15`](../../../../../../../Makefile) — `@if [ -f ./.env ]; then …; fi`.
3. Hard dep Done: pipeline REQ9-01 Meta 🟢 pkg-000053.

### Gap / Проблема
`check-env` still optional while serve/dev require `.env`.

### AC/DoD
- [x] (P0) `make check-env` sources `./.env` without `if [ -f ./.env ]` (fail if missing).
- [x] (P0) Shell pattern matches post-01 `serve`/`dev`: `set -a && . ./.env && set +a`.
- [x] (P1) Printed env keys unchanged unless needed for truthfulness after source.
- [x] (P1) No edits to `serve`/`dev`/runbook (REQ9-01 owned).
- [x] (P1) Header/comment does not claim optional `.env` load (TODO-DEP-03).

### Где менять код
- `doge-identity-service/Makefile` (`check-env` only)

### Out of scope
- Story gate (t02); REQ9-01 product surface; new env keys

### Проверка
```bash
rg -n 'check-env:|serve:|dev:|if \[ -f \./\.env \]|set -a && \. \./\.env' doge-identity-service/Makefile
# empty-dir: make check-env → ./.env: No such file or directory
```
