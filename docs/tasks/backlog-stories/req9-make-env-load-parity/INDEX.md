# REQ9 make `.env` load parity (identity) · index

**Зона:** `doge-identity-service/docs/tasks/backlog-stories/req9-make-env-load-parity/`  
**Тип:** backlog (постановки; P1.3/P3 — после активации pkg).  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)  
**Parent REQ:** [`22-req9-make-env-load-parity.md`](../../../requirements/22-req9-make-env-load-parity.md)  
**Parent product:** [`REQ9-DOGEstonia-Microservices-Ops-Parity-Target.md`](../../../../../docs/requirements%20backlog/REQ9-DOGEstonia-Microservices-Ops-Parity-Target.md)  
**Tech-arch:** [`docs/architecture/req9-ops-naming/01-runtime-and-probes.md`](../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md) (G8)  
**Dashboard:** [`identity-mvp-dashboard.md`](../../identity-mvp-dashboard.md) (operator lock: active MVP denominator)  
**Naming:** `STORY-IDS-REQ9-*`  
**Updated:** 2026-09-26T12:21:29Z · P3 Done REQ9-02 → EPIC-IDS-16 / pkg-000054 · package 2/2 Done

---

## Контекст одной фразой

Identity: `make serve`/`dev` require shell-source `./.env` (G8, gateway/threads parity); mini story for `make check-env` same policy. No peer URL renames; keep `SERVICE_API_TOKEN` / probes `/health` `/ready`.

---

## Operator locks (clarifying 2026-09-25)

| Theme | Decision |
|-------|----------|
| check-env | **C** — mini **REQ9-02** in same package; **Depends: REQ9-01**; TODO after 01 Done |
| runbook | **A** — `run-and-healthcheck.md` G8 wording in **REQ9-01** |
| dashboard | **A** — count in `identity-mvp-dashboard.md` active % |

---

## Stories

| Key | File | Status | Depends |
|-----|------|--------|---------|
| STORY-IDS-REQ9-01 | [STORY-IDS-REQ9-01-make-env-required.md](./STORY-IDS-REQ9-01-make-env-required.md) | 🟢 Done · pipeline [`EPIC-IDS-16` / pkg-000053](../../epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md) | — |
| STORY-IDS-REQ9-02 | [STORY-IDS-REQ9-02-check-env-required.md](./STORY-IDS-REQ9-02-check-env-required.md) | 🟢 Done · pipeline [`EPIC-IDS-16` / pkg-000054](../../epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-02-check-env-required/STORY-IDS-REQ9-02-check-env-required.md) | **REQ9-01** 🟢 |

---

## Out of package

- Renaming `SERVICE_API_TOKEN` / peer URLs on identity  
- Provider env family / product verification / spa `VITE_*`  
- `make test` / `make smoke` policy (not REQ 22)  
- Gateway/threads/aibridge Make edits  
