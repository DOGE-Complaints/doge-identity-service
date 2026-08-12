## Task workspace — `task-ids-10-02-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-PV-02-provider-owned-config.md`](../STORY-IDS-PV-02-provider-owned-config.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000023`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md); [`../../../../../../analysis/phone-verification-architecture-2026-06-10.md`](../../../../../../analysis/phone-verification-architecture-2026-06-10.md) §7, §10.2  
---

## Task: verify — STORY-IDS-PV-02 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim: SMS_PROVIDER registry validation, prefix allowlist, E.164 tests, AppConfig core fields, `.env.example`, offline green.

### Почему это важно
PV-02 разблокирует PV-03/PV-04/PV-05 parallel intake per epic dependency graph.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-PV-02-provider-owned-config.md`](../STORY-IDS-PV-02-provider-owned-config.md) (5 checkboxes verbatim).
2. Tasks t01–t05 — implementation + tests.
3. Backlog SSOT — [`STORY-IDS-PV-02-provider-owned-config.md`](../../../../../../backlog-stories/phone-verification/STORY-IDS-PV-02-provider-owned-config.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [ ] (P0) Story AC #1: `SMS_PROVIDER` registry + `ConfigError` — evidence t02/t05.
- [ ] (P0) Story AC #2: prefix allowlist `+372` ok / `+1` rejected — evidence t03/t05.
- [ ] (P0) Story AC #3: E.164 normalization tests — evidence t03/t05.
- [ ] (P0) Story AC #4: core phone params on `AppConfig`; no provider fields — evidence t02/t05.
- [ ] (P0) Story AC #5: `.env.example` + offline green — evidence t04/t05.
- [ ] (P1) `acceptance-verification-task-ids-10-02-t06-story-acceptance-verification.md` создан.
- [ ] (P1) Pipeline story Meta `Status: 🟢 Done`; epic Story 2; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/stories/STORY-IDS-PV-02-provider-owned-config/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-10-phone-verification/EPIC-IDS-10-phone-verification.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- Backlog file status sync (optional post-audit)
- PV-03 OTP engine
- Telnyx adapter — PV-06

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```
