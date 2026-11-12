## Task workspace — `task-ids-15-03-t05-offline-success-failure-tests`

- Story: [`../STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../STORY-IDS-VB-03-set-opaque-on-verification-success.md)
- Prerequisite: t01–t04

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000052`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md) (Scope #5, AC tests)  
---

## Task: test — offline success/failure opaque behavior

### Цель
Offline tests: attach success → `identity_verified` true; failure → opaque unchanged; audit helpers still used (no new schema). Extend existing attach tests or add focused module.

### Почему это важно
Offline proof of AC-ID-THR-03/05 without live EE.

### Факты из кода
1. Existing tests around phone/eID attach / repositories (discover at P3).
2. In-memory repos are primary offline target.

### Gap / Проблема
No offline coverage that opaque flips on attach success / stays on failure.

### AC/DoD
- [x] (P0) Phone attach success → opaque true (offline).
- [x] (P0) eID attach success → opaque true (offline).
- [x] (P0) Failure / conflict path → opaque unchanged (incl. already-true).
- [x] (P1) `pytest -m "not live_integration"` green for touched.

### Где менять код
- `doge-identity-service/tests/` (extend existing or new focused test file)

### Out of scope
- live EE smoke; OAuth introspection rewrite; story gate (t06)

### Проверка
```bash
cd doge-identity-service && python3 -m pytest -q -m "not live_integration" -k "attach or identity_verified or opaque"
```
