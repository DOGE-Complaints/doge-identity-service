# Acceptance verification — task-ids-07-02-t01-me-response-created-at-account-status

- **Gate:** PASS
- **Wave:** pkg-000044
- **Story:** STORY-IDS-AUTHCORE-02-me-account-fields

| AC/DoD | Result | Evidence |
|--------|--------|----------|
| Базовый dict: `account_status="active"`, `created_at=None` | PASS | [`me_response.py:19-35`](../../../../../../../src/core/api/me_response.py) |
| При profile: `created_at = _format_datetime(profile.created_at)` | PASS | [`me_response.py:49`](../../../../../../../src/core/api/me_response.py) |
| Не трогать email / email_verified | PASS | нет `email` в `build_me_data` (ONB-01) |
| `grep account_status supabase/bootstrap/` пусто | PASS | live: no matches |
| Import smoke | PASS | `.venv/bin/python -c "from core.api.me_response import build_me_data"` → ok |
