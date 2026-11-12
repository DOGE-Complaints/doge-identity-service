## Task workspace — `task-ids-15-01-t01-migration-identity-verified`

- Story: [`../STORY-IDS-VB-01-persist-identity-verified.md`](../STORY-IDS-VB-01-persist-identity-verified.md)
- Prerequisite: —

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000050`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md) (Scope #1, AC #1, TECH-ARCH §2.2)  
---

## Task: implement — migration + bootstrap `profiles.identity_verified`

### Цель
Добавить persisted column `profiles.identity_verified BOOLEAN NOT NULL DEFAULT FALSE` (физическое имя = wire). Синхронизировать bootstrap `000_full_init.sql` с etalon phone-column migration.

### Почему это важно
Story AC #1 / Scope #1: first-class opaque flag без read-time OR (D-VB-1).

### Факты из кода
1. Phone etalon [`20260611000001_profiles_phone_verification.sql`](../../../../../../../supabase/migrations/20260611000001_profiles_phone_verification.sql) — `ADD COLUMN IF NOT EXISTS phone_verified BOOLEAN NOT NULL DEFAULT FALSE` (+ related cols).
2. Profiles create [`20260525000001_create_profiles.sql`](../../../../../../../supabase/migrations/20260525000001_create_profiles.sql) — `eid_verified` there; no `identity_verified`.
3. Bootstrap [`000_full_init.sql`](../../../../../../../supabase/bootstrap/000_full_init.sql) exists (~230+ phone section per story Verified).
4. `rg identity_verified` in `supabase/` expected empty before this task (P3 verify).

### Gap / Проблема
Нет колонки `identity_verified` в migrations/bootstrap.

### AC/DoD
- [x] (P0) New migration adds `identity_verified BOOLEAN NOT NULL DEFAULT FALSE` on `public.profiles` (IF NOT EXISTS pattern).
- [x] (P0) Bootstrap `000_full_init.sql` includes the same column (parity with phone etalon habit).
- [x] (P1) No change to `/me` payload (VB-02 OOS).
- [x] (P1) No write hooks on phone/eID success (VB-03 OOS).

### Где менять код
- `doge-identity-service/supabase/migrations/` (new timestamped migration)
- `doge-identity-service/supabase/bootstrap/000_full_init.sql`

### Out of scope
- Domain/model map (t02); backfill SQL semantics beyond column default (t03); tests (t04); story gate (t05)

### Проверка
```bash
rg -n 'identity_verified' doge-identity-service/supabase/migrations doge-identity-service/supabase/bootstrap/000_full_init.sql
ls doge-identity-service/supabase/migrations/*identity* 2>/dev/null || true
```
