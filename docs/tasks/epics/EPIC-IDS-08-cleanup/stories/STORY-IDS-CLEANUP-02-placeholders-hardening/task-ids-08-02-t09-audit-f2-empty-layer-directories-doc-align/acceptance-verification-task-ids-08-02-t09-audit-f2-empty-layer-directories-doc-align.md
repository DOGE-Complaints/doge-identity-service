# Acceptance verification — task-ids-08-02-t09-audit-f2-empty-layer-directories-doc-align

- **Branch:** A (remove empty directories)
- **Audit:** F2 ([`epic-ids-08-cleanup-02-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md))

## Evidence

- `src/core/audit/`, `oauth/`, `profiles/` — directories removed (0 residual empty dirs)
- [`03-soa-roles.md:64`](../../../../../../../docs/runtime-docs/03-soa-roles.md) — «удалены» matches filesystem fact

## AC/DoD

| Criterion | Result |
|-----------|--------|
| Branch A: rmdir three dirs | PASS |
| Branch A: doc aligned | PASS |
| Offline pytest | PASS (206 passed) |
