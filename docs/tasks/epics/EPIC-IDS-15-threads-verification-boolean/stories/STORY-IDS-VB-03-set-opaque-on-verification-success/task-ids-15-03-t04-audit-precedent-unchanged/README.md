## Task workspace — `task-ids-15-03-t04-audit-precedent-unchanged`

- Story: [`../STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../STORY-IDS-VB-03-set-opaque-on-verification-success.md)
- Prerequisite: —

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000052`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md) (Scope #4, AC-ID-THR-05)  
---

## Task: verify — keep `_log_phone_audit` / `_log_eid_audit` (no new schema)

### Цель
Confirm AC-ID-THR-05: attempt audit remains via existing `_log_phone_audit` / `_log_eid_audit`; no new «opaque flipped» event type / schema.

### Почему это важно
REQ21 audit precedent — method may appear in audit; opaque boolean must not disclose method; no new schema.

### Факты из кода
1. [`handlers.py:114`](../../../../../../../src/core/api/handlers.py) `_log_phone_audit`
2. [`handlers.py:145`](../../../../../../../src/core/api/handlers.py) `_log_eid_audit`
3. Call sites on phone/eID flows remain (story Verified).

### Gap / Проблема
Risk of inventing new audit event while wiring opaque — must not.

### AC/DoD
- [x] (P0) `_log_phone_audit` / `_log_eid_audit` signatures and call sites retained (no replacement schema).
- [x] (P0) No new audit event type for opaque flip.
- [x] (P1) Evidence: `rg` / acceptance notes.

### Где менять код
- Prefer verify-only; do not add new audit schema

### Out of scope
- attach success impl (t01/t02); tests beyond grep (t05)

### Проверка
```bash
rg -n 'def _log_phone_audit|def _log_eid_audit|_log_phone_audit\(|_log_eid_audit\(' doge-identity-service/src/core/api/handlers.py
rg -n 'opaque|identity_verified.*audit|audit.*identity_verified' doge-identity-service/src/core || true
```
