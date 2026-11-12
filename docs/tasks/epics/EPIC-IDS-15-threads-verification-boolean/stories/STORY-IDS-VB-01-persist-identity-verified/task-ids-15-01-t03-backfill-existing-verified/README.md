## Task workspace — `task-ids-15-01-t03-backfill-existing-verified`

- Story: [`../STORY-IDS-VB-01-persist-identity-verified.md`](../STORY-IDS-VB-01-persist-identity-verified.md)
- Prerequisite: [`t01`](../task-ids-15-01-t01-migration-identity-verified/README.md) (column exists)

---
**Приоритет:** P0  
**Сложность:** M  
**Статус:** done  
**Wave:** `pkg-000050`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md`](../../../../../../backlog-stories/threads-verification-boolean/STORY-IDS-VB-01-persist-identity-verified.md) (Scope #2, AC #2,#3, TECH-ARCH §2.3–2.4)  
---

## Task: implement — one-shot backfill `phone_verified OR eid_verified` → opaque true

### Цель
One-shot backfill: rows with `phone_verified OR eid_verified` → `identity_verified=true` (arch §2.4). Failure paths не требуют clear-on-failure (arch §2.3 / AC #3) — этот task не добавляет clear-on-failure logic.

### Почему это важно
Существующие verified пользователи должны получить opaque true без ручного OR на read.

### Факты из кода
1. Story approach: `UPDATE … SET identity_verified = true WHERE phone_verified OR eid_verified`.
2. Phone migration etalon pattern: [`20260611000001_profiles_phone_verification.sql`](../../../../../../../supabase/migrations/20260611000001_profiles_phone_verification.sql).
3. Backfill may live in same migration as t01 or a follow-up migration — prefer one coherent migration wave; keep SQL auditable.
4. No clear-on-failure requirement (TECH-ARCH §2.3) — do not invent failure clear hooks here (VB-03 owns success writes).

### Gap / Проблема
После ADD COLUMN default false оставляет verified rows opaque=false without backfill.

### AC/DoD
- [x] (P0) One-shot SQL (or equivalent) sets `identity_verified=true` where `phone_verified OR eid_verified`.
- [x] (P0) Rows with neither method flag remain `identity_verified=false`.
- [x] (P0) No clear-on-failure behavior introduced (AC #3).
- [x] (P1) Bootstrap parity if backfill is migration-only (document or mirror as appropriate; do not invent live jobs).

### Где менять код
- `doge-identity-service/supabase/migrations/` (backfill in t01 migration or dedicated follow-up)
- Optionally `doge-identity-service/supabase/bootstrap/000_full_init.sql` if bootstrap needs consistent end-state for fresh installs

### Out of scope
- Model map (t02) beyond consuming column; phone/eID success writers (VB-03); `/me` (VB-02); tests (t04)

### Проверка
```bash
rg -n 'identity_verified|phone_verified OR|eid_verified' doge-identity-service/supabase/migrations
```
