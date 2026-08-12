## Task workspace — `task-ids-12-05-t06-audit-f1-platform-wording-separation-sync`

- Story: [`../STORY-IDS-SEC-04-service-role-isolation.md`](../STORY-IDS-SEC-04-service-role-isolation.md)
- Prerequisite: [`task-ids-12-05-t05-story-acceptance-verification`](../task-ids-12-05-t05-story-acceptance-verification/README.md)
- Audit source: [`../../../../../../analysis/epic-ids-12-sec-04-audit-2026-07-09.md`](../../../../../../analysis/epic-ids-12-sec-04-audit-2026-07-09.md) (F1)

---
**Приоритет:** P2  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_12_sec_04_audit_2026_07_09`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-12-sec-04-audit-2026-07-09.md`](../../../../../../analysis/epic-ids-12-sec-04-audit-2026-07-09.md) §3 F1  
---

## Task: fix — clarify service_role boundary wording (identity project vs platform)

### Цель
Устранить doc-overclaim F1: «единственный держатель … **в платформе**» — уточнить, что identity держит **identity Supabase project** `service_role`; gateway — отдельный Supabase-проект/ключ.

### Почему это важно
[`04-security.md:147`](../../../../../../../docs/runtime-docs/04-security.md) завышает scope; [`doge-complaints-gateway/src/core/config/schema.py:523-525`](../../../../../../../../doge-complaints-gateway/src/core/config/schema.py) тоже имеет `SUPABASE_SERVICE_ROLE` для своего проекта. Риск — неверная семантика инварианта, не утечка identity-ключа.

### Факты из кода
1. Overclaim — [`04-security.md:147`](../../../../../../../docs/runtime-docs/04-security.md): «единственный держатель … в платформе».
2. Partial spec — [`07-env-configuration-spec.md:29`](../../../../../../../docs/requirements/07-env-configuration-spec.md): «Только server-side. Никогда в браузер» без project separation.
3. Separation audit — [`supabase-project-separation-audit-2026-06-03.md`](../../../../../../analysis/supabase-project-separation-audit-2026-06-03.md).
4. Gateway env — [`doge-complaints-gateway/.../schema.py:523-525`](../../../../../../../../doge-complaints-gateway/src/core/config/schema.py).
5. Story AC #1 scope — identity↔spa/browser boundary выполнен; wording — F1.

### Gap / Проблема
Docs описывают platform-wide uniqueness; фактически — per-service Supabase project. Spa/browser invariant корректен.

### AC/DoD
- [x] (P0) [`04-security.md`](../../../../../../../docs/runtime-docs/04-security.md) §5.1 — «identity Supabase project» / не «единственный в платформе» без qualification; spa/browser запрет сохранён.
- [x] (P0) [`07-env-configuration-spec.md`](../../../../../../../docs/requirements/07-env-configuration-spec.md) — `SUPABASE_SERVICE_ROLE` scoped to identity server env + identity project; cross-link separation audit.
- [x] (P1) Optional: [`env-secrets-handbook.md`](../../../../../../../docs/runbook/env-secrets-handbook.md) — one-line gateway ≠ identity key.
- [x] (P1) grep docs: нет unqualified «единственный … в платформе».

### Где менять код
- `doge-identity-service/docs/runtime-docs/04-security.md`
- `doge-identity-service/docs/requirements/07-env-configuration-spec.md`
- optional: `doge-identity-service/docs/runbook/env-secrets-handbook.md`

### Out of scope
- Gateway code or env changes
- Spa SEC-01 implementation
- F2 test depth (t07)
- Новый `pkg-*.yaml`, смена `identity-active-package.current.yaml`

### Проверка
```bash
cd doge-identity-service
grep -n 'единственн\|platform\|identity project' docs/runtime-docs/04-security.md docs/requirements/07-env-configuration-spec.md
grep -n 'единственный.*платформ' docs/runtime-docs/04-security.md docs/requirements/07-env-configuration-spec.md && exit 1 || true
```
