## Task workspace — `task-ids-15-03-t03-failure-no-clear-opaque`

- Story: [`../STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../STORY-IDS-VB-03-set-opaque-on-verification-success.md)
- Prerequisite: t01/t02 success paths understood

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000052`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md) (Scope #3, D-VB-3, TECH-ARCH §2.3)  
---

## Task: verify/guard — failure does not set/clear opaque

### Цель
Ensure failure paths neither set `identity_verified=true` nor clear an already-true opaque (arch §2.3 / D-VB-3). Document/confirm no clear-on-failure hooks added.

### Почему это важно
Story AC: failure must leave opaque unchanged.

### Факты из кода
1. Attach methods raise `ProfileConflictError` on hash conflicts — before success replace.
2. Phone/eID confirm handlers log audit on failure without calling attach on fail paths (verify at P3).
3. TECH-ARCH §2.3: no clear-on-failure requirement.

### Gap / Проблема
Need explicit confirmation + any missing guards if code incorrectly clears opaque.

### AC/DoD
- [x] (P0) No code path clears `identity_verified` to false on verification failure.
- [x] (P0) Failure paths do not call attach success replace (or equivalent) that would set opaque true incorrectly.
- [x] (P1) Document evidence in acceptance (paths reviewed).

### Где менять код
- Prefer verify-only; change only if a clear-on-failure bug found in handlers/repos

### Out of scope
- Implementing success set (t01/t02); audit schema (t04); tests (t05)

### Проверка
```bash
rg -n 'identity_verified\s*=' doge-identity-service/src/core
rg -n 'identity_verified' doge-identity-service/src/core/api/handlers.py
```
