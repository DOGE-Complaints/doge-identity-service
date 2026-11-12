## Task workspace — `task-ids-16-01-t01-makefile-serve-dev`

- Story: [`../STORY-IDS-REQ9-01-make-env-required.md`](../STORY-IDS-REQ9-01-make-env-required.md)
- Prerequisite: —

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000053`  
**Skill declared:** devops-engineer  
**Decision Ref:** [`../../../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md`](../../../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md) (Scope #1, #4; AC-IDS-REQ901-01, AC-IDS-REQ901-02)  
---

## Task: implement — require shell-source `./.env` on `make serve` / `make dev`

### Цель
Remove optional `if [ -f ./.env ]` on `serve`/`dev`; use required `set -a && . ./.env && set +a` (gateway/threads parity). Fail closed if `.env` absent. Keep probe path registrations unchanged.

### Почему это важно
AC-IDS-REQ901-01 (G8): Make start must not silently run without env file.

### Факты из кода
1. [`Makefile:3-11`](../../../../../../../Makefile) — `serve`/`dev` wrap source in `if [ -f ./.env ]; then …; fi`.
2. [`doge-complaints-gateway/Makefile:14-22`](../../../../../../../../doge-complaints-gateway/Makefile) — required `set -a && . ./.env && set +a && \` (no `if [ -f ]`).
3. [`doge-threads/Makefile:16-22`](../../../../../../../../doge-threads/Makefile) — same required pattern.
4. Probes registered at [`asgi_app.py:288`](../../../../../../../src/core/api/asgi_app.py), `:295` — `/health`, `/ready` (no rename this task).

### Gap / Проблема
Identity `serve`/`dev` treat `.env` as optional; gateway/threads require it.

### AC/DoD
- [x] (P0) `make serve` and `make dev` source `./.env` without `if [ -f ./.env ]` (fail if missing).
- [x] (P0) Shell pattern matches gateway/threads: `set -a && . ./.env && set +a`.
- [x] (P1) `check-env` target **unchanged** this task (REQ9-02).
- [x] (P1) No rename of `/health` or `/ready` routes (AC-IDS-REQ901-02).

### Где менять код
- `doge-identity-service/Makefile` (`serve`, `dev` only)

### Out of scope
- `check-env` (t02 docs only + REQ9-02); `.env.example`/runbook wording (t02); story gate (t03)

### Проверка
```bash
rg -n 'serve:|dev:|if \[ -f \./\.env \]|set -a && \. \./\.env' doge-identity-service/Makefile
rg -n '/health|/ready' doge-identity-service/src/core/api/asgi_app.py
```
