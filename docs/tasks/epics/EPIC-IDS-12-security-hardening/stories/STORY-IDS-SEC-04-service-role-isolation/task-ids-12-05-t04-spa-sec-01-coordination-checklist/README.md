## Task workspace — `task-ids-12-05-t04-spa-sec-01-coordination-checklist`

- Story: [`../STORY-IDS-SEC-04-service-role-isolation.md`](../STORY-IDS-SEC-04-service-role-isolation.md)
- Cross-service: [`STORY-SPA-SEC-01`](../../../../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md)
- Prerequisite: [`task-ids-12-05-t03-service-role-rotation-runbook`](../task-ids-12-05-t03-service-role-rotation-runbook/README.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000043`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md) Scope §Координация с spa; Story AC #4  
---

## Task: add — cross-service rotation checklist (identity + spa SEC-01)

### Цель
Checklist координированной ротации после выноса `service_role` из фронта (SPA SEC-01) — единая точка решения — Story AC #4.

### Почему это важно
Ротация без синхронизации identity/spa может оставить старый ключ внутый в bundle или сломать deploy window.

### Факты из кода
1. Parity spa story — [`STORY-SPA-SEC-01`](../../../../../../../../spa-app/docs/tasks/backlog-stories/security-hardening/STORY-SPA-SEC-01-remove-service-role-from-frontend.md).
2. Rotation runbook scaffold — t03 `supabase-service-role-rotation.md`.

### Gap / Проблема
Нет checklist, связывающего identity rotation runbook с spa SEC-01 AC и порядком действий.

### AC/DoD
- [x] (P0) § Spa coordination in [`supabase-service-role-rotation.md`](../../../../../../../docs/runbook/supabase-service-role-rotation.md) OR dedicated subsection — references spa SEC-01 AC.
- [x] (P0) Single decision point: when to rotate (post spa key removal, leak, etc.).
- [x] (P1) Story AC #4.

### Где менять код
- `doge-identity-service/docs/runbook/supabase-service-role-rotation.md` § Spa coordination

### Out of scope
- Implementing spa SEC-01 (spa repo)
- BFF login model (SEC-05)

### Проверка
```bash
cd doge-identity-service
grep -n 'SEC-01\|spa\|coordination\|координ' docs/runbook/supabase-service-role-rotation.md
```
