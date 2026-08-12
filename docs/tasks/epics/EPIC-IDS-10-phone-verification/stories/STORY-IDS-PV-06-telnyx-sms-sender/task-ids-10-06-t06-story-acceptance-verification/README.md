## Task workspace — `task-ids-10-06-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-PV-06-telnyx-sms-sender.md`](../STORY-IDS-PV-06-telnyx-sms-sender.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000027`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md); [`../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md`](../../../../../../analysis/telnyx-integration-spec-dogestonia-2026-06-10.md) §2, §3, §9  
---

## Task: verify — STORY-IDS-PV-06 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim: Telnyx config/runtime, HTTP send, error mapping, offline tests, `.env.example`.

### Почему это важно
PV-06 разблокирует live SMS в production profile; PV-07 webhook builds on `provider_message_id`.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-PV-06-telnyx-sms-sender.md`](../STORY-IDS-PV-06-telnyx-sms-sender.md) (5 checkboxes verbatim).
2. Tasks t01–t05 — implementation + tests.
3. Backlog SSOT — [`STORY-IDS-PV-06-telnyx-sms-sender.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-06-telnyx-sms-sender.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [ ] (P0) Story AC #1: `SMS_PROVIDER=telnyx` + creds → `TelnyxSmsSender`; config errors → `ConfigError` — evidence t01/t04/t05.
- [ ] (P0) Story AC #2: correct POST + success result — evidence t02/t05.
- [ ] (P0) Story AC #3: Telnyx errors → `SmsErrorCode`; no PII logs — evidence t03/t05.
- [ ] (P0) Story AC #4: offline mocked httpx green; live skip without creds — evidence t05.
- [ ] (P0) Story AC #5: `.env.example` TELNYX_* block complete — evidence t05.
- [ ] (P1) `acceptance-verification-task-ids-10-06-t06-story-acceptance-verification.md` создан с PASS.
- [ ] (P1) Pipeline story Meta `Status: 🟢 Done`; epic Story 6; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-06-telnyx-sms-sender/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- Backlog file status sync (optional post-audit)
- PV-07 delivery webhook
- SPIKE-PV-08 Telnyx account setup (external)

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```
