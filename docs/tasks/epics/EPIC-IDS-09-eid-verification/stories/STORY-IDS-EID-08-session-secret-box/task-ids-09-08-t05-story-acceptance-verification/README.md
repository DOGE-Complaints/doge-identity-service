## Task workspace — `task-ids-09-08-t05-story-acceptance-verification`

- Story: [`../STORY-IDS-EID-08-session-secret-box.md`](../STORY-IDS-EID-08-session-secret-box.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000021`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/STORY-IDS-EID-08-session-secret-box.md`](../../../../../../backlog-stories/STORY-IDS-EID-08-session-secret-box.md); [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F7)  
---

## Task: verify — STORY-IDS-EID-08 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim: `SessionSecretBox` port+Fernet, `EID_SESSION_ENC_KEY` pilot/demo rules, `ProviderRuntime.secret_box`, key separation from `eid_secret`, offline green.

### Почему это важно
EID-08 разблокирует EID-02 (Authentigate PKCE capstone) per [`EPIC-IDS-EID.md`](../../../../../../backlog-stories/EPIC-IDS-EID.md) dependency graph.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-EID-08-session-secret-box.md`](../STORY-IDS-EID-08-session-secret-box.md) (5 checkboxes verbatim).
2. Tasks t01–t04 — implementation + offline tests.
3. Backlog SSOT — [`STORY-IDS-EID-08-session-secret-box.md`](../../../../../../backlog-stories/STORY-IDS-EID-08-session-secret-box.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [x] (P0) Story AC #1: `SessionSecretBox` port + Fernet; seal/open round-trip — evidence t01/t04.
- [x] (P0) Story AC #2: `EID_SESSION_ENC_KEY` pilot required, demo default — evidence t02/t04.
- [x] (P0) Story AC #3: `secret_box` via `ProviderRuntime` — evidence t03/t04.
- [x] (P0) Story AC #4: encryption key ≠ `eid_secret` — evidence t01/t02/t04.
- [x] (P0) Story AC #5: offline green — evidence t04.
- [x] (P1) `acceptance-verification-task-ids-09-08-t05-story-acceptance-verification.md` создан.
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-08-session-secret-box/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/bullrun-launch-index.md` (story/task statuses)

### Out of scope
- Backlog file status sync (optional post-audit)
- Epic AC gate EPIC-IDS-09 (отдельная операция)
- EID-02 Authentigate provider PKCE usage
- KMS/key rotation

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```
