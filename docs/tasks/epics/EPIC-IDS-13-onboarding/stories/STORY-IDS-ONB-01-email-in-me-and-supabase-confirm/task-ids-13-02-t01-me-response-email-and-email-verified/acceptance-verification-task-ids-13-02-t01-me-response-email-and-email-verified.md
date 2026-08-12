# Acceptance verification — task-ids-13-02-t01-me-response-email-and-email-verified

- **Gate:** PASS
- **Wave:** pkg-000045
- **Story:** STORY-IDS-ONB-01-email-in-me-and-supabase-confirm
- **Date:** 2026-07-24T18:57:53Z

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| Базовый dict: `email=current_user.email`, `email_verified=True` (и при no-profile) | PASS | [`me_response.py:21-22`](../../../../../../../src/core/api/me_response.py) |
| Сохранены AUTHCORE-02 `created_at` / `account_status` | PASS | [`me_response.py:35-36,50`](../../../../../../../src/core/api/me_response.py) |
| Import smoke | PASS | `.venv/bin/python -c "from core.api.me_response import build_me_data"` → ok |
