# Acceptance verification — task-ids-10-07-t06-story-acceptance-verification

- **Gate:** PASS (2026-06-02)
- **Wave:** pkg-000028
- **Story:** STORY-IDS-PV-07-telnyx-delivery-webhook

| AC (story verbatim) | Result | Evidence |
|---------------------|--------|----------|
| `POST /webhooks/telnyx/messaging` принимает события и обновляет `delivery_status` по `provider_message_id` | PASS | t01/t03/t04/t05 — `models.py` delivery fields; `delivery_ingest.py`; `handlers.py::handle_telnyx_messaging_webhook`; `asgi_app.py` route; `test_telnyx_delivery_webhook.py::test_valid_signed_webhook_updates_delivery_status` |
| Невалидная/отсутствующая подпись Telnyx → отклонение (401/403), не обрабатываем | PASS | t02/t04/t05 — `webhook_signature.py`; handler 401 on bad signature; `test_telnyx_webhook_signature.py`; `test_telnyx_delivery_webhook.py::test_invalid_signature_rejected_and_session_unchanged` |
| Повторное/устаревшее событие идемпотентно (не откатывает финальный статус) | PASS | t03/t05 — `apply_delivery_update` forward-only; `test_telnyx_delivery_ingest.py`; `test_telnyx_delivery_webhook.py::test_idempotent_replay_does_not_regress_final_status` |
| Событие доставки пишется в аудит без PII | PASS | t04/t05 — `telnyx_delivery_status_updated` audit; `test_telnyx_delivery_webhook.py::test_delivery_audit_logged_without_pii` |
| Offline-тесты: валидный/невалидный webhook, идемпотентность, маппинг статусов | PASS | t05 — `tests/test_telnyx_delivery_webhook.py` (5 tests); `tests/test_telnyx_webhook_signature.py` (3); `tests/test_telnyx_delivery_ingest.py` (6) |

```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
# 329 passed; ok 6 paths
```
