## Task workspace — `task-ids-09-04-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-EID-04-provider-owned-config.md`](../STORY-IDS-EID-04-provider-owned-config.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000017`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md`](../../../../../../analysis/authentigate-compatibility-audit-2026-06-07.md) §6 (F3, F4, F10)  
---

## Task: verify — STORY-IDS-EID-04 parent acceptance criteria

### Цель
Закрыть story parent AC: provider-owned config (ProviderConfigSpec, AuthentigateSettings, delegated validation, schema cleanup, .env.example, offline tests) — все 5 backlog AC [x].

### Почему это важно
Enabling wave EID-04 unlocks parallel EID-05/07/08 and capstone EID-02 per [`EPIC-IDS-EID.md`](../../../../../../backlog-stories/EPIC-IDS-EID.md).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-EID-04-provider-owned-config.md`](../STORY-IDS-EID-04-provider-owned-config.md) (5 checkboxes).
2. Tasks t01–t05 — implementation + tests.
3. No provider-if in schema — verify [`schema.py`](../../../../../../../src/core/config/schema.py) after t03.
4. Authentigate settings module — verify [`providers/authentigate/config.py`](../../../../../../../src/core/providers/authentigate/config.py) after t02.
5. EID-03 regression — [`test_provider_plugin_backbone.py`](../../../../../../../tests/test_provider_plugin_backbone.py).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [x] (P0) Story AC #1: Authentigate fields in `AuthentigateSettings`/`config_spec`, not in `load_config_from_env` body.
- [x] (P0) Story AC #2: authentigate missing required → `ConfigError` with field name — test evidence (t05).
- [x] (P0) Story AC #3: no provider logic in `schema.py` — grep/code review checklist.
- [x] (P0) Story AC #4: scopes default full claim-URLs — unit evidence (t02/t05); SPIKE-09 live confirm deferred.
- [x] (P0) Story AC #5: `.env.example` updated; offline pytest green; missing required test — evidence (t04/t05).
- [x] (P1) `acceptance-verification-task-ids-09-04-t06-story-acceptance-verification.md` создан.
- [x] (P1) Pipeline story Meta `Status: 🟢 Done`; bullrun sync (same iteration).

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-09-eid-verification/stories/STORY-IDS-EID-04-provider-owned-config/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/bullrun-launch-index.md` (story/task statuses)

### Out of scope
- Backlog file status sync (optional separate audit task)
- Epic AC gate EPIC-IDS-09 (отдельная операция)
- EID-03 audit t07 override wave
- EID-02 / EID-05 intake

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
grep -n "eideasy\|authentigate" src/core/config/schema.py
```
