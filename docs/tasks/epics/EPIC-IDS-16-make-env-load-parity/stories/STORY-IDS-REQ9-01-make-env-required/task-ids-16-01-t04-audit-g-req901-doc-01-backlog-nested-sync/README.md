## Task workspace — `task-ids-16-01-t04-audit-g-req901-doc-01-backlog-nested-sync`

- Story: [`../STORY-IDS-REQ9-01-make-env-required.md`](../STORY-IDS-REQ9-01-make-env-required.md)
- Prerequisite: [`task-ids-16-01-t03-story-gate`](../task-ids-16-01-t03-story-gate/README.md)
- Audit source: [`../../../../../../analysis/identity-req9-01-code-audit-2026-09-26.md`](../../../../../../analysis/identity-req9-01-code-audit-2026-09-26.md) (`G-REQ901-DOC-01`)
- P5 scaffold: `2026-09-26T12:13:03Z` · P6 Done: `2026-09-26T12:14:17Z`

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_16_req9_01_audit_2026_09_26`  
**Skill declared:** devops-engineer  
**Decision Ref:** [`../../../../../../analysis/identity-req9-01-code-audit-2026-09-26.md`](../../../../../../analysis/identity-req9-01-code-audit-2026-09-26.md) §Gaps `G-REQ901-DOC-01`  
---

## Task: docs — backlog REQ9-01 Nested Done + materialized folder names (`G-REQ901-DOC-01`)

### Цель
Синхронизировать backlog Nested с pipeline: Status → Done; folder names → `task-ids-16-01-t01…t03`. Не трогать Target/AC (уже `[x]`). Без правок Makefile / product / pytest.

### Почему это важно
Audit Low: Meta + AC backlog уже 🟢/`[x]`, но Nested остался Todo + projected `task-ids-req9-01-*` — дрейф persistent SSOT, не product gap.

### Факты из кода / docs
1. Backlog [`STORY-IDS-REQ9-01-make-env-required.md`](../../../../../backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md) — Nested now Done + `task-ids-16-01-t0N-*` (this P6).
2. Pipeline Nested T01–T03 🟢 `task-ids-16-01-t0N-*` (pkg-000053 P3 Done).
3. Package INDEX / bullrun — REQ9-01 🟢 pkg-000053.

### Gap / Проблема
Closed this P6 — backlog Nested synced. Immutable `pkg-000053` untouched.

### AC/DoD
- [x] (P0) Backlog Nested table → Status Done; folders `task-ids-16-01-t01…t03` (mirror pipeline).
- [x] (P0) Do not rewrite Target/AC text (already `[x]`).
- [x] (P1) No product source / Makefile / pytest.
- [x] (P1) Не мутировать `pkg-000053` / `identity-active-package.current.yaml`.
- [x] (P1) `acceptance-verification-task-ids-16-01-t04-audit-g-req901-doc-01-backlog-nested-sync.md` PASS.

### Где менять код
- `doge-identity-service/docs/tasks/backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md`

### Out of scope
- REQ9-02 materialize / `check-env`
- Product `Makefile` / `.env.example` / runbook body (already Done in P3)
- Live pytest re-run

### Проверка
```bash
rg -n 'task-ids-16-01-t0|task-ids-req9-01-t0|^\| \*\*T0' doge-identity-service/docs/tasks/backlog-stories/req9-make-env-load-parity/STORY-IDS-REQ9-01-make-env-required.md
```
