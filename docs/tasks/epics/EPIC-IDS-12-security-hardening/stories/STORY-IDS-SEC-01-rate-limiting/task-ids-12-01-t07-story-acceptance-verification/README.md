## Task workspace — `task-ids-12-01-t07-story-acceptance-verification`

- Story: [`../STORY-IDS-SEC-01-rate-limiting.md`](../STORY-IDS-SEC-01-rate-limiting.md)
- Prerequisite: [`task-ids-12-01-t06-offline-rate-limit-tests`](../task-ids-12-01-t06-offline-rate-limit-tests/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000035`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-01-rate-limiting.md); [`story-acceptance-gate-template.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-SEC-01 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim (6 checkboxes): route table, 429 envelope, cross-cutting layer, OTP policy, config+test, or DEFERRED path.

### Почему это важно
Story gate для pkg-000035; разблокирует SEC-02 (request context for IP/UA).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-SEC-01-rate-limiting.md`](../STORY-IDS-SEC-01-rate-limiting.md) (6 checkboxes verbatim).
2. Tasks t01–t06 — implementation + tests.
3. Runtime touchpoint: [`04-security.md`](../../../../../../../runtime-docs/04-security.md) anti-abuse.
4. AC #6 DEFERRED — only if operator explicitly chooses not to build.

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [ ] (P0) Story AC #1: sensitive routes + eid/start 5/10min — evidence t01, t04, t06.
- [ ] (P0) Story AC #2: 429 + retry_after envelope — evidence t03, t06.
- [ ] (P0) Story AC #3: cross-cutting layer — evidence t03, t04.
- [ ] (P0) Story AC #4: OTP cooldown policy — evidence t05, t06 regression.
- [ ] (P0) Story AC #5: config + N+1 test — evidence t01, t06.
- [ ] (P1) `acceptance-verification-task-ids-12-01-t07-story-acceptance-verification.md` с PASS (P3 gate; `--print-utc-now` for Date).
- [ ] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 1; bullrun sync (same iteration).
- [ ] (P1) Sync [`04-security.md`](../../../../../../../runtime-docs/04-security.md) rate-limit row.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-01-rate-limiting/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/EPIC-IDS-12-security-hardening.md`
- `doge-identity-service/docs/runtime-docs/04-security.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- SEC-02 implementation
- phone/request HTTP limit (follow-up)
- Backlog file deletion

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
```
