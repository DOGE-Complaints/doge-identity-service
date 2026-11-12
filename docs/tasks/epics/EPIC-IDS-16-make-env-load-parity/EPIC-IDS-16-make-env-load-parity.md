# EPIC-IDS-16 — REQ9 make `.env` load parity (G8)

> **ID:** `EPIC-IDS-16` · **Alias (backlog package):** `req9-make-env-load-parity` · **Статус:** 🟢 Done (REQ9-01 🟢 pkg-000053; REQ9-02 🟢 pkg-000054) · **Тип:** Ops / Makefile / runbook  
> **Source (backlog):** [`backlog-stories/req9-make-env-load-parity/INDEX.md`](../../backlog-stories/req9-make-env-load-parity/INDEX.md)  
> **P1 materialize (REQ9-01):** 2026-09-26T12:04:46Z · **P3 Done (REQ9-01):** 2026-09-26T12:08:20Z · **P1 materialize (REQ9-02):** 2026-09-26T12:18:23Z · **P3 Done (REQ9-02):** 2026-09-26T12:21:29Z · **REQ:** [`22-req9-make-env-load-parity.md`](../../../requirements/22-req9-make-env-load-parity.md)  
> **Parent product:** [`REQ9-DOGEstonia-Microservices-Ops-Parity-Target.md`](../../../../docs/requirements%20backlog/REQ9-DOGEstonia-Microservices-Ops-Parity-Target.md) §3, §8.2, §10.1 G8  
> **Tech-arch:** [`01-runtime-and-probes.md`](../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md) G8

## Назначение

Identity Make start (`serve`/`dev`) требует shell-source `./.env` (G8, parity с gateway/threads); mini story для `check-env` той же политики (REQ9-02). Без rename `SERVICE_API_TOKEN` / peer URLs; probes `/health` `/ready` без rename.

## База (не дублировать в stories)

- REQ [`22-req9-make-env-load-parity.md`](../../../requirements/22-req9-make-env-load-parity.md)
- Tech-arch [`01-runtime-and-probes.md`](../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md) G8
- Package INDEX [`req9-make-env-load-parity/INDEX.md`](../../backlog-stories/req9-make-env-load-parity/INDEX.md)

## Locked decisions (epic-wide)

| ID | Решение | Обоснование |
|----|---------|-------------|
| **D-REQ9-1** | `serve`/`dev` fail-closed if `./.env` missing | G8; gateway/threads pattern |
| **D-REQ9-2** | `check-env` same policy → REQ9-02 (Depends REQ9-01) | Package INDEX operator lock C |
| **D-REQ9-3** | Keep names `SERVICE_API_TOKEN` / `API_BASE_URL` / `PORT`; probes `/health` `/ready` | REQ22 / G8; no rename |

Волна pkg-000054 materialize **только REQ9-02** (REQ9-01 Done pkg-000053).

## Stories

| Story | Тема | Статус |
|-------|------|--------|
| [REQ9-01](stories/STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md) | `make serve`/`dev` require `.env` + runbook | 🟢 Done (pkg-000053) |
| [REQ9-02](stories/STORY-IDS-REQ9-02-check-env-required/STORY-IDS-REQ9-02-check-env-required.md) | `make check-env` require `.env` | 🟢 Done (pkg-000054) |

## Порядок

**REQ9-01** → **REQ9-02**. Sibling gateway/threads/spa REQs — не этот эпик.

## Non-goals эпика

- Renaming `SERVICE_API_TOKEN` / peer URLs on identity
- Provider env family / product verification / spa `VITE_*`
- `make test` / `make smoke` policy
- Gateway/threads/aibridge Make edits

### Story 1: STORY-IDS-REQ9-01 — make `.env` required on serve/dev — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md`](./stories/STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md)
- **Source (backlog):** [`backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md`](../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md)
- **Wave:** `pkg-000053` (P3 Done 2026-09-26T12:08:20Z)

### Story 2: STORY-IDS-REQ9-02 — `make check-env` require `.env` — 🟢 Done

- **Pipeline story:** [`stories/STORY-IDS-REQ9-02-check-env-required/STORY-IDS-REQ9-02-check-env-required.md`](./stories/STORY-IDS-REQ9-02-check-env-required/STORY-IDS-REQ9-02-check-env-required.md)
- **Source (backlog):** [`backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md`](../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md)
- **Wave:** `pkg-000054` (P3 Done 2026-09-26T12:21:29Z)
