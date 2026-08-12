## Task workspace — `task-ids-10-07-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../STORY-IDS-PV-07-telnyx-delivery-webhook.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000028`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md); [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §10.1  
---

## Task: verify — STORY-IDS-PV-07 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim: webhook endpoint, signature, idempotency, audit, offline tests.

### Почему это важно
PV-07 закрывает P2 (delivery tracking) в MVP; разблокирует observability/fraud signals без изменения verify flow.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../STORY-IDS-PV-07-telnyx-delivery-webhook.md) (5 checkboxes verbatim).
2. Tasks t01–t05 — implementation + tests.
3. Backlog SSOT — [`STORY-IDS-PV-07-telnyx-delivery-webhook.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-07-telnyx-delivery-webhook.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [x] (P0) Story AC #1: `POST /webhooks/telnyx/messaging` updates `delivery_status` by `provider_message_id` — evidence t01/t03/t04/t05.
- [x] (P0) Story AC #2: invalid/missing signature → 401/403 — evidence t02/t04/t05.
- [x] (P0) Story AC #3: idempotent forward-only updates — evidence t03/t05.
- [x] (P0) Story AC #4: delivery audit without PII — evidence t04/t05.
- [x] (P0) Story AC #5: offline webhook tests green — evidence t05.
- [x] (P1) `acceptance-verification-task-ids-10-07-t06-story-acceptance-verification.md` создан с PASS.
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic Story 7; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-07-telnyx-delivery-webhook/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- Backlog file status sync (optional post-audit)
- SPIKE-PV-08 live webhook
- Retry UX on `failed` delivery

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```
