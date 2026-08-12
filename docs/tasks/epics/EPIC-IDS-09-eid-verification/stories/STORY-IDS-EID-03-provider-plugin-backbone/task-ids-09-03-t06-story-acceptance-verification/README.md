## Task workspace — `task-ids-09-03-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-EID-03-provider-plugin-backbone.md`](../STORY-IDS-EID-03-provider-plugin-backbone.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000016`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6  
---

## Task: verify — STORY-IDS-EID-03 parent acceptance criteria

### Цель
Закрыть story parent AC: plugin backbone (descriptor, runtime, lazy registry, guard, mock эталон) — все 5 пунктов backlog AC [x]; offline pytest green.

### Почему это важно
Epic gate и следующие enabling stories (EID-04…08) опираются на EID-03 как фундамент ([`EPIC-IDS-EID.md`](../../../../../../backlog-stories/EPIC-IDS-EID.md) порядок).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-EID-03-provider-plugin-backbone.md`](../STORY-IDS-EID-03-provider-plugin-backbone.md) (5 checkboxes).
2. Tasks t01–t05 — implementation + tests.
3. [`providers.py:92`](../../../../../../../src/core/infrastructure/providers.py) — должен быть заменён после t03 (verify no hardcoded registry).
4. [`registry.py`](../../../../../../../src/core/providers/registry.py) — guard после t04.
5. EID-01 regression — [`test_eid_verification_flow.py`](../../../../../../../tests/test_eid_verification_flow.py).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [x] (P0) Story AC #1: `EIDProviderDescriptor` + `ProviderRuntime`; mock via descriptor — verify imports + factory path.
- [x] (P0) Story AC #2: registry from descriptor set; extensibility without `providers.py`/`registry.py` body edits — code review checklist in acceptance doc.
- [x] (P0) Story AC #3: `ProviderNotRegisteredError`/`ConfigError` with available list — test evidence (t05).
- [x] (P0) Story AC #4: no network clients in mock/in-memory — test evidence (t05).
- [x] (P0) Story AC #5: full offline pytest green — `pytest -m "not live_integration" -q`.
- [x] (P1) `acceptance-verification-task-ids-09-03-t06-story-acceptance-verification.md` создан.
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-03-provider-plugin-backbone/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/bullrun-launch-index.md` (story/task statuses)

### Out of scope
- Backlog file status sync (optional separate audit task)
- Epic AC gate EPIC-IDS-09 (отдельная операция после всех stories)
- EID-02 intake

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/builder-queue/builder_resolve_queue.py --project identity --verify
```
