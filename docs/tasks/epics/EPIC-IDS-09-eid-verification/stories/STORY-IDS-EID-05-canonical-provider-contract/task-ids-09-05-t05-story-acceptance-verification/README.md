## Task workspace — `task-ids-09-05-t05-story-acceptance-verification`

- Story: [`../STORY-IDS-EID-05-canonical-provider-contract.md`](../STORY-IDS-EID-05-canonical-provider-contract.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000018`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F2, F12)  
---

## Task: verify — STORY-IDS-EID-05 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim: `EidErrorCode`, orchestrator error distinction, canonical subject_hash + dedup test, no new core error codes per provider, offline green.

### Почему это важно
Enabling wave EID-05 unlocks EID-06 (redirect consumes `EidErrorCode`) per [`EPIC-IDS-EID.md`](../../../../../../backlog-stories/EPIC-IDS-EID.md).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-EID-05-canonical-provider-contract.md`](../STORY-IDS-EID-05-canonical-provider-contract.md) (5 checkboxes verbatim).
2. Tasks t01–t04 — implementation + tests.
3. Backlog SSOT — [`STORY-IDS-EID-05-canonical-provider-contract.md`](../../../../../../backlog-stories/STORY-IDS-EID-05-canonical-provider-contract.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [x] (P0) Story AC #1: `EidErrorCode`; `EIDProviderError` carries canonical code — evidence t01.
- [x] (P0) Story AC #2: orchestrator distinguishes `EIDProviderError` / `Exception`; user_cancel in audit — evidence t02/t04.
- [x] (P0) Story AC #3: subject_hash rule documented; cross-provider dedup unit test — evidence t03/t04.
- [x] (P0) Story AC #4: new provider does not add error codes to core — design review t01.
- [x] (P0) Story AC #5: offline pytest green; error mapping + dedup tests — evidence t04.
- [x] (P1) `acceptance-verification-task-ids-09-05-t05-story-acceptance-verification.md` создан.
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-05-canonical-provider-contract/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/bullrun-launch-index.md` (story/task statuses)

### Out of scope
- Backlog file status sync (optional audit task)
- Epic AC gate EPIC-IDS-09 (отдельная операция)
- EID-06 intake
- EID-02 Authentigate vendor mapping

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```
