## Task workspace — `task-ids-10-04-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-PV-04-profile-flag-migration.md`](../STORY-IDS-PV-04-profile-flag-migration.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000025`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md); [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §4, §10.1  
---

## Task: verify — STORY-IDS-PV-04 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim: migration, attach, dedup, `/me`, offline green.

### Почему это важно
PV-04 разблокирует PV-05 flow API (нужны profile attach + dedup + `/me` fields).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-PV-04-profile-flag-migration.md`](../STORY-IDS-PV-04-profile-flag-migration.md) (5 checkboxes verbatim).
2. Tasks t01–t05 — implementation + tests.
3. Backlog SSOT — [`STORY-IDS-PV-04-profile-flag-migration.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-04-profile-flag-migration.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [ ] (P0) Story AC #1: migration columns + index — evidence t01.
- [ ] (P0) Story AC #2: `attach_phone_verification` sets flags — evidence t03/t04.
- [ ] (P0) Story AC #3: dedup `ProfileConflictError`/409 when `PHONE_ONE_ACCOUNT_PER_NUMBER=true` — evidence t03/t04 tests.
- [ ] (P0) Story AC #4: `/me` phone fields — evidence t05.
- [ ] (P0) Story AC #5: offline suite green — evidence t01–t05.
- [ ] (P1) `acceptance-verification-task-ids-10-04-t06-story-acceptance-verification.md` создан с PASS.
- [ ] (P1) Pipeline story Meta `Status: 🟢 Done`; epic Story 4; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-04-profile-flag-migration/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- Backlog file status sync (optional post-audit)
- PV-05 HTTP flow
- Telnyx PV-06/07

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```
