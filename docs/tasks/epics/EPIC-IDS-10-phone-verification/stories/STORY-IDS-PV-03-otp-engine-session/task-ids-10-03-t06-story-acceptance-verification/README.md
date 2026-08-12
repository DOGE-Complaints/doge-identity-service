## Task workspace — `task-ids-10-03-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-PV-03-otp-engine-session.md`](../STORY-IDS-PV-03-otp-engine-session.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000024`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md); [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §3, §5, §10.1  
---

## Task: verify — STORY-IDS-PV-03 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim: session+store, OTP hash, verify paths, repeat invalidation, subject_hash, offline green.

### Почему это важно
PV-03 разблокирует PV-05 flow API (нужны session + OTP engine).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-PV-03-otp-engine-session.md`](../STORY-IDS-PV-03-otp-engine-session.md) (6 checkboxes verbatim).
2. Tasks t01–t05 — implementation + tests.
3. Backlog SSOT — [`STORY-IDS-PV-03-otp-engine-session.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-03-otp-engine-session.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [ ] (P0) Story AC #1: session + store with attempts — evidence t01/t02/t05.
- [ ] (P0) Story AC #2: crypto OTP, hash only, no log — evidence t03/t05.
- [ ] (P0) Story AC #3: verify ok / mismatch / limit / expired — evidence t04/t05.
- [ ] (P0) Story AC #4: repeat invalidation — evidence t03/t05.
- [ ] (P0) Story AC #5: `subject_hash = hash_secret(e164)` — evidence t01/t04/t05.
- [ ] (P0) Story AC #6: offline tests — evidence t05.
- [ ] (P1) `acceptance-verification-task-ids-10-03-t06-story-acceptance-verification.md` создан.
- [ ] (P1) Pipeline story Meta `Status: 🟢 Done`; epic Story 3; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-03-otp-engine-session/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- Backlog file status sync (optional post-audit)
- PV-04 profile flag
- PV-05 HTTP flow

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```
