# Acceptance verification — task-ids-06-04-t03-story4-acceptance-verification

- **Gate:** PASS (2026-06-02, static contract + local pytest timing)
- **Wave:** pkg-000008
- **Evidence:** `tests/test_ci_workflows_contract.py` 2 passed; offline suite 192 passed in ~0.9s

| AC (epic L244–248) | Result |
|--------------------|--------|
| `test-offline.yml` на каждый push и PR | PASS — yaml contains `on: push` + `pull_request` (`test_ci_workflows_contract`) |
| `integration-live.yml` только main или workflow_dispatch | PASS — `branches: [main]` + `workflow_dispatch` in yaml |
| Offline workflow без `SUPABASE_*` secrets → live SKIPPED | PASS — `test-offline.yml` has no `secrets.SUPABASE`; offline pytest 10 deselected live |
| Offline workflow < 5 минут | PASS — local `pytest -m "not live_integration"` ~0.9s (CI install dominates; job design < 5m) |

**Operator (post-push):** `gh run list --workflow=test-offline.yml --limit 1` after secrets/workflows enabled on remote.
