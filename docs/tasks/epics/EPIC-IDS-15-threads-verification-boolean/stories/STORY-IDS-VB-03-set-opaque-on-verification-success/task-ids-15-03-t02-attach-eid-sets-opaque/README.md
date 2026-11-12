## Task workspace — `task-ids-15-03-t02-attach-eid-sets-opaque`

- Story: [`../STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../STORY-IDS-VB-03-set-opaque-on-verification-success.md)
- Prerequisite: VB-01 Done; preferably after/with t01

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000052`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md) (Scope #2, AC-ID-THR-02/03, TECH-ARCH §2.3/§2.6)  
---

## Task: implement — eID attach sets `identity_verified=true`

### Цель
On successful `attach_eid_verification` (db_supabase + repositories), set `identity_verified=true` alongside existing method flags.

### Почему это важно
Same opaque contract for eID success path (AC-ID-THR-03 / AC-ID-THR-04 method-opaque).

### Факты из кода
1. [`repositories.py:105+`](../../../../../../../src/core/infrastructure/repositories.py) — eID success replace without opaque true.
2. [`db_supabase.py:417+`](../../../../../../../src/core/infrastructure/db_supabase.py) — same.
3. Handler call site: [`handlers.py`](../../../../../../../src/core/api/handlers.py) ~399 `attach_eid_verification`.

### Gap / Проблема
eID success does not set opaque true.

### AC/DoD
- [x] (P0) In-memory `attach_eid_verification` success → `identity_verified=True`.
- [x] (P0) Supabase `attach_eid_verification` success → persists `identity_verified=true`.
- [x] (P1) eID method flags behavior unchanged aside from opaque set.

### Где менять код
- `doge-identity-service/src/core/infrastructure/repositories.py`
- `doge-identity-service/src/core/infrastructure/db_supabase.py`

### Out of scope
- phone attach (t01); failure (t03); audit (t04); tests (t05); gate (t06)

### Проверка
```bash
rg -n 'attach_eid_verification|identity_verified' doge-identity-service/src/core/infrastructure/repositories.py doge-identity-service/src/core/infrastructure/db_supabase.py
```
