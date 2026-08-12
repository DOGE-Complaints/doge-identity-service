# Acceptance verification — task-ids-11-01-t07-story-acceptance-verification

- **Gate:** PASS (2026-06-24)
- **Wave:** pkg-000029
- **Story:** STORY-IDS-OAUTH-01-oauth-server-endpoints

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| `/oauth/authorize` (с валидным Supabase JWT) выдаёт authorization code привязанный к `supabase_user_id` | PASS | t04 — `handle_oauth_authorize_complete` + `issue_authorization_code`; t06 — `test_oauth_full_flow_with_pkce` |
| `/oauth/token` обменивает валидный code на access-токен; повторный обмен/просрочка → `invalid_grant` | PASS | t02/t04 — `InMemoryOAuthTokenService.issue_access_token`; t06 — `test_oauth_token_rejects_reused_code` |
| Неверный `client_secret` → отказ (в прод-пути проверка включена) | PASS | t02 — `client_secret.py` + token service; t06 — `test_oauth_token_rejects_wrong_client_secret` |
| PKCE: запрос с `code_challenge` требует корректный `code_verifier` | PASS | t04 — PKCE wire; t06 — `test_oauth_full_flow_with_pkce`, `test_oauth_token_pkce_mismatch` |
| `/oauth/authorize`: `invalid_client`, `invalid_redirect_uri`, `invalid_scope`, `state` пробрасывается | PASS | t03 — `oauth/handlers.py::handle_oauth_authorize`; t06 — authorize negative tests + state in callback |
| `authorization_request`-store: spa-login redirect + complete → code + ChatGPT redirect | PASS | t01 — `InMemoryAuthorizationRequestStore`; t03/t04; t06 — full flow |
| Ошибки RFC 6749; scope-модель валидируется | PASS | t02 — `oauth/errors.py`, `oauth/scope.py`; t06 — `test_oauth_rfc_error_shape` |
| Покрыто тестами (offline) | PASS | t06 — `tests/test_oauth_server_flow.py` (10 tests); `tests/test_oauth_authorization_request_store.py` (2) |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
# 341 passed; ok 7 paths
```
