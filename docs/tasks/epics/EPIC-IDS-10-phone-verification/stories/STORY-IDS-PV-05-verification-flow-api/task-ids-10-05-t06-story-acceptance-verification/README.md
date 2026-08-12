## Task workspace — `task-ids-10-05-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-PV-05-verification-flow-api.md`](../STORY-IDS-PV-05-verification-flow-api.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** todo  
**Wave:** `pkg-000026`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md); [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §5, §10  
---

## Task: verify — STORY-IDS-PV-05 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim: request/confirm flow, errors, audit PII-free, MockSmsSender e2e.

### Почему это важно
PV-05 разблокирует PV-06 Telnyx live sender integration.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-PV-05-verification-flow-api.md`](../STORY-IDS-PV-05-verification-flow-api.md) (5 checkboxes verbatim).
2. Tasks t01–t05 — implementation + tests.
3. Backlog SSOT — [`STORY-IDS-PV-05-verification-flow-api.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-05-verification-flow-api.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [ ] (P0) Story AC #1: request creates session + SMS + expires_at — evidence t03/t05.
- [ ] (P0) Story AC #2: COUNTRY_NOT_ALLOWED + RATE_LIMITED + invalidation on new — evidence t03/t05.
- [ ] (P0) Story AC #3: confirm success + SmsErrorCode paths + 409 dedup — evidence t04/t05.
- [ ] (P0) Story AC #4: audit without PII — evidence t01/t03/t04/t05.
- [ ] (P0) Story AC #5: MockSmsSender offline e2e — evidence t05.
- [ ] (P1) `acceptance-verification-task-ids-10-05-t06-story-acceptance-verification.md` создан с PASS.
- [ ] (P1) Pipeline story Meta `Status: 🟢 Done`; epic Story 5; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-05-verification-flow-api/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- Backlog file status sync (optional post-audit)
- PV-06 Telnyx sender
- PV-07 delivery webhook

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```
