## Task workspace — `task-ids-12-05-t03-service-role-rotation-runbook`

- Story: [`../STORY-IDS-SEC-04-service-role-isolation.md`](../STORY-IDS-SEC-04-service-role-isolation.md)
- Prerequisite: [`task-ids-12-05-t01-service-role-boundary-docs-sync`](../task-ids-12-05-t01-service-role-boundary-docs-sync/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000043`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md) Scope §Rotation runbook; Story AC #3  
---

## Task: add — Supabase service_role rotation runbook

### Цель
Документировать операционную процедуру: Supabase Dashboard → rotate key → update `SUPABASE_SERVICE_ROLE` in identity env — Story AC #3.

### Почему это важно
После инцидента с `spa-app/.env` нужна воспроизводимая процедура ротации без ad-hoc шагов.

### Факты из кода
1. Key read from env — [`schema.py`](../../../../../../../src/core/config/schema.py) `supabase_service_role`.
2. Runbook index — [`docs/runbook/README.md`](../../../../../../../docs/runbook/README.md).

### Gap / Проблема
Нет dedicated runbook `supabase-service-role-rotation.md` с шагами, триггерами и rollback note.

### AC/DoD
- [x] (P0) New [`docs/runbook/supabase-service-role-rotation.md`](../../../../../../../docs/runbook/supabase-service-role-rotation.md): steps, triggers (leak suspicion, spa bundle), rollback note.
- [x] (P0) Link from [`docs/runbook/README.md`](../../../../../../../docs/runbook/README.md).
- [x] (P1) Story AC #3.

### Где менять код
- `doge-identity-service/docs/runbook/supabase-service-role-rotation.md` (new at P3)
- `doge-identity-service/docs/runbook/README.md`

### Out of scope
- Spa coordination checklist detail (t04 — may extend same runbook §)
- Actual key rotation in production

### Проверка
```bash
cd doge-identity-service
test -f docs/runbook/supabase-service-role-rotation.md
grep -n 'Dashboard\|SUPABASE_SERVICE_ROLE\|rollback\|утечк' docs/runbook/supabase-service-role-rotation.md
grep -n 'supabase-service-role-rotation' docs/runbook/README.md
```
