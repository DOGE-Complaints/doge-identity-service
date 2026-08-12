# Acceptance verification — task-ids-05-02-t05-audit-s2-2-mark-consumed-started-guard

- **Gate:** PASS (2026-06-02)
- **Wave:** `run_mode=epic_ids_05_reaudit_2026_06_02`
- **Evidence:** `mark_consumed` params include `status=eq.started` (`db_supabase.py`); `test_verification_session_mark_consumed_filters_started_status`; `pytest -q` → 156 passed
