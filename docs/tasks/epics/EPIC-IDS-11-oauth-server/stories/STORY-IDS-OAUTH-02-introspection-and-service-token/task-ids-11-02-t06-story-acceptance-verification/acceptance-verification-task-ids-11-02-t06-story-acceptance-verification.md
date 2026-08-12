# Acceptance verification — task-ids-11-02-t06-story-acceptance-verification

- **Gate:** PASS
- **Date:** 2026-06-24
- **Wave:** pkg-000030
- **Story:** STORY-IDS-OAUTH-02-introspection-and-service-token

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| introspection с валидным токеном → `{active:true, sub, phone_verified}`; с просроченным/битым → `{active:false}` | PASS | `core/oauth/introspection.py`; `POST /oauth/introspect` in `asgi_app.py`; `tests/test_oauth_introspection.py` — active/inactive/expired |
| Запрос без валидного сервисного токена → 401/403 (даже с валидным пользовательским токеном) | PASS | `ServiceTokenAuth` + `require_service_token` in `security.py`; tests missing/invalid service token → 401 |
| `phone_verified` берётся из профиля, не из тела токена | PASS | `handle_oauth_introspect` profile lookup; `test_introspect_phone_verified_from_profile_not_jwt` |
| Покрыто тестами (offline) + зафиксирован контракт ответа для gateway | PASS | `tests/test_oauth_introspection.py` (7 tests, contract docstring); 350 pytest offline green |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
# 350 passed; ok 6 paths
```
