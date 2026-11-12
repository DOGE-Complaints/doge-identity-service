## Task workspace — `task-ids-15-01-t06-audit-g-vb01-doc-01-backlog-ac-sync`

- Story: [`../STORY-IDS-VB-01-persist-identity-verified.md`](../STORY-IDS-VB-01-persist-identity-verified.md)
- Prerequisite: [`task-ids-15-01-t05-story-acceptance-verification`](../task-ids-15-01-t05-story-acceptance-verification/README.md)
- Audit source: [`../../../../../../analysis/identity-vb-01-code-audit-2026-09-21.md`](../../../../../../analysis/identity-vb-01-code-audit-2026-09-21.md) (`G-VB01-DOC-01`)
- P5 scaffold: `2026-09-21T20:29:36Z` · P6 Done: `2026-09-21T20:32:01Z`

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_15_vb_01_audit_2026_09_21`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/identity-vb-01-code-audit-2026-09-21.md`](../../../../../../analysis/identity-vb-01-code-audit-2026-09-21.md) §Gaps `G-VB01-DOC-01`  
---

## Task: docs — backlog VB-01 AC `[ ]`→`[x]` + Nested Done (`G-VB01-DOC-01`)

### Цель
Синхронизировать backlog story с pipeline/INDEX: Target/AC отметить `[x]`; Nested Status → Done; folder names → materialized `task-ids-15-01-t01…t05` (как pipeline). Без правок product `src/` / migrations / pytest.

### Почему это важно
Audit Low: Meta backlog уже 🟢 Done, но AC и Nested остались Todo/projected — дрейф persistent SSOT, не product gap.

### Факты из кода / docs
1. Backlog [`STORY-IDS-VB-01-persist-identity-verified.md`](../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md) — Meta 🟢; Target/AC now `[x]`; Nested Done + `task-ids-15-01-*`.
2. Pipeline Meta 🟢; product code on disk (P3).
3. Package INDEX / bullrun — VB-01 🟢 pkg-000050.

### Gap / Проблема
Closed this P6 — backlog body synced. Immutable `pkg-000050` untouched.

### AC/DoD
- [x] (P0) Backlog Target/AC `:38-42` → `[x]` (verbatim text; no AC rewrite).
- [x] (P0) Nested table → Status Done; folders `task-ids-15-01-t01…t05` (mirror pipeline).
- [x] (P1) Prefer minimal: AC + Nested only (do not require Verified-current-state rewrite).
- [x] (P1) No product source / migrations / pytest.
- [x] (P1) Не мутировать `pkg-000050` / `identity-active-package.current.yaml`.
- [x] (P1) `acceptance-verification-task-ids-15-01-t06-audit-g-vb01-doc-01-backlog-ac-sync.md` PASS.

### Где менять код
- `doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md`

### Out of scope
- VB-02 / VB-03 materialize
- Product `src/` / SQL / tests
- Pipeline «Verified current state» historical snapshot

### Проверка
```bash
rg -n '^\- \[.\]|task-ids-15-01-t0|Status' doge-identity-service/docs/tasks/backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md
```
