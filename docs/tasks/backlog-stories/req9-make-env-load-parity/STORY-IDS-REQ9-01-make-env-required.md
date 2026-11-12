# STORY-IDS-REQ9-01 — make `.env` required on serve/dev (G8)

## Meta
- **Key:** `STORY-IDS-REQ9-01-make-env-required`
- **Пакет:** [`req9-make-env-load-parity/`](./INDEX.md)
- **Status:** 🟢 Done
- **Тип:** Makefile / ops parity / runbook
- **Parent REQ:** [`22-req9-make-env-load-parity.md`](../../../requirements/22-req9-make-env-load-parity.md)
- **Parent product:** REQ9 §3, §8.2, §10.1 G8
- **Tech-arch:** [`01-runtime-and-probes.md`](../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md) G8
- **Siblings:** gateway [`53`](../../../../doge-complaints-gateway/docs/requirements/53-req9-ops-parity-env-naming.md) / `STORY-GW-REQ9-*`; threads [`02`](../../../../doge-threads/docs/requirements/02-req9-ops-peer-token-docs.md); spa [`18`](../../../../spa-app/docs/requirements/18-req9-vite-identity-base-url.md); package sibling [REQ9-02](./STORY-IDS-REQ9-02-check-env-required.md)
- **Skill declared (future P3):** `devops-engineer` · soft `code-documenter`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/devops-engineer/SKILL.md`
- **Зависит от:** —
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Pipeline:** [`../epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md`](../../epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md) · pkg-000053 · P3 Done 2026-09-26T12:08:20Z

---

## Scope

1. `make serve` / `make dev`: shell-source `./.env` **required** — mirror gateway/threads (`set -a && . ./.env && set +a`), fail if missing (remove `if [ -f ./.env ]`).
2. Document unchanged names: `SERVICE_API_TOKEN`, `API_BASE_URL`, `PORT` (Makefile comment and/or `.env.example`).
3. Update [`run-and-healthcheck.md`](../../../runbook/run-and-healthcheck.md) so Make start wording matches G8 (required `.env`, not optional «подхватывает»).
4. Keep probes `/health` `/ready` (no path rename).

## Out of scope

- `make check-env` fail-closed → [REQ9-02](./STORY-IDS-REQ9-02-check-env-required.md).
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

## Nested tasks (materialized pkg-000053 · folders at P1.3)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-ids-16-01-t01-makefile-serve-dev` | 🟢 Done | Remove optional `if [ -f ]`; required `set -a && . ./.env` on serve/dev |
| **T02** | `task-ids-16-01-t02-env-example-runbook` | 🟢 Done | Comment names unchanged; runbook G8 wording |
| **T03** | `task-ids-16-01-t03-story-gate` | 🟢 Done | AC-IDS-REQ901-01…04 |

## Code touchpoints

- `Makefile` (`serve`, `dev`)
- `.env.example`
- `docs/runbook/run-and-healthcheck.md`

## Dependencies

- Unblocks [REQ9-02](./STORY-IDS-REQ9-02-check-env-required.md) (shared shell-source pattern).
- Sibling caller REQs parallel; this story owns identity Makefile + runbook only.
