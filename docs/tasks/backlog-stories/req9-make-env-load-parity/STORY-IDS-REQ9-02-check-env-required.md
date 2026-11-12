# STORY-IDS-REQ9-02 — `make check-env` require `.env` (mini)

## Meta
- **Key:** `STORY-IDS-REQ9-02-check-env-required`
- **Пакет:** [`req9-make-env-load-parity/`](./INDEX.md)
- **Status:** 🟢 Done
- **Тип:** Makefile diagnostics / ops parity (mini)
- **Parent REQ:** [`22-req9-make-env-load-parity.md`](../../../requirements/22-req9-make-env-load-parity.md) (operator lock C — same package; not in §5 AC list)
- **Parent product:** REQ9 G8 spirit / one Make ritual
- **Tech-arch:** [`01-runtime-and-probes.md`](../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md)
- **Siblings:** [REQ9-01](./STORY-IDS-REQ9-01-make-env-required.md) (hard dep 🟢)
- **Skill declared (future P3):** `devops-engineer`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/devops-engineer/SKILL.md`
- **Зависит от:** **STORY-IDS-REQ9-01** 🟢 Done (shared shell-source pattern)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Pipeline:** [`../../epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-02-check-env-required/STORY-IDS-REQ9-02-check-env-required.md`](../../epics/EPIC-IDS-16-make-env-load-parity/stories/STORY-IDS-REQ9-02-check-env-required/STORY-IDS-REQ9-02-check-env-required.md) · pkg-000054 · P3 Done 2026-09-26T12:21:29Z

---

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

## Dependency / TODO (do not invent ahead of REQ9-01)

> **Hard dep:** do not mark this story Done until REQ9-01 AC-IDS-REQ901-01 is Pass.

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

## Nested tasks (materialized pkg-000054 · folders at P1.3)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-ids-16-02-t01-check-env-source` | 🟢 Done | Apply TODO-DEP-01…03 after REQ9-01 |
| **T02** | `task-ids-16-02-t02-story-gate` | 🟢 Done | AC-IDS-REQ902-01…03 + dep proof |

## Code touchpoints

- `Makefile` (`check-env` only, after REQ9-01)

## Dependencies

- **Requires Todo→Done:** [STORY-IDS-REQ9-01-make-env-required](./STORY-IDS-REQ9-01-make-env-required.md).
- Soft: none. Do not block REQ9-01 on this story.
