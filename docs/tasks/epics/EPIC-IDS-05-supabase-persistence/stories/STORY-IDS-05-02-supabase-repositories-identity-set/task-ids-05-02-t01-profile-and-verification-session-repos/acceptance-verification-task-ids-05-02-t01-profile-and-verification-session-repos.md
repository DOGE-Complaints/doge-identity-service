# Acceptance verification — task-ids-05-02-t01-profile-and-verification-session-repos

- **Gate:** PASS (2026-05-31)
- **Wave:** pkg-000006
- **Evidence:** `src/core/infrastructure/db_supabase.py` — Profile GET/upsert/PATCH with `ProfileConflictError` on 409; VerificationSession POST/GET/PATCH lifecycle
