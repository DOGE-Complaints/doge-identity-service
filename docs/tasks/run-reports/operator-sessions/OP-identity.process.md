# OP-identity — process SSOT (subagent delivery)

> **Updated:** 2026-09-26T12:01:17Z  
> **Working plan:** [`.cursor/plans/OP-identity-req9-20260926.plan.md`](../../../../../.cursor/plans/OP-identity-req9-20260926.plan.md)  
> **Session:** [OP-identity.session.yaml](./OP-identity.session.yaml)  
> **Wave:** [wave-20260926-req9.md](../operator-waves/wave-20260926-req9.md)  
> **Dashboard (contract):** [identity-backlog-dashboard.md](../../identity-backlog-dashboard.md) → [identity-mvp-dashboard.md](../../identity-mvp-dashboard.md)  
> **Fences SSOT:** [workflow-console.html](../../../../../docs/methodology/Zeya888-builder-queue/tools/workflow-console.html) · [workflow.md](../../../../../docs/methodology/Zeya888-builder-queue/core/workflow.md)  
> **Method:** [.cursor/rules/analysis.mdc](../../../../../.cursor/rules/analysis.mdc)  
> **Plan sim:** variant **1** — two-step Plan simulation (draft → **OP auto-approve** overnight → materialize)  
> **Overnight:** **on** — no pause after stories; stop only on explicit operator `стоп`/`stop`/`pause`/`halt`

## Model

- UI chats `BLD-identity` / `VAL-identity` are **not** required; titles are labels only.
- OP spawns **two subagents** (builder + validator) and sends **verbatim** console/workflow fences (variables filled only).
- Operator sets `$queueSpec`; **no copy-paste**.
- Claims: Read/Glob only. OP does not write product code, invent AC, or push.

## Overnight non-stop (hard)

`overnight: on` until operator says `стоп` / `stop` / `pause` / `halt`.

| Rule | Behavior |
|------|----------|
| Pause after story | **forbidden** |
| P1.3 / P5 GATE | OP **auto-approve** immediately after PLAN_DRAFT |
| After P8 / DONE | next QUEUED story in the same OP turn |
| BLOCKED prod/deploy/asset/verify FAIL | log facts → **continue queue** |
| P8 | local commits, **no push** |
| Operator report | only on explicit halt, queue exhausted, or verify FAIL (then BLOCKED + next) |

## Delivery

| Field | Value |
|-------|--------|
| `delivery` | `subagent` |
| Builder bootstrap | console **Session starter** — **once** for this lifecycle |
| Validator bootstrap | analysis.mdc + identity-operator-contract — **once** |
| Agent ids | `builder_agent_id` / `validator_agent_id` in session.yaml only — **not** in `.cursor/plans/*` |
| Resume | same subagents per phase/story if Cursor keeps Task id; else re-spawn + starter, rewrite ids |

## ROLE_LOCK (every phase)

```text
ROLE_LOCK: Execute ONLY the fence below. RETURN_TO_ROOT: paths + ≤5 lines facts. Do not advance phases yourself.
```

### PLAN_DRAFT

```text
SIMULATED_CURSOR_MODE: plan
STEP: PLAN_DRAFT
Allowed writes: ONLY ephemeral .cursor/plans/p1_*_scaffold_*.plan.md OR p5_*_gap_*.plan.md
Forbidden: epics/**/stories/** materialize, task README, pkg-*.yaml, *-active-package.current.yaml,
  bullrun-launch-index.md edits, product source under focus_folder, $planFile body (except reading).
Output: plan file path + mapping preview (no apply).
```

### PLAN_APPLY

```text
SIMULATED_CURSOR_MODE: plan_apply
STEP: PLAN_APPLY
Approved ephemeral plan: <path>
Execute materialize per that plan + original P1.3|P5 fence checklist.
Then --verify / --verify --check-dates as fence requires.
```

## Identity constants

| Variable | Value |
|----------|--------|
| `$builderProject` | `identity` |
| `workspace_root` | `/Users/eslinko/Development/DOGEstonia` |
| `$tasksRoot` | `doge-identity-service/docs/tasks` |
| `$planFile` | `.cursor/plans/ID_builder.plan.md` |
| `$pipelineDoc` | `doge-identity-service/docs/tasks/ids-epic-execution-pipeline.md` |
| `$verifyCmd` | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify` |
| `$printUtcNowCmd` | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --print-utc-now` |
| `$verifyDatesCmd` | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates` |
| `$backlogIndex` | `doge-identity-service/docs/tasks/backlog-stories/INDEX.md` |
| package INDEX | `doge-identity-service/docs/tasks/backlog-stories/req9-make-env-load-parity/INDEX.md` |
| contract | `docs/methodology/Zeya888-builder-queue/contracts/identity-operator-contract.md` |
| dashboard | `doge-identity-service/docs/tasks/identity-backlog-dashboard.md` (redirect → `identity-mvp-dashboard.md`) |
| profile skill | `python-pro` |
| story Skill declared | `devops-engineer` (P3 task README override) |
| P1.3 variant | console **P1.3** clean (`hasUxPipeline: false`) |
| `$p13Appendix` | identity-operator-contract §6 |
| P8 push | **forbidden** |

## Queue (resolved $queueSpec B)

`mode: sequential`. Source: req9-make-env-load-parity/INDEX.md Order 1–2.

| # | Key | Path | Start status |
|---|-----|------|--------------|
| 1 | REQ9-01 | `doge-identity-service/docs/tasks/backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md` | QUEUED |
| 2 | REQ9-02 | `doge-identity-service/docs/tasks/backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-02-check-env-required.md` | QUEUED |

P1.3 required for both: no pipeline story under `docs/tasks/epics/` as of 2026-09-26 (Glob 0 for STORY-IDS-REQ9*).

## Phase script

Same as working plan / [orchestrator-builder-reference.md](../../../../../docs/methodology/Zeya888-builder-queue/guides/orchestrator-builder-reference.md) §8.

Stop-rules: verify FAIL → BLOCKED + next; `WAVE_STALLED_NO_DELTA` → leave story, next; `P5_DISPOSITION_INCOMPLETE` → re-P5; wave halt only `стоп|stop|pause|halt`.
