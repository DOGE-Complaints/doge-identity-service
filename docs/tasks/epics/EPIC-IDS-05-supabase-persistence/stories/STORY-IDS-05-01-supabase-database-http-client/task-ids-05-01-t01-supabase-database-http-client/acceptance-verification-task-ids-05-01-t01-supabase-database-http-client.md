# Acceptance verification — task-ids-05-01-t01-supabase-database-http-client

- **Gate:** PASS (2026-05-31)
- **Wave:** pkg-000006
- **Evidence:** `src/core/infrastructure/db_supabase.py` — frozen dataclass, `from_http` ValueError + URL normalize, `_headers` apikey/Bearer parity, `_request` error logging; module docstring PostgREST filters (`eq.`, `in.()`, `is.null`, `gt.`, `lt.`)
