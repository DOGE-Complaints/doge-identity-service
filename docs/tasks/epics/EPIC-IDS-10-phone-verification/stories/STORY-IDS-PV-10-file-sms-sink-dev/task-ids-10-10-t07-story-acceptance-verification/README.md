## Task workspace — `task-ids-10-10-t07-story-acceptance-verification`

- Story: [`../STORY-IDS-PV-10-file-sms-sink-dev.md`](../STORY-IDS-PV-10-file-sms-sink-dev.md)
- Prerequisite: [`task-ids-10-10-t06-offline-file-sms-tests`](../task-ids-10-10-t06-offline-file-sms-tests/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000041`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md); [`story-acceptance-gate-template.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-PV-10 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim (8 checkboxes): file sender, append, DX, sanitize, pilot guard, no httpx, hygiene, pytest gate.

### Почему это важно
Story gate для pkg-000041; завершает file SMS dev-DX wave (precedent PV-09 t07 — pytest gate, not doc-only).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-PV-10-file-sms-sink-dev.md`](../STORY-IDS-PV-10-file-sms-sink-dev.md) (8 checkboxes verbatim).
2. Tasks t01–t06 — sender, config, registry, pilot guard, hygiene, tests.
3. Backlog source unchanged — [`STORY-IDS-PV-10-file-sms-sink-dev.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-10-file-sms-sink-dev.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [x] (P0) Story AC #1: `SMS_PROVIDER=file` + request creates outbox log line — evidence t01, t03, t06.
- [x] (P0) Story AC #2: append + per-number files — evidence t01, t06.
- [x] (P0) Story AC #3: DX (`tail -f`) — manual note + file layout from t06.
- [x] (P0) Story AC #4: filename sanitize — evidence t01, t06.
- [x] (P0) Story AC #5: pilot+file ConfigError — evidence t04, t06.
- [x] (P0) Story AC #6: no httpx — evidence t03, t06.
- [x] (P0) Story AC #7: gitignore + env.example — evidence t05.
- [x] (P0) Story AC #8: offline pytest green — evidence t06.
- [x] (P1) `acceptance-verification-task-ids-10-10-t07-story-acceptance-verification.md` с PASS (P3 gate; `--print-utc-now` for Date).
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 10; bullrun sync (same iteration).
- [x] (P1) Backlog story Status → 🟢 Done (волна pkg-000041) optional sync.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-10-file-sms-sink-dev/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- Changes to mock/telnyx senders
- HTTP dev OTP endpoint (G-SMS-1 alt #2)
- pkg-000040 yaml changes

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -q -m "not live_integration"
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
