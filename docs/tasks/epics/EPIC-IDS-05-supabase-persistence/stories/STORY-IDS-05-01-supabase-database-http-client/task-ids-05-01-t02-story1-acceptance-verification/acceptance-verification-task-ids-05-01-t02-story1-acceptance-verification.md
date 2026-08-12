# Acceptance verification — task-ids-05-01-t02-story1-acceptance-verification

- **Gate:** PASS (2026-05-31)
- **Wave:** pkg-000006
- **Evidence:** `tests/test_db_supabase_client.py` — 5 passed

| AC (epic L69–73) | Result |
|------------------|--------|
| `from_http("", "key")` → `ValueError` | PASS — `test_from_http_empty_url_raises_value_error` |
| `from_http("https://x.co/", "key").base_url == "https://x.co"` | PASS — `test_from_http_strips_trailing_slash_from_base_url` |
| `_headers()["apikey"] == _headers()["Authorization"].split()[-1]` | PASS — `test_headers_apikey_matches_bearer_token_value` |
| `_request` HTTP 5xx → `logger.error` + `httpx.HTTPError` | PASS — `test_request_on_http_5xx_logs_error_and_raises` |
