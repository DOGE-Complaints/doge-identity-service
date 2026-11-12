## Task workspace — `task-ids-15-03-t01-attach-phone-sets-opaque`

- Story: [`../STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../STORY-IDS-VB-03-set-opaque-on-verification-success.md)
- Prerequisite: VB-01 Done (`identity_verified` column/model)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000052`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-03-set-opaque-on-verification-success.md) (Scope #1, AC-ID-THR-02/03, TECH-ARCH §2.3/§2.6)  
---

## Task: implement — phone attach sets `identity_verified=true`

### Цель
On successful `attach_phone_verification` (db_supabase + repositories), set `identity_verified=true` alongside existing method flags.

### Почему это важно
AC-ID-THR-03: opaque must persist on phone success path.

### Факты из кода
1. [`repositories.py:167+`](../../../../../../../src/core/infrastructure/repositories.py) — success `dataclasses.replace(..., phone_verified=True)` without opaque true.
2. [`db_supabase.py:497+`](../../../../../../../src/core/infrastructure/db_supabase.py) — same gap on Supabase path.
3. Handler call site: [`handlers.py`](../../../../../../../src/core/api/handlers.py) ~606 `attach_phone_verification`.

### Gap / Проблема
Phone success leaves `identity_verified` false / unchanged-false.

### AC/DoD
- [x] (P0) In-memory `attach_phone_verification` success → `identity_verified=True`.
- [x] (P0) Supabase `attach_phone_verification` success → persists `identity_verified=true`.
- [x] (P1) Method flags (`phone_verified`, provider, hash, …) behavior unchanged aside from opaque set.

### Где менять код
- `doge-identity-service/src/core/infrastructure/repositories.py`
- `doge-identity-service/src/core/infrastructure/db_supabase.py`

### Out of scope
- eID attach (t02); failure policy (t03); audit schema (t04); tests (t05); gate (t06)

### Проверка
```bash
rg -n 'identity_verified' doge-identity-service/src/core/infrastructure/repositories.py doge-identity-service/src/core/infrastructure/db_supabase.py
```
