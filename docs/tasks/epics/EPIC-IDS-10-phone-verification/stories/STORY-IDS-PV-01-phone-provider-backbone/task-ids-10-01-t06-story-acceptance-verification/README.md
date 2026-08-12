## Task workspace — `task-ids-10-01-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-PV-01-phone-provider-backbone.md`](../STORY-IDS-PV-01-phone-provider-backbone.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000022`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md); [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §3, §6  
---

## Task: verify — STORY-IDS-PV-01 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim: SMS port+DTO+errors+descriptor+runtime+registry guard, mock via descriptor, unregistered provider guard, extensible descriptors, offline green.

### Почему это важно
PV-01 разблокирует параллельный intake PV-02/PV-03/PV-04 per [`EPIC-IDS-PHONE.md`](../../../../../../backlog-stories/phone-verification/EPIC-IDS-PHONE.md) dependency graph.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-PV-01-phone-provider-backbone.md`](../STORY-IDS-PV-01-phone-provider-backbone.md) (5 checkboxes verbatim).
2. Tasks t01–t05 — implementation + offline tests.
3. Backlog SSOT — [`STORY-IDS-PV-01-phone-provider-backbone.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-01-phone-provider-backbone.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [x] (P0) Story AC #1: port + DTO + errors + descriptor + runtime + registry guard — evidence t01–t03.
- [x] (P0) Story AC #2: `MockSmsSender` via descriptor; registry active + mock — evidence t04.
- [x] (P0) Story AC #3: unregistered → `SmsProviderNotRegisteredError`/`ConfigError` — evidence t03/t05.
- [x] (P0) Story AC #4: +1 descriptor без правок registry class body — evidence t03.
- [x] (P0) Story AC #5: offline green — evidence t05.
- [x] (P1) `acceptance-verification-task-ids-10-01-t06-story-acceptance-verification.md` создан.
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; epic Story 1 section; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-01-phone-provider-backbone/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md` (Story 1 AC)
- `doge-identity-service/docs/tasks/bullrun-launch-index.md` (story/task statuses)

### Out of scope
- Backlog file status sync (optional post-audit)
- Epic gate EPIC-IDS-10 (отдельная операция)
- PV-02 config / `AppConfig.sms_provider`
- Service factory wiring

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```
