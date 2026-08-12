# BULLRUN-PHASE-LOG

- **Wave:** override `epic_ids_08_cleanup_02_audit_2026_06_05`
- **Process:** P3 Execute STORY-IDS-CLEANUP-02 t08 (audit F1)
- **Date:** 2026-06-02

| Phase | Status | Evidence |
|-------|--------|----------|
| Implement | Done | Branch A: `validate_return_url` in `handle_auth_eid_start_stub`; body parse in `asgi_app.py` |
| Verify | Done | `test_auth_eid_start_rejects_foreign_return_url` PASS; `rg validate_return_url src/` → handlers |

**Decision:** Branch A (enforce at stub boundary); invalid → 400 `invalid_return_url`.
