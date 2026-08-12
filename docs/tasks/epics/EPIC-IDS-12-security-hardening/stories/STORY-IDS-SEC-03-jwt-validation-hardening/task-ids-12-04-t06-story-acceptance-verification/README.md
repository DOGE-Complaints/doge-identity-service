## Task workspace — `task-ids-12-04-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-SEC-03-jwt-validation-hardening.md`](../STORY-IDS-SEC-03-jwt-validation-hardening.md)
- Prerequisite: [`task-ids-12-04-t05-spec-09-g5-gap-closure-docs`](../task-ids-12-04-t05-spec-09-g5-gap-closure-docs/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000038`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md); [`story-acceptance-gate-template.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-SEC-03 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim (5 checkboxes): `aud` decision, conditional aud test, live key import, G-5 gap closure, regression baseline.

### Почему это важно
Story gate для pkg-000038; завершает G-5 JWT hardening wave.

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-SEC-03-jwt-validation-hardening.md`](../STORY-IDS-SEC-03-jwt-validation-hardening.md) (5 checkboxes verbatim).
2. Tasks t01–t05 — live aud decision, key import, registry/waiver, offline tests, docs.
3. Backlog source unchanged — [`STORY-IDS-SEC-03-jwt-validation-hardening.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-03-jwt-validation-hardening.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [ ] (P0) Story AC #1: `aud` decision documented — evidence t01, t03, t05.
- [ ] (P0) Story AC #2 (if validate): aud test — evidence t04.
- [ ] (P0) Story AC #3: live key import + code/spec alignment — evidence t02.
- [ ] (P0) Story AC #4: G-5 gap closed — evidence t05.
- [ ] (P0) Story AC #5: iss/sub/exp/role regression — evidence t04 full suite.
- [ ] (P1) `acceptance-verification-task-ids-12-04-t06-story-acceptance-verification.md` с PASS (P3 gate; `--print-utc-now` for Date).
- [ ] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 4; bullrun sync (same iteration).
- [ ] (P1) Backlog story Status → 🟢 Done (волна pkg-000038) optional sync.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-03-jwt-validation-hardening/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/EPIC-IDS-12-security-hardening.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- SEC-01/02 changes
- RS256/JWKS
- pkg-000037 yaml changes

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
