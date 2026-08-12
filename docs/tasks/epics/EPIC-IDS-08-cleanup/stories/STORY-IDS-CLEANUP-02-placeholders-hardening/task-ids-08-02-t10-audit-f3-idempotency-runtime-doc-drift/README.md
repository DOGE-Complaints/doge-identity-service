## Task workspace — `task-ids-08-02-t10-audit-f3-idempotency-runtime-doc-drift`

- Story: [`../STORY-IDS-CLEANUP-02-placeholders-hardening.md`](../STORY-IDS-CLEANUP-02-placeholders-hardening.md)
- Audit source: [`../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md) (F3)

---
**Приоритет:** P1  
**Сложность:** S  
**Статус:** done  
**Wave:** `override epic_ids_08_cleanup_02_audit_2026_06_05`  
**Skill declared:** python-pro  
**Decision Ref:** [`../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md`](../../../../../../analysis/epic-ids-08-cleanup-02-audit-2026-06-05.md) §F3 · t05 follow-up (E21 «убрать»)  
---

## Task: fix/docs — idempotency runtime-doc drift (F3)

### Цель
Выровнять [`01-api.md`](../../../../../../../docs/runtime-docs/01-api.md) с решением t05: `idempotency.py` удалён, резолвер больше не существует.

### Почему это важно
Битая ссылка на удалённый файл и ложное «резолвер готов» вводят в заблуждение при onboarding по runtime-docs.

### Факты из кода
1. [`01-api.md:50`](../../../../../../../docs/runtime-docs/01-api.md) — bullet «Idempotency-key» со ссылкой на [`idempotency.py`](../../../../../../../src/core/api/idempotency.py).
2. `src/core/api/idempotency.py` — **отсутствует** (удалён в P3 t05).
3. Grep `resolve_idempotency_key|idempotency.py` в `src/` = 0.
4. Owner decision E21: **убрать** ([`owner-decisions-e17-e22.md`](../task-ids-08-02-t01-owner-decisions-placeholders-e17-e22/owner-decisions-e17-e22.md)).

### Gap / Проблема
Runtime-doc описывает заготовку, которую CLEANUP-02 сознательно убрал.

### AC/DoD
- [ ] (P0) Bullet §«Idempotency-key» в `01-api.md` удалён или переписан: модуль удалён в CLEANUP-02; idempotency deferred to functional epic / POST routes when implemented.
- [ ] (P0) Нет битых ссылок на `idempotency.py` в `01-api.md`.
- [ ] (P1) BULLRUN-PHASE-LOG + acceptance-verification в этой папке (P3).

### Где менять код
- [`docs/runtime-docs/01-api.md`](../../../../../../../docs/runtime-docs/01-api.md) — §«Что ещё есть под капотом» (~line 50)

### Out of scope
- Восстановление `src/core/api/idempotency.py` (противоречит E21/t05)
- Полный runtime-docs sync (CLEANUP-03)

### Проверка
```bash
grep -n "idempotency" doge-identity-service/docs/runtime-docs/01-api.md
test ! -f doge-identity-service/src/core/api/idempotency.py
```
