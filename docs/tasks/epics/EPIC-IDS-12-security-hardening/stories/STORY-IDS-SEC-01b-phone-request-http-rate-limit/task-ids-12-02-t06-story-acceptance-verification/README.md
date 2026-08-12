## Task workspace — `task-ids-12-02-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md)
- Prerequisite: [`task-ids-12-02-t05-offline-phone-request-rate-limit-tests`](../task-ids-12-02-t05-offline-phone-request-rate-limit-tests/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000036`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md); [`story-acceptance-gate-template.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-SEC-01b parent acceptance criteria

### Цель
Закрыть story parent AC verbatim (4 checkboxes): wire+config, 429 vs 400 policy, docs, offline tests.

### Почему это важно
Story gate для pkg-000036; завершает остаток G-1 (phone/request).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../STORY-IDS-SEC-01b-phone-request-http-rate-limit.md) (4 checkboxes verbatim).
2. Tasks t01–t05 — implementation + tests + docs.
3. Backlog source unchanged — [`STORY-IDS-SEC-01b-phone-request-http-rate-limit.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01b-phone-request-http-rate-limit.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [ ] (P0) Story AC #1: phone/request wired + config — evidence t01–t03.
- [ ] (P0) Story AC #2: 429 window vs 400 cooldown — evidence t04, t05.
- [ ] (P0) Story AC #3: coexistence policy docs — evidence t04.
- [ ] (P0) Story AC #4: offline both scenarios — evidence t05.
- [ ] (P1) `acceptance-verification-task-ids-12-02-t06-story-acceptance-verification.md` с PASS (P3 gate; `--print-utc-now` for Date).
- [ ] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 2; bullrun sync (same iteration).
- [ ] (P1) Backlog story Status → 🟢 Done (волна pkg-000036) optional sync.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01b-phone-request-http-rate-limit/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/EPIC-IDS-12-security-hardening.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- SEC-02 implementation
- pkg-000035 yaml changes

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
```
