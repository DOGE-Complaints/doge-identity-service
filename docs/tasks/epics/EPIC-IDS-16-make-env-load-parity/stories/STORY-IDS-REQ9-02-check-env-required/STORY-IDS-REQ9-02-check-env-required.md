# STORY-IDS-REQ9-02 — `make check-env` require `.env` (mini)

## Meta
- **Key:** `STORY-IDS-REQ9-02-check-env-required`
- **Parent Epic:** [`../../EPIC-IDS-16-make-env-load-parity.md`](../../EPIC-IDS-16-make-env-load-parity.md)
- **Status:** 🟢 Done
- **source:** `backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md`
- **Package:** [`req9-make-env-load-parity/INDEX.md`](../../../../backlog-stories/req9-make-env-load-parity/INDEX.md)
- **Parent REQ:** [`doge-identity-service/docs/requirements/22-req9-make-env-load-parity.md`](../../../../../requirements/22-req9-make-env-load-parity.md) (operator lock C — same package; not in §5 AC list)
- **Parent product:** REQ9 G8 spirit / one Make ritual
- **Tech-arch:** [`01-runtime-and-probes.md`](../../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md)
- **Decision Ref:** [`../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md`](../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md); REQ22; hard dep [REQ9-01](../STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md) 🟢 Done pkg-000053
- **Siblings:** [REQ9-01](../STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md) (hard dep 🟢)
- **Skill declared:** `devops-engineer` — [SKILL.md](../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/devops-engineer/SKILL.md)
- **Depends:** [STORY-IDS-REQ9-01-make-env-required](../STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md) 🟢 Done
- **Wave:** `pkg-000054`
- **P1 materialize:** 2026-09-26T12:18:23Z
- **P3 Done:** 2026-09-26T12:21:29Z

## Scope

1. Align `make check-env` with the **same** required `./.env` shell-source as `serve`/`dev` after REQ9-01 lands (fail closed if missing).
2. Keep `check-env` as a print/diagnostic target (no new product env keys).

## Out of scope

- Changing which variables `check-env` prints (unless needed to stay truthful after source).
- `serve`/`dev` / runbook (owned by REQ9-01).
- Renames, providers, product flows.

## Verified current state

| Fact | Path |
|------|------|
| `check-env` optional `.env` | `Makefile:13-20` |
| `serve`/`dev` still optional until REQ9-01 | `Makefile:3-11` |

> **Note (P1 materialize):** backlog Verified table is historical pre-01. Post-REQ9-01 fact: `serve`/`dev` required (`Makefile:4-11`); `check-env` still optional (`Makefile:14-15`). Re-Grep at P3 (TODO-DEP-04).

## Dependency / TODO (do not invent ahead of REQ9-01)

> **Hard dep:** do not mark this story Done until REQ9-01 AC-IDS-REQ901-01 is Pass.  
> **Status at materialize:** REQ9-01 🟢 Done (pkg-000053) — dep unlocked for P3.

**TODO (after REQ9-01 Done — implement wave):**

1. **TODO-DEP-01:** Copy the **exact** post-01 `serve`/`dev` shell-source stanza into `check-env` (no leftover `if [ -f ./.env ]`).
2. **TODO-DEP-02:** Manually verify: without `./.env`, `make check-env` fails closed (same class of failure as `make serve`).
3. **TODO-DEP-03:** If REQ9-01 adjusted Makefile comments for G8, ensure `check-env` header comment does not claim optional load.
4. **TODO-DEP-04:** Re-read `Makefile` at implement time — line numbers below are pre-01; re-Grep before edit.

Until REQ9-01 is Done, leave `check-env` unchanged in P3 of this story (no premature dual patterns).

## Target / AC

- [x] **AC-IDS-REQ902-01:** `make check-env` requires sourcing `./.env` (fail closed if absent).
- [x] **AC-IDS-REQ902-02:** Shell-source pattern matches post-REQ9-01 `serve`/`dev` (no optional `if [ -f ]` divergence).
- [x] **AC-IDS-REQ902-03:** REQ9-01 Done evidence cited in story gate / acceptance (dep closed).

## Техническое решение (projected)

- **Approach:** copy exact post-01 `set -a && . ./.env && set +a` into `check-env` only; keep print/diagnostic keys; do not touch `serve`/`dev`/runbook.
- **Skill:** devops-engineer
- **Depends:** REQ9-01 Done (satisfied).

## Nested tasks (materialized pkg-000054)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | [`task-ids-16-02-t01-check-env-source`](task-ids-16-02-t01-check-env-source/README.md) | 🟢 Done | Apply TODO-DEP-01…03 after REQ9-01 |
| **T02** | [`task-ids-16-02-t02-story-gate`](task-ids-16-02-t02-story-gate/README.md) | 🟢 Done | AC-IDS-REQ902-01…03 + dep proof |

## Code touchpoints

- `Makefile` (`check-env` only, after REQ9-01)

## Dependencies

- **Requires Todo→Done:** [STORY-IDS-REQ9-01-make-env-required](../STORY-IDS-REQ9-01-make-env-required/STORY-IDS-REQ9-01-make-env-required.md) 🟢 Done.
- Soft: none. Do not block REQ9-01 on this story.
