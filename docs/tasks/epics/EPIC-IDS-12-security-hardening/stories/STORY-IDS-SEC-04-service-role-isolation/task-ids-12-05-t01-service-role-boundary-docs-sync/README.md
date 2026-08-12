## Task workspace — `task-ids-12-05-t01-service-role-boundary-docs-sync`

- Story: [`../STORY-IDS-SEC-04-service-role-isolation.md`](../STORY-IDS-SEC-04-service-role-isolation.md)

---
**Приоритет:** P0  
**Сложность:** S  
**Статус:** done  
**Wave:** `pkg-000043`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md`](../../../../../../backlog-stories/security-hardening/STORY-IDS-SEC-04-service-role-isolation.md) Scope §Инвариант границы; Story AC #1  
---

## Task: fix — document service_role boundary invariant (identity-only holder)

### Цель
Зафиксировать требование: `SUPABASE_SERVICE_ROLE` существует **только** в server env `doge-identity-service`, **никогда** в spa/браузере/клиентских артефактах — Story AC #1.

### Почему это важно
Cross-service security boundary: единственный легитимный держатель привилегированного ключа — identity-backend.

### Факты из кода
1. `supabase_service_role` pilot-required — [`schema.py:33,159,165-166,184`](../../../../../../../src/core/config/schema.py).
2. Partial mention in runtime security — [`04-security.md:143,159`](../../../../../../../docs/runtime-docs/04-security.md).
3. Env handbook may need explicit § — [`env-secrets-handbook.md`](../../../../../../../docs/runbook/env-secrets-handbook.md).

### Gap / Проблема
Docs не содержат явного инварианта «identity — единственный держатель service_role; не в браузере» во всех целевых местах (04-security, 07-env, runbook cross-link).

### AC/DoD
- [x] (P0) [`04-security.md`](../../../../../../../docs/runtime-docs/04-security.md) — явный инвариант границы service_role (identity-only).
- [x] (P0) [`07-env-configuration-spec.md`](../../../../../../../docs/requirements/07-env-configuration-spec.md) — `SUPABASE_SERVICE_ROLE` server-only, не клиент.
- [x] (P1) Cross-link в [`env-secrets-handbook.md`](../../../../../../../docs/runbook/env-secrets-handbook.md) (optional §).
- [x] (P1) Story AC #1 — grep docs: «identity-only holder» / эквивалент; нет claim что spa держит service_role.

### Где менять код
- `doge-identity-service/docs/runtime-docs/04-security.md`
- `doge-identity-service/docs/requirements/07-env-configuration-spec.md`
- `doge-identity-service/docs/runbook/env-secrets-handbook.md` (optional)

### Out of scope
- No-expose tests (t02)
- Rotation runbook (t03)
- Spa key removal (SPA SEC-01)

### Проверка
```bash
cd doge-identity-service
grep -rn 'service_role\|SERVICE_ROLE' docs/runtime-docs/04-security.md docs/requirements/07-env-configuration-spec.md docs/runbook/env-secrets-handbook.md
grep -rn 'единственн\|identity-only\|only.*identity' docs/runtime-docs/04-security.md docs/requirements/07-env-configuration-spec.md
```
