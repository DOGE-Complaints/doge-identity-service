# Acceptance verification — task-ids-09-06-t06-story-acceptance-verification

- **Gate:** PASS (2026-06-09)
- **Wave:** pkg-000019
- **Story:** STORY-IDS-EID-06-browser-callback-redirect

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| `handle_auth_eid_callback` возвращает `EidCallbackOutcome` (домен-исход) | PASS | t01 — `eid_callback.py`, `handlers.py` |
| Успешный callback в браузере → `303` с `?eid_status=verified`; ошибка → `?eid_status=error&eid_error=<код>` | PASS | t03/t04 — `asgi_app.py`, `test_eid_callback_redirect.py` |
| Неизвестная сессия/return_url → безопасный 400 (без редиректа) | PASS | t03/t04 — safe fallback |
| Один роут `/auth/{provider}/callback`; незарегистрированный `provider` → `ConfigError` | PASS | t02/t04 — `asgi_app.py`, redirect tests |
| Mock-флоу EID-01 продолжает проходить (JSON-вариант) | PASS | t04 — `test_eid_verification_flow.py` |
| Доки отражают SPA-first redirect-модель; offline green | PASS | t05 docs; 232 pytest |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
# 232 passed
```
