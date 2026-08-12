# Acceptance verification — task-ids-07-01-t06-story-acceptance-verification

- **Gate:** PASS (2026-06-04)
- **Wave:** pkg-000009
- **Story:** STORY-IDS-AUTHCORE-01-profile-and-me

| AC (story) | Result | Evidence |
|------------|--------|----------|
| `GET /me` без токена → 401 `AUTHENTICATION_REQUIRED` | PASS | `test_me_without_auth_returns_401`, `test_me_without_bearer_returns_401` |
| `GET /me` с валидным Supabase JWT → 200, `data` с `supabase_user_id`, `eid_verified`, поля профиля | PASS | `test_me_with_valid_jwt_and_profile_returns_200_envelope` |
| Если профиля нет — детерминировано + тест | PASS | t01: synthetic 200; `test_me_missing_profile_returns_200_not_verified_no_db_write` |
| Envelope `{"data": {...}}` | PASS | `test_me_response_uses_envelope_shape` |
| Offline тесты, `in_memory` | PASS | conftest `DB_BACKEND=in_memory`; 4 test modules /me |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q \
  tests/test_me_profile.py tests/test_http_transport_smoke.py \
  tests/test_asgi_transport.py tests/test_supabase_jwt_auth.py
# 33 passed

.venv/bin/python -m pytest -m "not live_integration" -q
# 199 passed, 1 failed
```

**Note (out of story scope):** `test_asgi_import_config_isolation.py::test_access_app_with_incomplete_supabase_env_raises_config_error` fails locally because `provide_app_config()` loads `SUPABASE_SERVICE_ROLE` from `.env` despite monkeypatch — EPIC-IDS-06 F1 artifact; не регрессия AUTHCORE-01.
