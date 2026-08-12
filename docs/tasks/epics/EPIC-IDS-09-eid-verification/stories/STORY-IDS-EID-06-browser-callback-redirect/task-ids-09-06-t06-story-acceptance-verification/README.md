## Task workspace — `task-ids-09-06-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-EID-06-browser-callback-redirect.md`](../STORY-IDS-EID-06-browser-callback-redirect.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000019`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md`](../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md); [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F1, F6, F11)  
---

## Task: verify — STORY-IDS-EID-06 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim: `EidCallbackOutcome`, browser redirect 303 + markers, safe fallback 400, dynamic route + registry guard, EID-01 JSON regression, SPA-first docs, offline green.

### Почему это важно
EID-06 разблокирует EID-02 (real providers redirect browser to callback) per [`EPIC-IDS-EID.md`](../../../../../../backlog-stories/EPIC-IDS-EID.md).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-EID-06-browser-callback-redirect.md`](../STORY-IDS-EID-06-browser-callback-redirect.md) (6 checkboxes verbatim).
2. Tasks t01–t05 — implementation + tests + docs.
3. Backlog SSOT — [`STORY-IDS-EID-06-browser-callback-redirect.md`](../../../../../../backlog-stories/STORY-IDS-EID-06-browser-callback-redirect.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [x] (P0) Story AC #1: `handle_auth_eid_callback` → `EidCallbackOutcome` — evidence t01.
- [x] (P0) Story AC #2: browser 303 + `eid_status`/`eid_error` markers — evidence t03/t04.
- [x] (P0) Story AC #3: unknown session/return_url → safe 400, no redirect — evidence t03/t04.
- [x] (P0) Story AC #4: single `/auth/{provider}/callback`; unregistered → `ConfigError` — evidence t02/t04.
- [x] (P0) Story AC #5: EID-01 mock flow via JSON variant — evidence t04.
- [x] (P0) Story AC #6: docs SPA-first + offline green — evidence t05/t04.
- [x] (P1) `acceptance-verification-task-ids-09-06-t06-story-acceptance-verification.md` создан.
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-06-browser-callback-redirect/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/bullrun-launch-index.md` (story/task statuses)

### Out of scope
- Backlog file status sync (optional post-audit)
- Epic AC gate EPIC-IDS-09 (отдельная операция)
- EID-02 real provider implementation
- EID-07/EID-08 intake

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```
