## Task workspace — `task-ids-12-03-t06-story-acceptance-verification`

- Story: [`../STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../STORY-IDS-SEC-02-audit-ip-ua-hashing.md)
- Prerequisite: [`task-ids-12-03-t05-offline-audit-ip-ua-hash-no-pii-tests`](../task-ids-12-03-t05-offline-audit-ip-ua-hash-no-pii-tests/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000037`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md); [`story-acceptance-gate-template.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)  
---

## Task: verify — STORY-IDS-SEC-02 parent acceptance criteria

### Цель
Закрыть story parent AC verbatim (5 checkboxes): request context both modes, hash-only storage, PhoneAuditEvent fields, PII invariant, HMAC spec alignment.

### Почему это важно
Story gate для pkg-000037; завершает G-2b (IP/UA hash audit).

### Факты из кода
1. Pipeline story AC — [`../STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../STORY-IDS-SEC-02-audit-ip-ua-hashing.md) (5 checkboxes verbatim).
2. Tasks t01–t05 — model, helper, eID/phone wiring, tests, docs (t02).
3. Backlog source unchanged — [`STORY-IDS-SEC-02-audit-ip-ua-hashing.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-02-audit-ip-ua-hashing.md).

### Gap / Проблема
Story parent AC ещё `[ ]` до финальной сверки gates.

### AC/DoD
- [ ] (P0) Story AC #1: request context eID + phone — evidence t03, t04.
- [ ] (P0) Story AC #2: hash-only storage — evidence t02, t05.
- [ ] (P0) Story AC #3: PhoneAuditEvent fields — evidence t01, t04.
- [ ] (P0) Story AC #4: no PII invariant — evidence t05.
- [ ] (P0) Story AC #5: HMAC documented vs spec 16 — evidence t02.
- [ ] (P1) `acceptance-verification-task-ids-12-03-t06-story-acceptance-verification.md` с PASS (P3 gate; `--print-utc-now` for Date).
- [ ] (P1) Pipeline story Meta `Status: 🟢 Done`; epic §Story 3; bullrun sync (same iteration).
- [ ] (P1) Backlog story Status → 🟢 Done (волна pkg-000037) optional sync.

### Где менять код
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/stories/STORY-IDS-SEC-02-audit-ip-ua-hashing/` (acceptance doc, story status)
- `doge-identity-service/docs/tasks/epics/EPIC-IDS-12-security-hardening/EPIC-IDS-12-security-hardening.md`
- `doge-identity-service/docs/tasks/bullrun-launch-index.md`

### Out of scope
- SEC-03 implementation
- PV-09 durable migration
- pkg-000036 yaml changes

### Проверка
```bash
cd doge-identity-service
.venv/bin/python -m pytest -m "not live_integration" -q
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify
python3 ../docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project identity --verify --check-dates
```
