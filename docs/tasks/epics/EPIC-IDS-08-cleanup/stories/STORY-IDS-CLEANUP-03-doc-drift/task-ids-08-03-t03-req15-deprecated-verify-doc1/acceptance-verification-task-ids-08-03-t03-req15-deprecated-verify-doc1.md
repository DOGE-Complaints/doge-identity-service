# Acceptance verification — task-ids-08-03-t03-req15-deprecated-verify-doc1

- **Wave:** pkg-000014 · **Date:** 2026-06-02

## Branch

**Branch A (verify) + minimal Branch B:** DEPRECATED banner from CLEANUP-01 t05 was sufficient; status line `НЕ реализовано` contradicted banner → aligned to `DEPRECATED — historical spec only`.

## Evidence

| Claim | Source |
|-------|--------|
| DEPRECATED banner at top | `req-15:3` — `> **DEPRECATED (2026-06):**` |
| Status line aligned | `req-15:5` — `> **Статус:** DEPRECATED — historical spec only` |
| Body retained as historical | req-15 §Canonical Story Lifecycle unchanged |

## AC/DoD

| Criterion | Result |
|-----------|--------|
| Branch A: banner sufficient (CLEANUP-01 t05) | PASS |
| Branch B: status line no longer reads as active spec | PASS |
| Story AC #3 (partial): req-15 deprecated evidenced | PASS |
| BULLRUN-PHASE-LOG + acceptance in task folder | PASS |
