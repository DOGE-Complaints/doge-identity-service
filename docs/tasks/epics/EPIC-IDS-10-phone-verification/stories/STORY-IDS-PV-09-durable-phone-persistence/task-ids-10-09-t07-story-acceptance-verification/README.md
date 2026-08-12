## Task workspace — `task-ids-10-09-t07-story-acceptance-verification`

- Story: [`../STORY-IDS-PV-09-durable-phone-persistence.md`](../STORY-IDS-PV-09-durable-phone-persistence.md)
- Prerequisite: [`task-ids-10-09-t06-offline-phone-durability-regression-tests`](../task-ids-10-09-t06-offline-phone-durability-regression-tests/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000039`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md); [`story-acceptance-gate-template.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-PV-09 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim (7 checkboxes): session durability, audit durability, protocol parity, DI switch, migration coverage, bootstrap parity, SEC-02 scope boundary.

### Почему это важно
Story gate для pkg-000039; завершает G-3/G-2a phone persistence wave.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-PV-09-durable-phone-persistence.md`](../STORY-IDS-PV-09-durable-phone-persistence.md) (7 checkboxes verbatim).
2. Tasks t01–t06 — migration, stores, DI, bootstrap, durability tests.
3. Backlog source unchanged — [`STORY-IDS-PV-09-durable-phone-persistence.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-09-durable-phone-persistence.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [x] (P0) Story AC #1: session survives store rebuild — evidence t02, t06.
- [x] (P0) Story AC #2: audit survives repo rebuild — evidence t03, t06.
- [x] (P0) Story AC #3: protocol parity — evidence t02, t03.
- [x] (P0) Story AC #4: DI switch + in_memory unchanged — evidence t04, t06.
- [x] (P0) Story AC #5: migration + test coverage — evidence t01.
- [x] (P0) Story AC #6: bootstrap parity — evidence t05.
- [x] (P0) Story AC #7: no IP/UA logic added — evidence t03, t06 scope boundary.
- [x] (P1) `acceptance-verification-task-ids-10-09-t07-story-acceptance-verification.md` с PASS (P3 gate; `--print-utc-now` for Date).
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 9; bullrun sync (same iteration).
- [x] (P1) Backlog story Status → 🟢 Done (волна pkg-000039) optional sync.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-09-durable-phone-persistence/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- SEC-02 hashing changes
- Rate-limiting (SEC-01)
- Access-token statelessness (OAuth)
- pkg-000038 yaml changes

### Проверка
```bash
cd doge-identity-service
python3 -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
