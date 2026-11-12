# STORY-IDS-REQ9-01 — make `.env` required on serve/dev (G8)

## Meta
- **Key:** `STORY-IDS-REQ9-01-make-env-required`
- **Parent Epic:** [`../../EPIC-IDS-16-make-env-load-parity.md`](../../EPIC-IDS-16-make-env-load-parity.md)
- **Status:** 🟢 Done
- **source:** `backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md`
- **Package:** [`req9-make-env-load-parity/INDEX.md`](../../../../backlog-stories/req9-make-env-load-parity/INDEX.md)
- **Parent REQ:** [`doge-identity-service/docs/requirements/22-req9-make-env-load-parity.md`](../../../../../requirements/22-req9-make-env-load-parity.md)
- **Parent product:** REQ9 §3, §8.2, §10.1 G8 — [`REQ9-DOGEstonia-Microservices-Ops-Parity-Target.md`](../../../../../../docs/requirements%20backlog/REQ9-DOGEstonia-Microservices-Ops-Parity-Target.md)
- **Tech-arch:** [`01-runtime-and-probes.md`](../../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md) G8
- **Decision Ref:** [`../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md`](../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md); REQ22; tech-arch G8; parent product REQ9
- **Siblings:** gateway `53` / `STORY-GW-REQ9-*`; threads `02`; spa `18`; package sibling [REQ9-02](../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md)
- **Skill declared:** `devops-engineer` — [SKILL.md](../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/devops-engineer/SKILL.md) · soft `code-documenter`
- **Depends:** —
- **Wave:** `pkg-000053`
- **P1 materialize:** 2026-09-26T12:04:46Z
- **P3 Done:** 2026-09-26T12:08:20Z

## Scope

1. `make serve` / `make dev`: shell-source `./.env` **required** — mirror gateway/threads (`set -a && . ./.env && set +a`), fail if missing (remove `if [ -f ./.env ]`).
2. Document unchanged names: `SERVICE_API_TOKEN`, `API_BASE_URL`, `PORT` (Makefile comment and/or `.env.example`).
3. Update [`run-and-healthcheck.md`](../../../../runbook/run-and-healthcheck.md) so Make start wording matches G8 (required `.env`, not optional «подхватывает»).
4. Keep probes `/health` `/ready` (no path rename).

## Out of scope

- `make check-env` fail-closed → [REQ9-02](../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md).
- Renaming `SERVICE_API_TOKEN` or peer URLs on identity.
- Provider env family; product verification; spa/gateway renames.
- `make test` / `make smoke` policy.

## Verified current state

| Fact | Path |
|------|------|
| `serve`/`dev` optional `.env` | `Makefile:3-11` |
| Gateway required shell-source | `doge-complaints-gateway/Makefile:14-22` |
| Threads required shell-source | `doge-threads/Makefile:16-22` |
| `PORT` / `API_BASE_URL` | `.env.example:9-10` |
| `SERVICE_API_TOKEN=` | `.env.example:135` |
| Probes | `src/core/api/asgi_app.py:288`, `:295` |
| Runbook Make wording | `docs/runbook/run-and-healthcheck.md:43` |

## Target / AC

- [x] **AC-IDS-REQ901-01 (G8):** `make serve` and `make dev` require sourcing `./.env` (fail closed if absent), same shell pattern as gateway/threads.
- [x] **AC-IDS-REQ901-02:** `GET /health` and `GET /ready` remain registered (no probe rename).
- [x] **AC-IDS-REQ901-03:** Inbound env name `SERVICE_API_TOKEN` unchanged in `.env.example` (no rename in Makefile).
- [x] **AC-IDS-REQ901-04:** Document `API_BASE_URL` / `PORT` names stay; runbook Make section states required `./.env` for `serve`/`dev`.

## Техническое решение (projected)

- **Approach:** mirror gateway/threads Make pattern for `serve`/`dev` only (`set -a && . ./.env && set +a` without `if [ -f ]`); document unchanged env names; update runbook G8 wording; do **not** touch `check-env` (REQ9-02); do not rename probes.
- **Skill:** devops-engineer
- **Arch:** [01-runtime-and-probes.md](../../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md) G8

## Nested tasks (materialized pkg-000053)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | [`task-ids-16-01-t01-makefile-serve-dev`](task-ids-16-01-t01-makefile-serve-dev/README.md) | 🟢 Done | Remove optional `if [ -f ]`; required `set -a && . ./.env` on serve/dev |
| **T02** | [`task-ids-16-01-t02-env-example-runbook`](task-ids-16-01-t02-env-example-runbook/README.md) | 🟢 Done | Comment names unchanged; runbook G8 wording |
| **T03** | [`task-ids-16-01-t03-story-gate`](task-ids-16-01-t03-story-gate/README.md) | 🟢 Done | AC-IDS-REQ901-01…04 |
| **T04** | [`task-ids-16-01-t04-audit-g-req901-doc-01-backlog-nested-sync`](task-ids-16-01-t04-audit-g-req901-doc-01-backlog-nested-sync/README.md) | 🟢 Done | Audit G-REQ901-DOC-01 — backlog Nested sync (override) |

## Code touchpoints

- `Makefile` (`serve`, `dev`)
- `.env.example`
- `docs/runbook/run-and-healthcheck.md`

## Dependencies

- Unblocks [REQ9-02](../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md) (shared shell-source pattern).
- Sibling caller REQs parallel; this story owns identity Makefile + runbook only.
