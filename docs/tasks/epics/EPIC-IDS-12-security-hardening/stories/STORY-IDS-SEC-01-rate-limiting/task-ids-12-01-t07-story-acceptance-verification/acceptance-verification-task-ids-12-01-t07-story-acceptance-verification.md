# Acceptance verification — task-ids-12-01-t07-story-acceptance-verification

- **Gate:** PASS
- **Date:** 2026-06-26
- **Wave:** pkg-000035
- **Story:** STORY-IDS-SEC-01-rate-limiting

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| Чувствительные роуты + eid/start 5/10min/user | PASS | `rate_limit_config.py` defaults; `asgi_app.py` Depends on eid/start + callback; operator: phone/request follow-up |
| HTTP 429 + `retry_after` в envelope | PASS | `build_rate_limit_envelope`; `test_eid_start_rate_limit_returns_429_with_retry_after` |
| Сквозной слой до handler | PASS | `rate_limit_dependency.py`; wired via FastAPI Depends |
| OTP-cooldown сосуществование | PASS | `handlers.py` comment; `test_phone_otp_cooldown_still_domain_400_not_http_429` |
| Конфиг + N+1 тест | PASS | `schema.py` RATE_LIMIT_* env; `tests/test_rate_limiting.py` |
| DEFERRED альтернатива | N/A | не выбрана оператором |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
# 369 passed
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
