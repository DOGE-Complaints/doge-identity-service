## Task workspace — `task-ids-15-01-t04-offline-persist-tests`

- Story: [`../STORY-IDS-VB-01-persist-identity-verified.md`](../STORY-IDS-VB-01-persist-identity-verified.md)
- Prerequisite: [`t01`](../task-ids-15-01-t01-migration-identity-verified/README.md), [`t02`](../task-ids-15-01-t02-profile-model-and-db-map/README.md), [`t03`](../task-ids-15-01-t03-backfill-existing-verified/README.md)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000050`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md) (Scope #4, AC #4)  
---

## Task: test — offline persist + backfill semantics

### Цель
Offline tests: default false; map round-trip; backfill semantics (`phone_verified OR eid_verified` → opaque true). Suite marker `-m "not live_integration"` green for touched tests.

### Почему это важно
Story AC #4 / Scope #4 — without tests persist/backfill regress silently.

### Факты из кода
1. Test root: `doge-identity-service/tests/` (71+ files historically).
2. Profile/map coverage likely near existing supabase/repository tests — extend or add focused module (P3 chooses path; do not invent product API).
3. Profile test command (profile): `cd doge-identity-service && python3 -m pytest -q -m "not live_integration"`.

### Gap / Проблема
Нет offline assertions on `identity_verified` map/backfill until this task.

### AC/DoD
- [x] (P0) Test: new profile / default → `identity_verified` false.
- [x] (P0) Test: row map round-trip preserves `identity_verified` true/false.
- [x] (P0) Test: backfill semantics — method OR → opaque true; neither → false (unit or SQL-fixture level as codebase allows offline).
- [x] (P0) Touched tests pass under `-m "not live_integration"`.

### Где менять код
- `doge-identity-service/tests/` (new or extend)

### Out of scope
- Live integration / Railway; `/me` payload tests (VB-02); success-hook tests (VB-03); story gate sync (t05)

### Проверка
```bash
cd doge-identity-service && python3 -m pytest -q -m "not live_integration" -k identity_verified
# or broader touched paths once named in P3
```
